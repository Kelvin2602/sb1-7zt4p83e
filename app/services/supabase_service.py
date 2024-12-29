from ..database import supabase
from ..models.user import User
from ..models.message import Message
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class SupabaseService:
    @staticmethod
    async def get_user_profile(user_id: str) -> Optional[User]:
        try:
            result = supabase.from_('profiles')\
                .select('*')\
                .eq('id', user_id)\
                .single()\
                .execute()
            return User(**result.data) if result.data else None
        except Exception as e:
            logger.error(f"Error fetching user profile: {e}")
            return None

    @staticmethod
    async def create_room(name: str, description: str, created_by: str):
        try:
            result = supabase.from_('rooms')\
                .insert({
                    'name': name,
                    'description': description,
                    'created_by': created_by
                })\
                .execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Error creating room: {e}")
            raise

    @staticmethod
    async def join_room(room_id: str, user_id: str):
        try:
            result = supabase.from_('room_members')\
                .insert({
                    'room_id': room_id,
                    'user_id': user_id
                })\
                .execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Error joining room: {e}")
            raise

    @staticmethod
    async def get_room_messages(room_id: str) -> List[Message]:
        try:
            result = supabase.from_('messages')\
                .select('*, profiles:sender_id(full_name, avatar_url)')\
                .eq('room_id', room_id)\
                .order('created_at')\
                .execute()
            return [Message(**msg) for msg in result.data]
        except Exception as e:
            logger.error(f"Error fetching room messages: {e}")
            raise