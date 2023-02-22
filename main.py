import argparse

from app.utils.logging import *
from app.settings import settings


def configure_logging():
    logging.basicConfig(
        filename=settings.LOGGING.FILE,
        filemode=settings.LOGGING.FILEMODE,
        level=settings.LOGGING.LEVEL,
        format=settings.LOGGING.FORMAT
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=settings.APP_NAME,
        description=f'{settings.APP_NAME} is an application that will help you detect someone '
                    'else presence on your computer while you are away.'
    )
    parser.add_argument(
        '-c', '--configurator',
        help='run in configurator mode',
        action='store_true',
        default=False
    )

    return parser.parse_args()


def main():
    args = parse_args()
    configure_logging()
    logger.info(f'Application started. Arguments: {args.__dict__}')

    if args.configurator:
        logger.debug('Running configurator...')
    else:
        logger.debug('Running bot...')

    logger.info(f'Application terminated')


if __name__ == '__main__':
    main()
