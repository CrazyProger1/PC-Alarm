import sys

import aiogram
import tkinter.messagebox

from aiogram import types
from app.settings import settings
from app.utils import import_utils, translator
from .sender import Sender
from .router import Router
from .pages import *
from .executors import *
from .enums import ContentType


class App:
    def __init__(self):
        self._translator = translator.Translator(settings.L18N.BOT_DOMAIN)
        if not settings.BOT.TOKEN or not settings.BOT.ADMIN:
            tkinter.messagebox.showerror('PC-Alarm',
                                         'Token or Admin-ID not specified! Run with --configurator option.')
            sys.exit(-1)
        self._bot = aiogram.Bot(token=settings.BOT.TOKEN)
        self._dispatcher = aiogram.Dispatcher(bot=self._bot)
        self._middlewares = list(
            import_utils.import_module(middleware_path)(bot=self._bot)
            for middleware_path in settings.MIDDLEWARES
        )
        self._sender = Sender(bot=self._bot)
        self._router = Router(bot=self._bot)

    @staticmethod
    def _middlewares(content_type: ContentType):
        def decorator(method):
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

                await middleware(
                    next_step,
                    message_or_callback,
                    content_type=content_type)

            return wrapper

        return decorator

    @_middlewares(content_type=ContentType.CALLBACK)
    async def _handle_callback(self, *args, **kwargs):
        await self._router.route_callback(*args, **kwargs)

    @_middlewares(content_type=ContentType.MESSAGE)
    async def _handle_message(self, *args, **kwargs):
        await self._router.route_message(*args, **kwargs)

    @_middlewares(content_type=ContentType.COMMAND)
    async def _handle_command(self, *args, **kwargs):
        await self._router.route_command(*args, **kwargs)

    @_middlewares(content_type=ContentType.MEDIA)
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
