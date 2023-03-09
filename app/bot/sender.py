import aiogram

from aiogram import types
from app.database import Users
from app.settings import settings
from app.utils import cls


class Sender(metaclass=cls.SingletonMeta):
    def __init__(self, bot: aiogram.Bot = None):
        self.bot = bot

    async def send_message(self, user: Users, text: str, **kwargs) -> types.Message:
        return await self.bot.send_message(
            user.id,
            text,
            **kwargs,
            parse_mode=settings.MESSAGES.PARSE_MODE
        )
