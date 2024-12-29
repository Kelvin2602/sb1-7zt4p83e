from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Message(BaseModel):
    content: str = Field(..., description="Nội dung tin nhắn")
    room_id: str = Field(..., description="ID của phòng chat")
    sender_id: str = Field(..., description="ID của người gửi")
    created_at: Optional[datetime] = Field(default=None, description="Thời gian tạo")