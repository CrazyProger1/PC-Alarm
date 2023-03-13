import functools
import shlex
import aiogram

from dataclasses import dataclass
from typing import Optional, Callable, Coroutine
from aiogram import types

from app.bot import events, enums
from app.database import Users, Languages
from app.settings import settings
from app.utils import cls as cls_tools, string, event, logging
from app.utils.translator import _

from .sender import Sender


class Middleware(metaclass=cls_tools.SingletonMeta):
    def __init__(self, bot: aiogram.Bot):
        self.bot = bot

    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        return await method(message_or_callback, **kwargs)


class Permission(metaclass=cls_tools.SingletonMeta):
    message_key: str

    def __init__(self, bot: aiogram.Bot):
        self.bot = bot

    async def __call__(self,
                       page: "Page",
                       message_or_callback: types.Message | types.CallbackQuery,
                       content_type: enums.ContentType,
                       **kwargs) -> bool:
        return True


@dataclass
class Command:
    command: str
    args: tuple


class Parser(cls_tools.Customizable, metaclass=cls_tools.SingletonMeta):
    cls_path = settings.COMMAND.PARSER_CLASS

    def parse(self, message: types.Message) -> Command:
        command, *params = shlex.split(message.text.removeprefix(settings.COMMAND.PREFIX))
        return Command(command, params)


class Executor(metaclass=cls_tools.SingletonMeta):
    commands: tuple[str] = ()

    def __init__(self,
                 bot: aiogram.Bot = None):
        self.bot = bot
        self.sender = Sender()

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        pass

    @classmethod
    @functools.cache
    def _cached_get(cls, command: str):
        for subcls in cls.__subclasses__():
            if command in subcls.commands:
                return subcls()

    @classmethod
    def get(cls, command: Command) -> "Executor":
        return cls._cached_get(command.command)


class Keyboard(event.EventEmitter, metaclass=cls_tools.SingletonMeta):
    button_keys: tuple[str] = []
    caption_key: str

    def __init__(self, bot: aiogram.Bot):
        self.bot = bot
        self._active_for_users = []
        self.sender = Sender()
        super(Keyboard, self).__init__()

    @functools.cache
    def get_caption(self, language: Languages):
        return _(self.caption_key, language=language)

    @functools.cache
    def get_button_keys(self) -> tuple[str]:
        return self.button_keys

    @functools.cache
    def get_button_text_translation(self, key: str, language: Languages):
        return _(key, language=language)

    @functools.cache
    def get_buttons(self) -> list[types.KeyboardButton | types.InlineKeyboardButton]:
        pass

    @functools.cache
    def get_markup(self, language: Languages) -> types.ReplyKeyboardMarkup | types.InlineKeyboardMarkup:
        pass

    @functools.cache
    def get_translation_key_pairs(self, language: Languages) -> dict[str, str]:
        result = {}
        for button_key in self.get_button_keys():
            translated = self.get_button_text_translation(button_key, language=language)
            result.update({
                translated: button_key
            })
        return result

    @functools.cache
    def get_pressed(self, text: str, language: Languages) -> str | None:
        return self.get_translation_key_pairs(language=language).get(text)

    def is_active(self, user: Users):
        return user in self._active_for_users

    async def show(self, user: Users):
        self._active_for_users.append(user)

    async def hide(self, user: Users):
        try:
            self._active_for_users.remove(user)
        except ValueError:
            pass

    async def check_pressed(self, *args, **kwargs):
        pass


class ReplyKeyboard(Keyboard):
    row_width: int = 1

    @functools.cache
    def get_buttons(self, language: Languages) -> list[list[types.KeyboardButton | types.InlineKeyboardButton]]:
        result, row = [], []
        for button_key in self.get_button_keys():
            if len(row) == self.row_width:
                result.append(row)
                row = []

            translated = self.get_button_text_translation(button_key, language=language)
            row.append(types.KeyboardButton(translated))

        if len(row) > 0:
            result.append(row)
        return result

    @functools.cache
    def get_markup(self, language: Languages) -> types.ReplyKeyboardMarkup | types.InlineKeyboardMarkup:
        return types.ReplyKeyboardMarkup(
            self.get_buttons(language=language),
            row_width=self.row_width
        )

    async def show(self, user: Users):
        markup = self.get_markup(language=user.language)
        await super(ReplyKeyboard, self).show(user)
        msg = await self.sender.send_message(
            user,
            self.get_caption(language=user.language),
            reply_markup=markup
        )
        user.state.reply_keyboard_msg_id = msg.message_id

    async def hide(self, user: Users):
        msgid = user.state.reply_keyboard_msg_id
        if msgid:
            await self.bot.delete_message(user.id, msgid)
            await super(ReplyKeyboard, self).hide(user)

    async def check_pressed(self, message: types.Message, user: Users, **kwargs):
        button_key = self.get_pressed(message.text, user.language)
        if button_key:
            await self._call(
                events.BUTTON_CLICKED,
                button=button_key,
                user=user,
                message=message
            )


