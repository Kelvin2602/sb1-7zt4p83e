from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Message(BaseModel):
    content: str
    room_id: str
    sender_id: str
    created_at: Optional[datetime] = None