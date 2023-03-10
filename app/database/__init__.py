import gettext

from app.settings import settings
from app.utils import json, filesystem, logging, config
from .connection import connection
from .models import Users, Languages, Categories, Model
from .authenticator import Authenticator

__all__ = [
    'connection',
    'Users',
    'Languages',
    'Categories',
    'Authenticator'
]


def _load_default_languages():
    for lang_folder in filesystem.iter_files(settings.L18N.LOCALE_FOLDER):
        if not lang_folder.is_dir():
            continue
        data = config.JSONConfig.load(lang_folder / '.lang')
        Languages.get_or_create(
            full_name=data.full_name,
            short_name=data.short_name,
        )
    logging.logger.info('Loaded default languages')


def _load_default_categories():
    for category_file in filesystem.iter_files(settings.CATEGORIES.FOLDER):
        data = config.JSONConfig.load(category_file)
        Categories.get_or_create(
            name=data.name,
            access_level=data.access_level
        )
    logging.logger.info('Loaded default categories')


def _init():
    connection.create_tables((Model.__subclasses__()))
    _load_default_categories()
    _load_default_languages()


_init()
