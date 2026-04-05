

from pydantic import BaseModel
from enum import Enum
from uuid import UUID

class Models(str,Enum):
   Llama_3_1_8B = "llama-3.1-8b-instant"
   Lama_3_3_70B = "llama-3.3-70b-versatile"
   GPT_OSS_120B = "openai/gpt-oss-120b"
   GPT_OSS_20B = "openai/gpt-oss-20b"
   


class ChatInput(BaseModel):
   """Holds actions details as per database and user defined values."""
   conversation_id:str
   user_message: str

class ChatResponse(BaseModel):
    conversation_id: str
    response: str