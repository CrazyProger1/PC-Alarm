import asyncio
import sys
from tkinter import messagebox

from src.settings import (
    APP,
    DEBUG
)

from src.core.logging import logger
from src.factories import ApplicationFactory
from src.app import run


def report_critical_error(error: Exception):
    text = f'An error occurred while running application, please try to restart. \nError: {error}'
    logger.critical(text)
    messagebox.showerror(f'{APP} Error', text)


async def main():
    logger.info(f'{APP} launched')
    try:
        await run(factory=ApplicationFactory)
    except Exception as error:
        if DEBUG:
            raise error
        report_critical_error(error=error)
        await asyncio.sleep(10)
        sys.exit(-1)

    logger.info(f'{APP} terminated')


if __name__ == '__main__':
    asyncio.run(main())
