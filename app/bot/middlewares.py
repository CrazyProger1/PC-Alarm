import aiogram

from aiogram import types
from app.utils.cls import SingletonMeta
from app.database.authenticator import Authenticator


class Middleware(metaclass=SingletonMeta):
    def __init__(self, bot: aiogram.Bot):
        self.bot = bot

    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        return await method(message_or_callback, **kwargs)


class ErrorCatchingMiddleware(Middleware):
    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        try:
            return await method(message_or_callback, **kwargs)
        except Exception as e:
            print(e)
            raise


class AuthMiddleware(Middleware):
    def __init__(self, *args, **kwargs):
        super(AuthMiddleware, self).__init__(*args, **kwargs)
        self.authenticator = Authenticator()

    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        user = self.authenticator.authenticate(message_or_callback.from_user)
        return await method(message_or_callback, user=user, **kwargs)


class PermissionMiddleware(Middleware):
    pass
