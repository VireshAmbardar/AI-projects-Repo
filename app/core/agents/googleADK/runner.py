"""
Celery task: runs the ADK agent for one chat turn and persists every event
to Postgres (agent_events table), NOTIFYing on each insert so the SSE
endpoint can forward it to the browser in near-real-time.

NOTE: Celery tasks are synchronous by default. ADK's Runner is async-only
(`run_async` is an async generator), so each task spins up its own asyncio
event loop with `asyncio.run(...)`. That's normal and fine for one task per
worker process/thread — just don't try to call asyncio.run() from inside
code that's already in an event loop.
"""

import asyncio
import json

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.core.agents.googleADK.base import root_agent
from app.core.celery.celery_app import celery_app
from app.core.db import db
from uuid import uuid4

APP_NAME = "bond_scanner"


def _event_to_dict(event) -> dict:
    """ADK Event objects are pydantic models — dump to plain JSON-safe dict."""
    try:
        return json.loads(event.model_dump_json(exclude_none=True))
    except Exception:
        # Fallback so a serialization quirk never silently drops an event
        return {"raw": str(event)}


async def _run_agent_async(run_id: str, user_query: str, user_id: str, session_id: str) -> None:
    # A fresh InMemorySessionService per task run is fine here: the task is
    # short-lived (one chat turn) and the session_id/user_id you pass in
    # scope it. If you later want multi-turn memory across separate runs,
    # swap this for ADK's DatabaseSessionService pointed at the same Postgres DB.
    session_service = InMemorySessionService()

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,  # <- was missing before; Runner
        # silently used its own default service otherwise, disconnected
        # from the session you create below.
    )

    if not session_id:
        session_id = str(uuid4())
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    content = types.Content(role="user", parts=[types.Part(text=user_query)])

    seq = 0
    from loguru import logger
    try:
        logger.info(f"Running agent for run_id: {run_id}")
        try:
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content,
            ):
                seq += 1
                await db.append_event(run_id, seq, "agent_event", _event_to_dict(event))

            seq += 1
            await db.append_event(run_id, seq, "done", {"message": "run complete"})
        except Exception as exc:
            logger.error(f"Error running agent for run_id: {run_id} - {str(exc)}")
            await db.append_event(run_id, seq, "error", {"error": str(exc)})

    except Exception as exc:  # noqa: BLE001 — we want to persist *any* failure
        seq += 1
        await db.append_event(run_id, seq, "error", {"error": str(exc)})


@celery_app.task(name="run_agent_task")
def run_agent_task(run_id: str, user_query: str, user_id: str, session_id: str) -> None:
    asyncio.run(_run_agent_async(run_id, user_query, user_id, session_id))