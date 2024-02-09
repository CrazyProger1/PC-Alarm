import asyncio

from src.settings import (
    APP,
    DESCRIPTION
)
from src.utils.arguments import SchemedArgumentParser
from src.core.logging import logger
from src.core.utils import (
    load_settings,
    save_settings,
    parse_arguments
)
from src.core.schemas import (
    Settings,
    Arguments
)
from src.core.enums import (
    ApplicationWorkingMode
)
from src.configurator import run_configurator
from src.bot import run_bot


async def main():
    logger.info(f'{APP} launched')

    arguments = parse_arguments(
        parser=SchemedArgumentParser(
            schema=Arguments,
            prog=APP,
            description=DESCRIPTION
        )
    )

    settings = load_settings(
        file=arguments.settings_file,
        schema=Settings
    )

    match arguments.mode:
        case ApplicationWorkingMode.BOT:
            await run_bot(
                arguments=arguments,
                settings=settings
            )
        case ApplicationWorkingMode.CONFIGURATOR:
            await run_configurator(
                arguments=arguments,
                settings=settings
            )

    save_settings(
        file=arguments.settings_file,
        instance=settings
    )

    logger.info(f'{APP} terminated')


if __name__ == '__main__':
    asyncio.run(main())
