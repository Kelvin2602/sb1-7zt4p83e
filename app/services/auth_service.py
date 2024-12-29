from ..database import supabase
from ..models.user import User, UserRole

class AuthService:
    async def get_user_role(self, user_id: str) -> UserRole:
        result = supabase.table('profiles')\
            .select('role')\
            .eq('id', user_id)\
            .single()\
            .execute()
        return UserRole(result.data.get('role', UserRole.USER))

    async def is_admin(self, user_id: str) -> bool:
        role = await self.get_user_role(user_id)
        return role == UserRole.ADMIN