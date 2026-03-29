

from pydantic import BaseModel


class ChatInput(BaseModel):
    """Holds actions details as per database and user defined values."""

    user_message: str