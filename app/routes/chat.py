from fastapi import APIRouter, HTTPException, Depends
from ..models.message import Message
from ..services.chat_service import ChatService
from ..services.auth_service import AuthService

router = APIRouter()
chat_service = ChatService()
auth_service = AuthService()

@router.get("/messages/{room_id}")
async def get_room_messages(room_id: str):
    try:
        return await chat_service.get_room_messages(room_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/messages/{message_id}")
async def delete_message(message_id: str):
    try:
        return await chat_service.delete_message(message_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))