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
from app.database import Users, Languages, Categories
from app.utils import logging, threads, filesystem
from app.utils.translator import _
from app.bot.router import Router
from app.bot.pages import SayPage, MusicPage, BeepPage, LanguagePage, OwnerAddingPage
from app.exceptions import *


class BaseCommandsExecutor(Executor):
    commands = (
        'help',
        'start'
    )

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        await self.sender.send_message(user, _('Welcome, {first_name}!', user=user).format(first_name=user.first_name))


class AlarmCommandsExecutor(Executor):
    commands = (
        'turn_on_alarm',
        'turn_off_alarm'
    )

    def __init__(self, *args, **kwargs):
        super(AlarmCommandsExecutor, self).__init__(*args, **kwargs)
        self._alarm_active = False

    async def turn_on_alarm(self):
        logging.logger.debug('Alarm turned on')
        await self.sender.send_message_to_all('Alarm Turned ON')
        self._alarm_active = True

        mouse_pos = pyautogui.position()

        while self._alarm_active:
            logging.logger.debug('Alarm check')
            await asyncio.sleep(5)
            new_pos = pyautogui.position()
            if new_pos != mouse_pos:
                await self.sender.send_message_to_all('ALARM')
            mouse_pos = new_pos

    async def turn_off_alarm(self):
        logging.logger.debug('Alarm turned off')
        await self.sender.send_message_to_all('Alarm Turned OFF')
        self._alarm_active = False

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
        await self.sender.send_message(user, _('Shutting down...', user=user))
        os.system('shutdown /s /f /t 0')

    async def restart(self, user: Users):
        logging.logger.debug('Restarting...')
        await self.sender.send_message(user, _('Restarting...', user=user))
        os.system('shutdown /r /f /t 0')

    async def end_session(self, user: Users):
        logging.logger.debug('Ending session...')
        await self.sender.send_message(user, _('Ending session...', user=user))
        os.system('shutdown /l /f')

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
    def _play_sound(self, sound_path: Path):
        filename, ext = sound_path.stem, sound_path.suffix
        string_path = str(sound_path)

        if ext == '.ogg':
            mp3_path = f'{filename}.mp3'
            convert_command = f'ffmpeg -i {filename}.ogg -vn -af "volume=20" -ar 44100 -ac 2 {mp3_path} -loglevel quiet'
            os.system(convert_command)
            playsound.playsound(mp3_path)
            os.remove(mp3_path)
        elif ext == '.mp3':
            playsound.playsound(string_path)

        os.remove(string_path)

    async def say(self, command: Command, user: Users):
        try:
            audio = gtts.gTTS(text=command.args[0], lang=user.language.short_name, slow=False)
        except IndexError:
            return await Router().set_page(user, SayPage.path)

        path = Path(filesystem.safe_filename('.mp3', 'sound'))

        audio.save(str(path))

        self._play_sound(path)

        while path.exists():
            await asyncio.sleep(1)

        await self.sender.send_message(user, _('Said', user=user))

    async def music(self, command: Command, user: Users):
        try:
            path = Path(command.args[0])
            if not path.exists():
                raise FileDoesNotExists(user, str(path))

        except IndexError:
            return await Router().set_page(user, MusicPage.path)

        self._play_sound(path)

        while Path(path).exists():
            await asyncio.sleep(1)

        await self.sender.send_message(user, _('Played', user=user))

    @threads.thread
    def _threaded_beep(self, freq: int, duration: int):
        winsound.Beep(freq, duration)

    async def beep(self, command: Command, user: Users):
        try:
            freq = command.args[0]

            if not 37 <= freq <= 32767:
                raise BotInteractionError(
                    user,
                    _('Wrong frequency value! It must be in the range from 37 to 32767',
                      user=user)
                )

        except IndexError:
            return await Router().set_page(user, BeepPage.path)

        duration_mcs = 5000

        try:
            if len(command.args) > 1:
                duration_mcs = int(command.args[1])
        except ValueError:
            pass

        self._threaded_beep(freq, 5000)
        await asyncio.sleep(duration_mcs / 1000)
        await self.sender.send_message(user, _('Beep played', user=user))

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        await getattr(self, command.command)(command, user)


class SetCommandExecutor(Executor):
    commands = (
        'set',
    )

    async def set_language(self, user: Users, language_id: str):
        try:
            user.language = Languages.get_by_id(language_id)
            user.save()
            logging.logger.debug(f'User {user} changed language to {user.language.short_name}')
            await self.sender.send_message(
                user,
                _('Language changed', user=user)
            )
            await Router.reload_page(user)
        except Languages.DoesNotExist:
            raise BotInteractionError(user, _('This language is not available yet', user=user))

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        args_number = len(command.args)
        if args_number < 2:
            raise MissingArgumentsError(user, ('target', 'value')[args_number:])

        target = command.args[0]
        value = command.args[1]

        match target:
            case 'language':
                await self.set_language(user, value)
            case _:
                raise TargetNotExistsError(user, target)


class AddOwnerCommandExecutor(Executor):
    commands = (
        'add_owner',
    )

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        try:
            username = command.args[0]
        except IndexError:
            return await Router().set_page(user, OwnerAddingPage.path)

        if username.startswith('@'):
            username = username.removeprefix('@')

        try:
            user2 = Users.get(username=username)
        except Users.DoesNotExist:
            raise BotInteractionError(user, _('This user is not in the database', user=user))

        user2.category = Categories.get_owner()
        user2.save()
        await self.sender.send_message(user, _('The user has been added to the owners group', user=user))
