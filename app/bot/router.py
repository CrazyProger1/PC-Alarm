import aiogram

from app.database import Users
from app.utils import logging, cls
from .types import Page


class Router(metaclass=cls.SingletonMeta):
    def __init__(self, bot: aiogram.Bot = None):
        self._bot = bot
        self._init_pages()

    def _init_pages(self):
        for page in cls.iter_subclasses(Page):
            page(
                bot=self._bot,
                set_page_callback=self.set_page
            )

    @staticmethod
    async def get_page(user: Users) -> Page:
        page = user.state.page
        if not page:
            await Router.set_page(user, Page.get_default())
            page = user.state.page

        return page

    @staticmethod
    async def set_page(user: Users, page: str | Page | type[Page], reload: bool = False):
        old_page: Page = user.state.page
        new_page: Page | None = None

        if isinstance(page, str):
            new_page = Page.get(page)()
        elif isinstance(page, Page):
            new_page = page
        elif issubclass(page, Page):
            new_page = page()

        if not new_page:
            raise ValueError(f'Page not found: {page}')

        if old_page != new_page or reload:
            if old_page:
                await old_page.destroy(user)
            user.state.page = new_page
            await new_page.initialize(user)

            if not reload:
                logging.logger.debug(f'User {user} changed page to {new_page}')

    @staticmethod
    async def reload_page(user: Users):
        curr_page = user.state.page
        logging.logger.debug(f'Page {curr_page} reloaded for user {user}')
        await Router.set_page(user, curr_page, reload=True)

    async def route_callback(self, *args, **kwargs):
        page = await self.get_page(kwargs.get('user'))
        await page.handle_callback(*args, **kwargs)

    async def route_message(self, *args, **kwargs):
        page = await self.get_page(kwargs.get('user'))
        await page.handle_message(*args, **kwargs)

    async def route_command(self, *args, **kwargs):
        page = await self.get_page(kwargs.get('user'))
        await page.handle_command(*args, **kwargs)

    async def route_media(self, *args, **kwargs):
        page = await self.get_page(kwargs.get('user'))
        await page.handle_media(*args, **kwargs)
