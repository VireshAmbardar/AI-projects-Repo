from pydantic import BaseModel, Field
from enum import Enum
from uuid import UUID

class Models(str,Enum):
   Llama_3_1_8B = "llama-3.1-8b-instant"
   Llama_3_3_70B = "llama-3.3-70b-versatile"
   GPT_OSS_120B = "openai/gpt-oss-120b"
   GPT_OSS_20B = "openai/gpt-oss-20b"
   


class ChatInput(BaseModel):
    """Request payload for the human-in-the-loop chat endpoint."""

    conversation_id: str = Field(..., min_length=1, description="Unique conversation ID")
    user_message: str = Field(..., min_length=1, description="User's current message")

class ChatResponse(BaseModel):
    """Response returned by the human-in-the-loop chat endpoint."""

    conversation_id: str
    response: str
    status: str = Field(..., description="Either 'follow_up' or 'completed'")