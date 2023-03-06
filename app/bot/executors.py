from aiogram import types
from app.bot.types import Executor, Command
from app.database import Users


class BaseCommandsExecutor(Executor):
    commands = (
        'help',
        'start'
    )

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        await self.bot.send_message(user.id, command.command)
