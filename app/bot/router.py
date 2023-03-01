import aiogram

from app.database import Users
from .types import Page


class Router:
    def __init__(self, bot: aiogram.Bot):
        self._bot = bot

    @staticmethod
    async def get_page(user: Users) -> Page:
        page = user.state.page
        if not page:
            await Router.set_page(user, Page.get_default())

        return page

    @staticmethod
    async def set_page(user: Users, page: str | Page):
        user.state.page = page \
            if isinstance(page, Page) \
            else Page.get(page)

    async def route_callback(self, callback, user):
        page = await self.get_page(user)

    async def route_message(self, message, user):
        page = await self.get_page(user)

    async def route_command(self, message, user):
        page = await self.get_page(user)

    async def route_media(self, message, user):
        page = await self.get_page(user)
