from aiogram import types
from app.utils.cls import Customizable
from app.settings import settings
from .models import Users


class Authenticator(Customizable):
    cls_path: str = settings.DATABASE.AUTHENTICATOR_CLASS

    def authenticate(self, user: types.User) -> Users:
        pass
