"""Schemas for the chat app."""
from pydantic import BaseModel, validator


class ChatResponse(BaseModel):
    """Chat response schema."""
    sender: bool
    message: str
    type: str
    seq_num: int
    seq_complete: bool
    socket_id: str

    @validator("type")
    def validate_message_type(cls, v):
        if v not in ["start", "stream", "end", "error", "info"]:
            raise ValueError("type must be start, stream or end")
        return v
