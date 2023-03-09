import pyautogui
import asyncio

from aiogram import types
from app.bot.types import Executor, Command
from app.database import Users
from app.utils import logging
from app.utils.translator import _


class BaseCommandsExecutor(Executor):
    commands = (
        'help',
        'start'
    )

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        await self.bot.send_message(user.id, command.command)


class AlarmCommandsExecutor(Executor):
    commands = (
        'turn_on_alarm',
        'turn_off_alarm'
    )

    def __init__(self, *args, **kwargs):
        super(AlarmCommandsExecutor, self).__init__(*args, **kwargs)
        self._alarm_activated = False

    async def turn_on_alarm(self):
        logging.logger.debug('Alarm turned on')
        await self.sender.send_message_to_all(_('Alarm Turned ON'))
        self._alarm_activated = True

        mouse_pos = pyautogui.position()

        while self._alarm_activated:
            logging.logger.debug('Alarm check')
            await asyncio.sleep(5)
            new_pos = pyautogui.position()
            if new_pos != mouse_pos:
                await self.sender.send_message_to_all(_('ALARM'))
            mouse_pos = new_pos

    async def turn_off_alarm(self):
        logging.logger.debug('Alarm turned off')
        await self.sender.send_message_to_all(_('Alarm Turned OFF'))
        self._alarm_activated = False

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        await getattr(self, command.command)()
