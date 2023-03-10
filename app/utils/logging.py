import logging
import colorama

from app.settings import settings

colorama.init()


class _Formatter(logging.Formatter):
    green = colorama.Fore.GREEN
    white = colorama.Fore.WHITE
    blue = colorama.Fore.BLUE
    yellow = colorama.Fore.YELLOW
    red = colorama.Fore.RED
    bold_red = colorama.Fore.RED + colorama.Style.BRIGHT
    reset = colorama.Style.RESET_ALL

    def __init__(self, log_format: str):
        self.formats = {
            logging.DEBUG: self.blue + log_format + self.reset,
            logging.INFO: self.green + log_format + self.reset,
            logging.WARNING: self.yellow + log_format + self.reset,
            logging.ERROR: self.red + log_format + self.reset,
            logging.CRITICAL: self.bold_red + log_format + self.reset
        }
        super(_Formatter, self).__init__()

    def format(self, record):
        log_fmt = self.formats.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger: logging.Logger = logging.getLogger(settings.APP.NAME)
logger.setLevel(settings.LOGGING.LEVEL)

_stream_handler = logging.StreamHandler()
_stream_handler.setLevel(settings.LOGGING.LEVEL)

_stream_handler.setFormatter(_Formatter(settings.LOGGING.FORMAT))

logger.addHandler(_stream_handler)
