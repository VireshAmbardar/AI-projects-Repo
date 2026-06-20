

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from uuid import UUID


class ChatInput(BaseModel):
    """Holds actions details as per database and user defined values."""

    user_message: str

class RunId(BaseModel):
    """Holds actions details as per database and user defined values."""

    run_id: str

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)