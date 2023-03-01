import functools
import aiogram

from typing import Generator, Optional
from aiogram import types
from app.utils.cls import SingletonMeta


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

    @classmethod
    def iter_subpages(cls) -> Generator["Page", None, None]:
        for subpage in cls.__subclasses__():
            yield subpage
            for subsubpage in subpage.iter_subpages():
                yield subsubpage

    @classmethod
    @functools.cache
    def get_default(cls) -> Optional["Page"]:
        for page in cls.iter_subpages():
            if page.default:
                return page

    @classmethod
    @functools.cache
    def get(cls, path: str) -> Optional["Page"]:
        for page in cls.iter_subpages():
            if page.path == path:
                return page
