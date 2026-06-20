"""
SSE endpoint backed by Postgres LISTEN/NOTIFY instead of Redis Pub/Sub.

Pattern:
  1. On connect, replay any events already written for this run_id (covers
     the case where the worker finished — or got ahead — before the client
     connected).
  2. If the run isn't finished yet, open a dedicated asyncpg connection and
     LISTEN on the notify channel. Each NOTIFY just carries the run_id; on
     wake-up we re-query for any event rows newer than the last one we sent.
  3. Stop when we see a 'done' or 'error' event.

Each open SSE connection holds one dedicated Postgres connection for the
LISTEN. That's the real cost vs. Redis pub/sub -- fine for tens/low hundreds
of concurrent streams, worth revisiting (e.g. a single fan-out listener
process + asyncio queues per run_id) if you scale past that.
"""

import asyncio
import json

import asyncpg
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.core.db import db
from app.core.settings import settings

router = APIRouter(
    prefix="/adk",
    tags=["Google ADK"],
)


def _format_sse(event_type: str, payload: dict) -> str:
    return f"event: {event_type}\ndata: {json.dumps(payload)}\n\n"


@router.get("/chat/stream/{run_id}")
async def stream_chat(run_id: str):
    async def event_generator():
        conn = await asyncpg.connect(settings.database_url)
        notify_queue: asyncio.Queue[str] = asyncio.Queue()

        def _on_notify(_connection, _pid, _channel, payload):
            notify_queue.put_nowait(payload)

        await conn.add_listener(db.NOTIFY_CHANNEL, _on_notify)
        last_seq = 0
        try:
            # 1. Catch up on anything already written.
            rows = await db.fetch_events_after(conn, run_id, last_seq)
            for row in rows:
                last_seq = row["seq"]
                yield _format_sse(row["event_type"], json.loads(row["payload"]))
                if row["event_type"] in ("done", "error"):
                    return

            # 2. Wait for live updates.
            while True:
                notified_run_id = await notify_queue.get()
                if notified_run_id != run_id:
                    continue  # someone else's run, shared channel

                rows = await db.fetch_events_after(conn, run_id, last_seq)
                for row in rows:
                    last_seq = row["seq"]
                    yield _format_sse(row["event_type"], json.loads(row["payload"]))
                    if row["event_type"] in ("done", "error"):
                        return
        finally:
            await conn.remove_listener(db.NOTIFY_CHANNEL, _on_notify)
            await conn.close()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
