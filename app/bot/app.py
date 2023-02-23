import aiogram

from aiogram import types
from app.settings import settings


class App:
    def __init__(self):
        self._bot = aiogram.Bot(token=settings.BOT.TOKEN)
        self._dispatcher = aiogram.Dispatcher(bot=self._bot)

    @staticmethod
    def _catch_error(method):
        async def wrapper(self, message_or_callback: types.Message | types.CallbackQuery):
            try:
                return await method(self, message_or_callback)
            except Exception:
                raise

        return wrapper

    @_catch_error
    async def _handle_callback(self, callback: types.CallbackQuery):
        pass

    @_catch_error
    async def _handle_message(self, message: types.Message):
        pass

    @_catch_error
    async def _handle_command(self, message: types.Message):
        pass

    @_catch_error
    async def _handle_media(self, message: types.Message):
        pass

    def _register_handlers(self):
        self._dispatcher.register_message_handler(
            callback=self._handle_command,
            regexp=settings.COMMAND_REGEXP
        )
        self._dispatcher.register_message_handler(
            callback=self._handle_message
        )
        self._dispatcher.register_message_handler(
            callback=self._handle_media,
            content_types=
            (
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
