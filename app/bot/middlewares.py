import aiogram

from aiogram import types

from app.utils import logging
from app.utils.translator import _
from app.database import Authenticator
from app.exceptions import AccessError, BotInteractionError
from app.settings import settings
from .router import Router
from .types import Middleware, Page


class ErrorCatchingMiddleware(Middleware):
    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        try:
            return await method(message_or_callback, **kwargs)
        except BotInteractionError as e:
            await message_or_callback.reply(str(e), parse_mode=settings.MESSAGES.PARSE_MODE)
        except Exception as e:
            await message_or_callback.reply(
                f'<b>An internal error occurred, please write to support:</b> @{settings.SUPPORT.TELEGRAM}\nInfo: `{e}`',
                parse_mode=types.ParseMode.HTML)

            logging.logger.error(str(e))


class AuthMiddleware(Middleware):
    def __init__(self, *args, **kwargs):
        super(AuthMiddleware, self).__init__(*args, **kwargs)
        self.authenticator = Authenticator()

    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        user = self.authenticator.authenticate(message_or_callback.from_user)
        return await method(message_or_callback, user=user, **kwargs)


class PermissionMiddleware(Middleware):
    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        user = kwargs.get('user')
        page = await Router.get_page(user)
        for perm_cls in page.permission_classes:
            if not await perm_cls(bot=self.bot)(
                    page,
                    message_or_callback,
                    **kwargs
            ):
                user_page = user.state.page
                await page.back(user)
                if user_page == user.state.page:
                    await Router.set_page(user, Page.get_default())
                raise AccessError(_(perm_cls.message_key, user=user))

        return await method(message_or_callback, **kwargs)
