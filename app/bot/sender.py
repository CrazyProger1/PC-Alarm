import aiogram

from aiogram import types
from app.database import Users
from app.settings import settings
from app.utils import cls


class Sender(metaclass=cls.SingletonMeta):
    def __init__(self, bot: aiogram.Bot = None):
        self.bot = bot

    async def send_message(self, user: Users, text: str = '', **kwargs) -> types.Message:
        return await self.bot.send_message(
            user.id,
            text,
            **kwargs,
            parse_mode=settings.MESSAGES.PARSE_MODE
        )

    async def send_message_to_all(self, text: str, **kwargs) -> list[types.Message]:
        result = []
        for user in Users.select():
            result.append(await self.send_message(user, text, **kwargs))

        return result

    async def send_photo(self, user: Users, path: str, **kwargs) -> types.Message:
        with open(path, 'rb') as f:
            return await self.bot.send_photo(
                user.id,
                f,
                **kwargs
            )
