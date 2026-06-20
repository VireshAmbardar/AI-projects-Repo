from pydantic import BaseModel

class LangGraphRequestBody(BaseModel):
    """Holds actions details as per database and user defined values."""

    user_message: str