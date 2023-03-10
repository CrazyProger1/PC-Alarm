import functools
import gettext

from app.settings import settings
from app.database import Users, Languages
from .filesystem import iter_files
from .cls import SingletonMeta
from .logging import logger


class Translator(metaclass=SingletonMeta):
    def __init__(self, domain: str = None):
        self._domain = domain
        self._loaded_packs: dict[str, gettext.GNUTranslations] = {}
        self._load()

    def _load(self):
        for language in Languages.select():
            try:
                self._loaded_packs.update({
                    language.short_name: gettext.translation(
                        domain=self._domain,
                        localedir=settings.L18N.LOCALE_FOLDER,
                        languages=[language.short_name]
                    )})
                logger.debug(f'Loaded language: {language.short_name}')
            except FileNotFoundError:
                if settings.DEBUG:
                    logger.fatal(
                        f'No translations for {self._domain} domain in the {language.short_name} language!'
                        f' Note: add a translation for this domain or the program will not work')
                    continue
                raise

    @functools.cache
    def translate(
            self,
            key: str,
            user: Users = None,
            language: Languages = None
    ) -> str:
        if not language and user:
            language = user.language

        if not language:
            language = Languages.get_default()

        lang_name = language.short_name

        try:
            return self._loaded_packs[lang_name].gettext(key)
        except KeyError:
            return key


@functools.cache
def _(*args, **kwargs):
    return Translator().translate(*args, **kwargs)
