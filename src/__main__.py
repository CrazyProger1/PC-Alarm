import asyncio

import toml
from pydantic import BaseModel
from typeguard import typechecked

from src.settings import (
    DEFAULT_SETTINGS_FILE
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
    args = parse_arguments(SchemedArgumentParser(schema=Arguments))
    settings = load_settings(file=args.settings_file, schema=Settings)

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


if __name__ == '__main__':
    asyncio.run(main())
