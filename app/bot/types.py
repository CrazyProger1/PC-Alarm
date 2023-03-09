import functools
import shlex
import aiogram

from dataclasses import dataclass
from typing import Optional, Callable
from aiogram import types

from app.bot import events, enums
from app.database import Users, Languages
from app.settings import settings
from app.utils import cls as cls_tools, string, event
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
    params: list


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
    buttons: list[str] = []
    caption_key: str

    def __init__(self, bot: aiogram.Bot):
        self.bot = bot
        self._active_for_users = []
        self._sender = Sender()
        super(Keyboard, self).__init__()

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

    def __init__(self, *args, **kwargs):
        self._markups = {}
        self._translations = {}
        super(ReplyKeyboard, self).__init__(*args, **kwargs)
        self._setup_markups()

    def _get_buttons(self, language: Languages) -> list[list[types.KeyboardButton]]:
        self._translations[language.short_name] = {}
        result = []
        width = 0
        row = []
        for button_key in self.buttons:
            if width == self.row_width:
                width = 0
                row = []
                result.append(row)
            width += 1
            translated = _(button_key, language=language)
            row.append(
                types.KeyboardButton(translated)
            )
            self._translations[language.short_name].update({translated: button_key})

        if len(row) > 0:
            result.append(row)
        return result

    def _setup_markups(self):
        for language in Languages.select():
            markup = types.ReplyKeyboardMarkup(
                self._get_buttons(language),
                row_width=self.row_width
            )
            self._markups.update({language.short_name: markup})

    async def show(self, user: Users):
        markup = self._markups.get(user.language.short_name)
        await super(ReplyKeyboard, self).show(user)
        msg = await self._sender.send_message(
            user,
            _(self.caption_key, user=user),
            reply_markup=markup
        )
        user.state.reply_keyboard_msg_id = msg.message_id

    async def hide(self, user: Users):
        msgid = user.state.reply_keyboard_msg_id
        if msgid:
            await self.bot.delete_message(user.id, msgid)
            await super(ReplyKeyboard, self).hide(user)

    async def check_pressed(self, message: types.Message, user: Users, **kwargs):
        translations = self._translations.get(user.language.short_name)

        button_key = translations.get(message.text)

        if button_key:
            await self._call(
                events.BUTTON_CLICKED,
                button=button_key,
                user=user,
                message=message
            )


class InlineKeyboard(Keyboard):
    row_width: int

    def __init__(self, *args, **kwargs):
        super(InlineKeyboard, self).__init__(*args, **kwargs)

    async def show(self, user: Users):
        await super(InlineKeyboard, self).show(user)

    async def hide(self, user: Users):
        await super(InlineKeyboard, self).hide(user)

    async def check_pressed(self, *args, **kwargs):
        pass


class Page(event.EventEmitter, metaclass=cls_tools.SingletonMeta):
    permission_classes: tuple[type[Permission]] = ()
    keyboard_classes: tuple[type[Keyboard]] = ()
    default: bool = False
    path: str = ''

    def __init__(self,
                 bot: aiogram.Bot = None,
                 set_page_callback: Callable[[Users, any], None] = None):
        self.bot = bot

        self._set_page_callback = set_page_callback
        self._command_parser = Parser()
        self._keyboards = tuple(keyboard_cls(self.bot) for keyboard_cls in self.keyboard_classes)
        self._sender = Sender()

        self._init_executors()
        self._bind_callbacks()
        super(Page, self).__init__()

    def _init_executors(self):
        for executor_cls in Executor.__subclasses__():
            executor_cls(bot=self.bot)

    def _bind_callbacks(self):
        for keyboard in self._keyboards:
            keyboard.add_callback(events.BUTTON_CLICKED, self.handle_button_click)

    @functools.cached_property
    def reply_keyboards(self):
        return tuple(filter(lambda kb: isinstance(kb, ReplyKeyboard), self._keyboards))

    @functools.cached_property
    def inline_keyboards(self):
        return tuple(filter(lambda kb: isinstance(kb, InlineKeyboard), self._keyboards))

    async def show_keyboard(self, user: Users, keyboard: type[Keyboard]):
        if keyboard in self.keyboard_classes:
            await self._keyboards[self.keyboard_classes.index(keyboard)].show(user)

    async def hide_keyboard(self, user: Users, keyboard: type[Keyboard]):
        if keyboard in self.keyboard_classes:
            await self._keyboards[self.keyboard_classes.index(keyboard)].hide(user)

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
            self._set_page_callback(user, prev_page)
        except ValueError:
            pass

    async def next(self, user: Users, page: any):
        if isinstance(page, str):
            try:
                self._set_page_callback(
                    user,
                    string.join_by(self.path, page)
                )
            except ValueError:
                self._set_page_callback(
                    user,
                    string.join_by(page)
                )
            return
        self._set_page_callback(
            user,
            page
        )

    async def _execute_command(self, message: types.Message, user: Users, **kwargs):
        command = self._command_parser.parse(
            message=message
        )
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
