from app.database import Users, Categories
from app.settings import settings
from .types import Permission


class IsNotBanned(Permission):
    message_key = r'You are banned'

    async def __call__(self, page, message_or_callback, **kwargs) -> bool:
        user: Users = kwargs.get('user')
        return not user.is_banned()


class IsOwnerOrAdminOrHigher(Permission):
    message_key = r"You don't have access to this action! If you are the owner of this computer, ask the " \
                  f"<a href='tg://user?id={settings.BOT.ADMIN}'>administrator</a> to add you!"

    def __init__(self, *args, **kwargs):
        super(IsOwnerOrAdminOrHigher, self).__init__(*args, **kwargs)

        self.owner_access_level = Categories.get_owner().access_level

    async def __call__(self, page, message_or_callback, **kwargs) -> bool:
        user: Users = kwargs.get('user')
        return user.category.access_level >= self.owner_access_level


class IsAdmin(Permission):
    message_key = 'This action is available only for administrator!'

    async def __call__(self, page, message_or_callback, **kwargs) -> bool:
        user: Users = kwargs.get('user')
        return user.is_admin()
