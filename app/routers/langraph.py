"using alnggraph"

from fastapi import APIRouter
from app.schemas.chat import RunId
from app.schemas.langgraph import LangGraphRequestBody

router = APIRouter(
    prefix="/langgraph",
    tags=["LangGraph"]
)

@router.post("/chat", response_model=RunId)
def langgraph_chat(
    request: LangGraphRequestBody
    ) -> RunId:
    """
    """
    # run 1 main agent

    # return uuid

    from uuid import uuid4
    return RunId(run_id=uuid4())