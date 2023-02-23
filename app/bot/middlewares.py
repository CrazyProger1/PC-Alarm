import aiogram

from aiogram import types
from app.utils.cls import SingletonMeta


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
    pass


class PermissionMiddleware(Middleware):
    pass
