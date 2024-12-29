import socketio
from .services.chat_service import ChatService
from .models.message import Message
from .utils.logger import logger

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=['http://localhost:8000']
)

chat_service = ChatService()

@sio.event
async def connect(sid, environ):
    logger.info(f"Client kết nối: {sid}")

@sio.event
async def disconnect(sid):
    logger.info(f"Client ngắt kết nối: {sid}")

@sio.event
async def join_room(sid, room_id):
    sio.enter_room(sid, room_id)
    logger.info(f"User {sid} tham gia phòng {room_id}")

@sio.event
async def send_message(sid, data):
    try:
        message = Message(
            content=data['message'],
            room_id=data['room'],
            sender_id=data['sender']
        )
        
        saved_message = await chat_service.save_message(message)
        await sio.emit('receive_message', saved_message, room=message.room_id)
    except Exception as e:
        logger.error(f"Lỗi khi lưu tin nhắn: {e}")
        await sio.emit('error', 'Không thể lưu tin nhắn', room=sid)

@sio.event
async def message_deleted(sid, data):
    await sio.emit('message_deleted', data, room=data['roomId'])