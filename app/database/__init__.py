from app.settings import settings
from app.utils import json, filesystem, logging
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
    for pack_file in filesystem.iter_files(settings.FILESYSTEM.LANGUAGES_FOLDER):
        data = json.read_json(pack_file)
        Languages.get_or_create(
            full_name=data['full_name'],
            short_name=data['short_name'],
            pack_file=pack_file
        )
    logging.logger.info('Loaded default languages')


def _load_default_categories():
    for category_file in filesystem.iter_files(settings.FILESYSTEM.CATEGORIES_FOLDER):
        data = json.read_json(category_file)
        Categories.get_or_create(
            name=data['name'],
            access_level=data['access_level']
        )
    logging.logger.info('Loaded default categories')


def _init():
    connection.create_tables((Model.__subclasses__()))
    _load_default_categories()
    _load_default_languages()


_init()
