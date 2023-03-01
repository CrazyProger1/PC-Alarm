import functools
import aiogram

from typing import Generator, Optional
from aiogram import types
from app.utils.cls import SingletonMeta
from app.database import Users


class Middleware(metaclass=SingletonMeta):
    def __init__(self, bot: aiogram.Bot):
        self.bot = bot

    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        return await method(message_or_callback, **kwargs)


class Permission(metaclass=SingletonMeta):
    def __init__(self, bot: aiogram.Bot):
        self.bot = bot

    async def __call__(self, page: "Page", message_or_callback: types.Message | types.CallbackQuery, **kwargs) -> bool:
        return True


class Page(metaclass=SingletonMeta):
    permission_classes: tuple[type[Permission]] = ()
    default: bool = False
    path: str = ''

    def __init__(self, bot: aiogram.Bot = None):
        self.bot = bot

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

    async def on_initialize(self, user: Users):
        pass

    async def on_destroy(self, user: Users):
        pass

    async def on_message(self, message: types.Message, user: Users, **kwargs):
        pass

    async def on_callback(self, callback: types.CallbackQuery, user: Users, **kwargs):
        pass

    async def on_media(self, message: types.Message, user: Users, **kwargs):
        pass

    async def on_command(self, message: types.Message, user: Users, **kwargs):
        pass
