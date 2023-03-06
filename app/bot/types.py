import functools
import aiogram
import shlex

from typing import Generator, Optional, Callable
from aiogram import types
from dataclasses import dataclass

from app.utils import cls, string, event
from app.database import Users
from app.settings import settings
from app.bot import events, enums


class Middleware(metaclass=cls.SingletonMeta):
    def __init__(self, bot: aiogram.Bot):
        self.bot = bot

    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        return await method(message_or_callback, **kwargs)


class Permission(metaclass=cls.SingletonMeta):
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


class Parser(cls.Customizable, metaclass=cls.SingletonMeta):
    cls_path = settings.COMMAND.PARSER_CLASS

    def parse(self, message: types.Message) -> Command:
        command, *params = shlex.split(message.text.removeprefix(settings.COMMAND.PREFIX))
        return Command(command, params)


class Executor(metaclass=cls.SingletonMeta):
    commands: tuple[str] = ()

    def __init__(self,
                 bot: aiogram.Bot = None):
        self.bot = bot

    async def execute(self, command: Command, message: types.Message, user: Users, **kwargs):
        pass

    @classmethod
    @functools.cache
    def _cache_get(cls, command: str):
        for subcls in cls.__subclasses__():
            if command in subcls.commands:
                return subcls()

    @classmethod
    def get(cls, command: Command) -> "Executor":
        return cls._cache_get(command.command)


class Page(event.EventEmitter, metaclass=cls.SingletonMeta):
    permission_classes: tuple[type[Permission]] = ()
    default: bool = False
    path: str = ''

    def __init__(self,
                 bot: aiogram.Bot = None,
                 set_page_callback: Callable[[Users, any], None] = None):
        self.bot = bot
        self._set_page_callback = set_page_callback
        self._command_parser = Parser()
        self._init_executors()
        super(Page, self).__init__()

    def _init_executors(self):
        for executor_cls in Executor.__subclasses__():
            executor_cls(bot=self.bot)

    @classmethod
    def iter_subpages(cls) -> Generator[type["Page"], None, None]:
        for subpage in cls.__subclasses__():
            yield subpage
            for subsubpage in subpage.iter_subpages():
                yield subsubpage

    @classmethod
    @functools.cache
    def get_default(cls) -> Optional[type["Page"]]:
        for page in cls.iter_subpages():
            if page.default:
                return page

    @classmethod
    @functools.cache
    def get(cls, path: str) -> Optional[type["Page"]]:
        for page in cls.iter_subpages():
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

    async def handle_callback(self, callback: types.CallbackQuery, user: Users, **kwargs):
        await self._call(events.CALLBACK, callback=callback, user=user, **kwargs)

    async def handle_media(self, message: types.Message, user: Users, **kwargs):
        await self._call(events.MEDIA, message=message, user=user, **kwargs)

    async def handle_command(self, message: types.Message, user: Users, **kwargs):
        await self._call(events.COMMAND, message=message, user=user, **kwargs)
        await self._execute_command(message, user, **kwargs)

    def __repr__(self):
        return self.path
