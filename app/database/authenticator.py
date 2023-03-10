from aiogram import types
from app.utils.cls import Customizable
from app.settings import settings
from .models import Users, Languages, Categories


class Authenticator(Customizable):
    cls_path: str = settings.DATABASE.AUTHENTICATOR_CLASS

    def authenticate(self, user: types.User) -> Users:
        db_user = Users.get_or_none(id=user.id)

        language = Languages.get_or_none(short_name=user.locale.language) or Languages.get_default()
        if not db_user:
            db_user = Users.create(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                language=language
            )

        if db_user.id == settings.BOT.ADMIN:
            db_user.category = Categories.get_admin()
        return db_user
