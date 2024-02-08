import asyncio

import toml
from pydantic import BaseModel
from typeguard import typechecked

from src.settings import (
    DEFAULT_SETTINGS_FILE,
    APP,
    DESCRIPTION
)
from src.configurator import run_configurator
from src.bot import run_bot
from src.core.schemas import (
    Settings,
    Arguments
)
from src.core.enums import (
    ApplicationWorkingMode
)
from src.core.logging import logger
from src.utils.argutils import (
    BaseSchemedArgumentParser,
    SchemedArgumentParser
)


@typechecked
def parse_arguments(parser: BaseSchemedArgumentParser) -> BaseModel:
    return parser.parse_schemed_args()


@typechecked
def load_settings(file: str, schema: type[BaseModel]) -> BaseModel:
    try:
        data = toml.load(file)
    except Exception as e:
        return schema()
    return schema.model_validate(data)


@typechecked
def save_settings(file: str, settings: BaseModel):
    try:
        with open(file, 'w', encoding='utf-8') as f:
            toml.dump(settings.model_dump(), f)
    except Exception as e:
        save_settings(DEFAULT_SETTINGS_FILE, settings)


async def main():
    logger.info(f'{APP} launched')
    args = parse_arguments(SchemedArgumentParser(
        schema=Arguments,
        prog=APP,
        description=DESCRIPTION
    ))
    logger.info(f'Arguments parsed: {args}')
    settings = load_settings(file=args.settings_file, schema=Settings)

    logger.info('Settings loaded')

    match args.mode:
        case ApplicationWorkingMode.BOT:
            await run_bot(
                arguments=args,
                settings=settings
            )
        case ApplicationWorkingMode.CONFIGURATOR:
            await run_configurator(
                arguments=args,
                settings=settings
            )

    save_settings(file=args.settings_file, settings=settings)
    logger.info(f'{APP} terminated')


if __name__ == '__main__':
    asyncio.run(main())
