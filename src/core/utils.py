from typing import Iterable

from pydantic import BaseModel

from src.utils.arguments import (
    BaseSchemedArgumentParser
)
from src.utils.settings import (
    load,
    save
)
from src.core.logging import logger


def parse_arguments(parser: BaseSchemedArgumentParser) -> BaseModel:
    args = parser.parse_schemed_args()
    logger.info(f'Arguments parsed: {args}')
    return args


def load_settings(file: str, schema: type[BaseModel]) -> BaseModel:
    try:
        settings = load(
            file=file,
            schema=schema
        )
    except Exception as e:
        logger.critical(f'Error occurred while loading settings: {e}')
        raise

    logger.info(f'Settings loaded: {file}')
    return settings


def save_settings(file: str, instance: BaseModel, exclude: Iterable[str] = None):
    try:
        save(
            file=file,
            instance=instance,
            exclude=exclude,
            by_alias=True
        )
    except Exception as e:
        logger.critical(f'Error occurred while saving settings: {e}')
        raise
    logger.info(f'Settings saved: {file}')

