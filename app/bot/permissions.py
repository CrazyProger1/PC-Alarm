from app.database import Users
from .types import Permission


class IsNotBanned(Permission):
    async def __call__(self, page, message_or_callback, **kwargs) -> bool:
        user: Users = kwargs.get('user')
        return not user.is_banned()