class InlineKeyboard(Keyboard):
    row_width: int = 1
    callback_data_length: int = 30

    @functools.cache
    def get_buttons(self, language: Languages) -> list[list[types.KeyboardButton | types.InlineKeyboardButton]]:
        result, row = [], []
        for button_key in self.get_button_keys():
            if len(row) == self.row_width:
                result.append(row)
                row = []

            translated = self.get_button_text_translation(button_key, language=language)
            row.append(types.InlineKeyboardButton(translated, callback_data=translated[:self.callback_data_length]))

        if len(row) > 0:
            result.append(row)
        return result

    @functools.cache
    def get_markup(self, language: Languages) -> types.ReplyKeyboardMarkup | types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup(
            row_width=self.row_width
        )
        for btn_row in self.get_buttons(language=language):
            markup.add(*btn_row)
        return markup

    async def show(self, user: Users):
        markup = self.get_markup(language=user.language)
        await super(InlineKeyboard, self).show(user)
        msg = await self.sender.send_message(
            user,
            self.get_caption(language=user.language),
            reply_markup=markup
        )
        user.state.inline_keyboard_msg_id = msg.message_id

    async def hide(self, user: Users):
        msgid = user.state.inline_keyboard_msg_id
        if msgid:
            await self.bot.delete_message(user.id, msgid)
            await super(InlineKeyboard, self).hide(user)

    @functools.cache
    def get_pressed(self, text: str, language: Languages) -> str | None:
        return self.get_translation_key_pairs(language=language).get(text[:self.callback_data_length])

    async def check_pressed(self, callback: types.CallbackQuery, user: Users, **kwargs):
        button_key = self.get_pressed(callback.data, user.language)
        if button_key:
            await self._call(
                events.BUTTON_CLICKED,
                button=button_key,
                user=user,
                callback=callback
            )


class Page(event.EventEmitter, metaclass=cls_tools.SingletonMeta):
    permission_classes: tuple[type[Permission]] = ()
    keyboard_classes: tuple[type[Keyboard]] = ()
    default: bool = False
    path: str = ''

    def __init__(self,
                 bot: aiogram.Bot = None,
                 set_page_callback=None):
        self.bot = bot

        self._set_page_callback = set_page_callback
        self._command_parser = Parser()
        self.keyboards = tuple(keyboard_cls(self.bot) for keyboard_cls in self.keyboard_classes)
        self.sender = Sender()

        self._init_executors()
        self._bind_callbacks()
        super(Page, self).__init__()

    def _init_executors(self):
        for executor_cls in Executor.__subclasses__():
            executor_cls(bot=self.bot)

    def _bind_callbacks(self):
        for keyboard in self.keyboards:
            keyboard.add_callback(events.BUTTON_CLICKED, self.handle_button_click)

    @functools.cached_property
    def reply_keyboards(self):
        return tuple(filter(lambda kb: isinstance(kb, ReplyKeyboard), self.keyboards))

    @functools.cached_property
    def inline_keyboards(self):
        return tuple(filter(lambda kb: isinstance(kb, InlineKeyboard), self.keyboards))

    async def show_keyboard(self, user: Users, keyboard: type[Keyboard]):
        if keyboard in self.keyboard_classes:
            await self.keyboards[self.keyboard_classes.index(keyboard)].show(user)

    async def hide_keyboard(self, user: Users, keyboard: type[Keyboard]):
        if keyboard in self.keyboard_classes:
            await self.keyboards[self.keyboard_classes.index(keyboard)].hide(user)

    @classmethod
    @functools.cache
    def get_default(cls) -> Optional[type["Page"]]:
        for page in cls_tools.iter_subclasses(cls):
            if page.default:
                return page

    @classmethod
    @functools.cache
    def get(cls, path: str) -> Optional[type["Page"]]:
        for page in cls_tools.iter_subclasses(cls):
            if page.path == path:
                return page

    async def back(self, user: Users):
        try:
            prev_page, _ = self.path.rsplit('.', 1)
            await self._set_page_callback(user, prev_page)
        except ValueError:
            pass

    async def next(self, user: Users, page: any):
        if isinstance(page, str):
            try:
                await self._set_page_callback(
                    user,
                    string.join_by(self.path, page)
                )
            except ValueError:
                await self._set_page_callback(
                    user,
                    string.join_by(page)
                )
            return
        await self._set_page_callback(
            user,
            page
        )

    async def _execute_command(self, message: types.Message, user: Users, **kwargs):
        command = self._command_parser.parse(
            message=message
        )
        logging.logger.debug(f'Command got: {command}')

        executor = Executor.get(command)

        if executor:
            await executor.execute(command, message, user, **kwargs)

    async def initialize(self, user: Users):
        await self._call(events.INIT, user=user)

    async def destroy(self, user: Users):
        await self._call(events.DESTROY, user=user)

    async def handle_message(self, message: types.Message, user: Users, **kwargs):
        await self._call(events.MESSAGE, message=message, user=user, **kwargs)

        for keyboard in self.reply_keyboards:
            if keyboard.is_active(user):
                await keyboard.check_pressed(
                    message=message,
                    user=user,
                    **kwargs
                )

    async def handle_callback(self, callback: types.CallbackQuery, user: Users, **kwargs):
        await self._call(events.CALLBACK, callback=callback, user=user, **kwargs)

        for keyboard in self.inline_keyboards:
            if keyboard.is_active(user):
                await keyboard.check_pressed(
                    callback=callback,
                    user=user,
                    **kwargs
                )

    async def handle_media(self, message: types.Message, user: Users, **kwargs):
        await self._call(events.MEDIA, message=message, user=user, **kwargs)

    async def handle_command(self, message: types.Message, user: Users, **kwargs):
        await self._call(events.COMMAND, message=message, user=user, **kwargs)
        await self._execute_command(message, user, **kwargs)

    async def handle_button_click(self, keyboard: Keyboard, **kwargs):
        await self._call(events.BUTTON_CLICKED, keyboard=keyboard, **kwargs)

    def __repr__(self):
        return self.path
