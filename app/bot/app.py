import aiogram

from aiogram import types
from app.settings import settings
from app.utils.import_utils import import_module
from .router import Router
from .pages import *


class App:
    def __init__(self):
        self._bot = aiogram.Bot(token=settings.BOT.TOKEN)
        self._dispatcher = aiogram.Dispatcher(bot=self._bot)
        self._middlewares = list(
            import_module(middleware_path)(bot=self._bot)
            for middleware_path in settings.MIDDLEWARES
        )
        self._router = Router(bot=self._bot)

    @staticmethod
    def _middlewares(method):
        async def wrapper(self, message_or_callback: types.Message | types.CallbackQuery):
            counter = 0
            middleware = self._middlewares[counter]

            async def next_step(*args, **kwargs):
                nonlocal counter, middleware
                counter += 1

                if counter < len(self._middlewares):
                    middleware = self._middlewares[counter]
                    await middleware(next_step, *args, **kwargs)
                else:
                    await method(self, *args, **kwargs)

            await middleware(next_step, message_or_callback)

        return wrapper

    @_middlewares
    async def _handle_callback(self, *args, **kwargs):
        await self._router.route_callback(*args, **kwargs)

    @_middlewares
    async def _handle_message(self, *args, **kwargs):
        await self._router.route_message(*args, **kwargs)

    @_middlewares
    async def _handle_command(self, *args, **kwargs):
        await self._router.route_command(*args, **kwargs)

    @_middlewares
    async def _handle_media(self, *args, **kwargs):
        await self._router.route_media(*args, **kwargs)

    def _register_handlers(self):
        self._dispatcher.register_message_handler(
            callback=self._handle_command,
            regexp=settings.COMMAND.REGEXP
        )
        self._dispatcher.register_message_handler(
            callback=self._handle_message
        )
        self._dispatcher.register_message_handler(
            callback=self._handle_media,
            content_types=(
                types.ContentType.AUDIO,
                types.ContentType.VOICE,
                types.ContentType.VIDEO
            )
        )
        self._dispatcher.register_callback_query_handler(
            callback=self._handle_callback
        )

    def run(self):
        self._register_handlers()
        aiogram.executor.start_polling(
            dispatcher=self._dispatcher,
            skip_updates=True
        )
