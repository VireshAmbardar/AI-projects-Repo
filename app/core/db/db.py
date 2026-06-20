"""
Postgres access layer.

Used in two places:
  - FastAPI process: async reads + LISTEN for the SSE endpoint
  - Celery worker: writes new agent events + NOTIFY after each one

We use raw asyncpg rather than an ORM here on purpose — LISTEN/NOTIFY needs a
single dedicated connection (not a pooled one), and for an events table this
thin, an ORM doesn't buy much. Swap in SQLAlchemy later if the schema grows.
"""

import json
from datetime import datetime, timezone
from typing import Any, Optional

import asyncpg

from app.core.settings import settings

NOTIFY_CHANNEL = "agent_events_channel"

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS agent_runs (
    run_id UUID PRIMARY KEY,
    user_id TEXT,
    session_id TEXT,
    query TEXT,
    status TEXT NOT NULL DEFAULT 'pending',  -- pending | running | completed | failed
    error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS agent_events (
    id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES agent_runs(run_id) ON DELETE CASCADE,
    seq INT NOT NULL,
    event_type TEXT NOT NULL,   -- 'agent_event' | 'done' | 'error'
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (run_id, seq)
);

CREATE INDEX IF NOT EXISTS idx_agent_events_run_id_seq ON agent_events (run_id, seq);
"""


async def init_db() -> None:
    """Call once on FastAPI startup (and safe to call from worker boot too)."""
    conn = await asyncpg.connect(settings.database_url)
    try:
        await conn.execute(CREATE_TABLES_SQL)
    finally:
        await conn.close()


async def create_run(run_id: str, user_id: str, session_id: str, query: str) -> None:
    print(settings.database_url)
    conn = await asyncpg.connect(settings.database_url)
    try:
        print()
        await conn.execute(
            """
            INSERT INTO agent_runs (run_id, user_id, session_id, query, status)
            VALUES ($1, $2, $3, $4, 'pending')
            """,
            run_id, user_id, session_id, query,
        )
    finally:
        await conn.close()


async def append_event(run_id: str, seq: int, event_type: str, payload: dict[str, Any]) -> None:
    """Write one event row and NOTIFY listeners. Used by the Celery worker."""
    conn = await asyncpg.connect(settings.database_url)
    try:
        async with conn.transaction():
            await conn.execute(
                """
                INSERT INTO agent_events (run_id, seq, event_type, payload)
                VALUES ($1, $2, $3, $4::jsonb)
                """,
                run_id, seq, event_type, json.dumps(payload),
            )
            if event_type == "done":
                await conn.execute(
                    "UPDATE agent_runs SET status='completed', completed_at=$2 WHERE run_id=$1",
                    run_id, datetime.now(timezone.utc),
                )
            elif event_type == "error":
                await conn.execute(
                    "UPDATE agent_runs SET status='failed', error=$2, completed_at=$3 WHERE run_id=$1",
                    run_id, payload.get("error", "unknown error"), datetime.now(timezone.utc),
                )
            elif event_type == "agent_event":
                await conn.execute(
                    "UPDATE agent_runs SET status='running' WHERE run_id=$1 AND status='pending'",
                    run_id,
                )
        # NOTIFY payload is just the run_id — listeners re-query for new rows,
        # so we never hit Postgres's ~8000 byte NOTIFY payload limit.
        await conn.execute("SELECT pg_notify($1, $2)", NOTIFY_CHANNEL, run_id)
    finally:
        await conn.close()


async def get_run_status(run_id: str) -> Optional[str]:
    conn = await asyncpg.connect(settings.database_url)
    try:
        return await conn.fetchval("SELECT status FROM agent_runs WHERE run_id=$1", run_id)
    finally:
        await conn.close()


async def fetch_events_after(conn: asyncpg.Connection, run_id: str, after_seq: int) -> list[asyncpg.Record]:
    return await conn.fetch(
        "SELECT seq, event_type, payload FROM agent_events WHERE run_id=$1 AND seq > $2 ORDER BY seq",
        run_id, after_seq,
    )