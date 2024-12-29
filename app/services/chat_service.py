from ..database import supabase
from ..models.message import Message

class ChatService:
    async def get_room_messages(self, room_id: str):
        result = supabase.table('messages')\
            .select('*')\
            .eq('room_id', room_id)\
            .order('created_at')\
            .execute()
        return result.data
    
    async def save_message(self, message: Message):
        result = supabase.table('messages').insert(message.dict()).execute()
        return result.data[0]
        
    async def delete_message(self, message_id: str):
        result = supabase.table('messages')\
            .delete()\
            .eq('id', message_id)\
            .execute()
        return result.data