"""using Google ADK"""

from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.core.db import db
from app.core.celery.celery_app import celery_app
from app.schemas.chat import RunId
from app.schemas.googleadk import GoogleADkRequestBody

router = APIRouter(
    prefix="/adk",
    tags=["Google ADK"],
)


@router.post("/chat", response_model=RunId)
async def adk_chat(request: GoogleADkRequestBody) -> RunId:
    """
    Kicks off one agent run in the background and returns immediately
    with a run_id. Client should open GET /adk/chat/stream/{run_id}
    (see sse_router.py) to receive events as they happen.
    """
    run_id = str(uuid4())

    # Row must exist before we dispatch, so the SSE endpoint never hits a
    # run_id that "doesn't exist yet" due to a race with the worker.

    # Need to run only once to create the tables
    # await db.init_db()

    # for subsequent runs only
    await db.create_run(
        run_id=run_id,
        user_id=request.user_id,
        session_id=request.session_id,
        query=request.query,
    )


    celery_app.send_task(
        "run_agent_task",
        kwargs={
            "run_id": run_id,
            "user_query": request.query,
            "user_id": request.user_id,
            "session_id": request.session_id,
        },
    )

    return RunId(run_id=run_id)


@router.get("/chat/{run_id}/status")
async def adk_chat_status(run_id: str) -> dict:
    status = await db.get_run_status(run_id)
    if status is None:
        raise HTTPException(status_code=404, detail="run_id not found")
    return {"run_id": run_id, "status": status}