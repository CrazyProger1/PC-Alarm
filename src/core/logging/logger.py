import logging

from src.settings import (
    APP,
    DEBUG,
    LOGGING_LEVEL
)

logger = logging.getLogger(APP)
logger.setLevel(LOGGING_LEVEL)

if DEBUG:
    try:
        import colorlog

        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)s:%(name)s:%(message)s',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
    except ImportError:
        pass
