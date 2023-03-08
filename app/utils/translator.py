import gettext

from app.settings import settings
from app.database import Users, Languages
from .filesystem import iter_files
from .cls import SingletonMeta


class Translator(metaclass=SingletonMeta):
    def __init__(self, domain: str = None):
        self._domain = domain
        self._loaded_packs: dict[str, gettext.GNUTranslations] = {}
        self._load()

    def _load(self):
        for language in Languages.select():
            self._loaded_packs.update({language.short_name: gettext.translation(
                domain=self._domain,
                localedir=settings.LANGUAGE.LOCALE_FOLDER,
                languages=[language.short_name]
            )})

    def translate(
            self,
            key: str,
            user: Users = None,
            language: Languages = None
    ):
        if not language and user:
            language = user.language

        if not language:
            language = Languages.get_default()

        lang_name = language.short_name
        return self._loaded_packs[lang_name].gettext(key)


def _(*args, **kwargs):
    return Translator().translate(*args, **kwargs)
