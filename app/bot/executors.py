import os
import pyautogui
import asyncio
import random
import cv2

from pathlib import Path
from aiogram import types
from app.bot.types import Executor, Command
from app.database import Users
from app.utils import logging, threads
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


class PhotoCommandsExecutor(Executor):
    commands = (
        'photo',
        'screenshot'
    )

    @threads.thread
    def _threaded_make_photo(self, path: str):
        webcam = cv2.VideoCapture(0)
        check, frame = webcam.read()
        cv2.imwrite(filename=path, img=frame)
        logging.logger.debug(f'Photo saved to {path}')

    async def make_photo(self, user: Users):
        path = Path(f'photo{random.randint(1, 1000000000)}.png')
        self._threaded_make_photo(str(path))

        while not path.exists():
            await asyncio.sleep(1)
        await self.sender.send_photo(user, str(path))
        os.remove(path)

    async def make_screenshot(self, user: Users):
        path = f'screenshot{random.randint(1, 1000000000)}.png'
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        logging.logger.debug(f'Screenshot saved to {path}')
        await self.sender.send_photo(user, path)
        os.remove(path)

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        await getattr(self, f'make_{command.command}')(user)
