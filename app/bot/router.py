import aiogram

from app.database import Users
from app.utils.cls import SingletonMeta
from .types import Page


class Router(metaclass=SingletonMeta):
    def __init__(self, bot: aiogram.Bot):
        self._bot = bot

        for page in Page.iter_subpages():
            page(bot=self._bot)

    @staticmethod
    async def get_page(user: Users) -> Page:
        page = user.state.page
        if not page:
            await Router.set_page(user, Page.get_default())
            page = user.state.page

        return page

    @staticmethod
    async def set_page(user: Users, page: str | Page | type[Page]):
        old_page: Page = user.state.page
        new_page: Page | None = None

        if isinstance(page, str):
            new_page = Page.get(page)
        elif isinstance(page, Page):
            new_page = page
        elif issubclass(page, Page):
            new_page = page()

        if not new_page:
            raise ValueError(f'Page not found: {page}')

        if old_page != new_page:
            if old_page:
                await old_page.on_destroy(user)
            user.state.page = new_page
            await new_page.on_initialize(user)

    async def route_callback(self, *args, **kwargs):
        page = await self.get_page(kwargs.get('user'))
        await page.on_callback(*args, **kwargs)

    async def route_message(self, *args, **kwargs):
        page = await self.get_page(kwargs.get('user'))
        await page.on_message(*args, **kwargs)

    async def route_command(self, *args, **kwargs):
        page = await self.get_page(kwargs.get('user'))
        await page.on_command(*args, **kwargs)

    async def route_media(self, *args, **kwargs):
        page = await self.get_page(kwargs.get('user'))
        await page.on_media(*args, **kwargs)
