import os
import playsound
import pyautogui
import asyncio
import cv2
import pyttsx3
import gtts
import winsound

from pathlib import Path
from aiogram import types
from app.bot.types import Executor, Command
from app.database import Users, Languages
from app.utils import logging, threads, filesystem
from app.utils.translator import _
from app.bot.router import Router
from app.bot.pages import SayPage, MusicPage, BeepPage, LanguagePage


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
        await self.sender.send_message_to_all('Alarm Turned ON')
        self._alarm_activated = True

        mouse_pos = pyautogui.position()

        while self._alarm_activated:
            logging.logger.debug('Alarm check')
            await asyncio.sleep(5)
            new_pos = pyautogui.position()
            if new_pos != mouse_pos:
                await self.sender.send_message_to_all('ALARM')
            mouse_pos = new_pos

    async def turn_off_alarm(self):
        logging.logger.debug('Alarm turned off')
        await self.sender.send_message_to_all('Alarm Turned OFF')
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
        path = Path(filesystem.safe_filename('.png', 'photo'))
        self._threaded_make_photo(str(path))

        while not path.exists():
            await asyncio.sleep(1)
        await self.sender.send_photo(user, str(path))
        os.remove(path)

    async def make_screenshot(self, user: Users):
        path = filesystem.safe_filename('.png', 'screenshot')
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        logging.logger.debug(f'Screenshot saved to {path}')
        await self.sender.send_photo(user, path)
        os.remove(path)

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        await getattr(self, f'make_{command.command}')(user)


class PowerCommandsExecutor(Executor):
    commands = (
        'shutdown',
        'restart',
        'end_session'
    )

    async def shutdown(self, user: Users):
        logging.logger.debug('Shutting down...')
        await self.sender.send_message(user, _('Shutting down...'))

    async def restart(self, user: Users):
        logging.logger.debug('Restarting...')
        await self.sender.send_message(user, _('Restarting...'))

    async def end_session(self, user: Users):
        logging.logger.debug('Ending session...')
        await self.sender.send_message(user, _('Ending session...'))

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        await getattr(self, command.command)(user)


class SoundCommandsExecutor(Executor):
    commands = (
        'say',
        'music',
        'beep'
    )

    def __init__(self, *args, **kwargs):
        super(SoundCommandsExecutor, self).__init__(*args, **kwargs)
        self.engine = pyttsx3.init()

    @threads.thread
    def _play_sound(self, sound_path: str):
        filename, ext = os.path.splitext(sound_path)

        if ext == '.ogg':
            mp3_path = f'{filename}.mp3'
            convert_command = f'ffmpeg -i {filename}.ogg -vn -af "volume=20" -ar 44100 -ac 2 {mp3_path} -loglevel quiet'
            os.system(convert_command)
            playsound.playsound(mp3_path)
            os.remove(mp3_path)
        elif ext == '.mp3':
            playsound.playsound(sound_path)

        os.remove(sound_path)

    async def say(self, command: Command, user: Users):
        try:
            audio = gtts.gTTS(text=command.params[0], lang=user.language.short_name, slow=False)
        except IndexError:
            return await Router().set_page(user, SayPage.path)
        path = filesystem.safe_filename('.mp3', 'sound')
        audio.save(path)
        self._play_sound(path)
        while Path(path).exists():
            await asyncio.sleep(1)
        await self.sender.send_message(user, _('Said'))

    async def music(self, command: Command, user: Users):
        try:
            path = command.params[0]
        except IndexError:
            return await Router().set_page(user, MusicPage.path)
        self._play_sound(path)
        while Path(path).exists():
            await asyncio.sleep(1)
        await self.sender.send_message(user, _('Played'))

    @threads.thread
    def _threaded_beep(self, freq: int, duration: int):
        winsound.Beep(freq, duration)

    async def beep(self, command: Command, user: Users):
        try:
            freq = command.params[0]
        except IndexError:
            return await Router().set_page(user, BeepPage.path)
        duration_mcs = 5000
        try:
            if len(command.params) > 1:
                duration_mcs = int(command.params[1])
        except ValueError:
            pass

        self._threaded_beep(freq, 5000)
        await asyncio.sleep(duration_mcs / 1000)
        await self.sender.send_message(user, _('Beep played'))

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        await getattr(self, command.command)(command, user)


class SetCommandExecutor(Executor):
    commands = (
        'set',
    )

    async def set_language(self, user: Users, language_id: str):
        try:
            user.language = Languages.get_by_id(language_id)
            logging.logger.debug(f'User {user} changed language to {user.language.short_name}')
            await self.sender.send_message(
                user,
                _('Language changed', user=user)
            )
        except Languages.DoesNotExist:
            raise 'Wrong ID'

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        if len(command.params) < 2:
            raise

        target = command.params[0]
        value = command.params[1]

        match target:
            case 'language':
                await self.set_language(user, value)
