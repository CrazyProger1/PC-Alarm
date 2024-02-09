from pydantic import BaseModel

from src.utils.arguments import (
    BaseSchemedArgumentParser
)
from src.utils.settings import (
    load,
    save
)
from src.utils.settings.exceptions import (
    SettingsError
)
from src.core.logging import logger


def parse_arguments(parser: BaseSchemedArgumentParser) -> BaseModel:
    args = parser.parse_schemed_args()
    logger.info(f'Arguments parsed: {args}')
    return args


def load_settings(file: str, schema: type[BaseModel]) -> BaseModel:
    logger.info(f'Settings loaded')


def save_settings(file: str, instance: BaseModel):
    logger.info(f'Settings saved')

