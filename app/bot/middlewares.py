import aiogram

from aiogram import types
from app.utils.cls import SingletonMeta
from app.database import Authenticator
from app.exceptions import AccessError
from .router import Router
from .types import Middleware, Page


class ErrorCatchingMiddleware(Middleware):
    async def __call__(self, method, message_or_callback: types.Message | types.CallbackQuery, **kwargs):
        try:
            return await method(message_or_callback, **kwargs)
        except Exception as e:
            print(e)
            raise


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
                raise AccessError()

        return await method(message_or_callback, **kwargs)
