from pydantic import BaseModel, Field


class GoogleADkRequestBody(BaseModel):
    """Body for POST /adk/chat."""

    query: str = Field(..., description="The user's message to the agent")
    user_id: str
    session_id: str