import peewee

from app.settings import settings
from app.utils.logging import logger
from app.utils.import_utils import import_module


def connect():
    logger.info('SQLite connection created')
    try:
        engine = import_module(settings.DATABASE.ENGINE)
    except ModuleNotFoundError:
        raise

    config = settings.DATABASE.PARAMS

    return engine(**config)


connection = connect()
