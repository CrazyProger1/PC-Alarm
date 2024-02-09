import asyncio
import sys
from tkinter import messagebox

from src.settings import (
    APP,
    DESCRIPTION,
    ENV_FILE
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
    Arguments,
    ENVSettings
)
from src.core.enums import (
    ApplicationWorkingMode
)
from src.configurator import run_configurator
from src.bot import run_bot


async def run():
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
    settings.env = load_settings(
        file=ENV_FILE,
        schema=ENVSettings
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
        instance=settings,
        exclude=('env',)
    )
    save_settings(
        file=ENV_FILE,
        instance=settings.env,
    )


def report_critical_error(error: Exception):
    text = f'An error occurred while running application, please try to restart. \nError: {error}'
    logger.critical(text)
    messagebox.showerror(f'{APP} Error', text)


async def main():
    logger.info(f'{APP} launched')
    try:
        await run()
    except Exception as error:
        report_critical_error(error=error)
        sys.exit(-1)

    logger.info(f'{APP} terminated')


if __name__ == '__main__':
    asyncio.run(main())
