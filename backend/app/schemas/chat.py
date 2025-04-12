from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class ChatMessageBase(BaseModel):
    content: str
    message_type: str


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessage(ChatMessageBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ChatResponse(BaseModel):
    content: str
    message_type: str
