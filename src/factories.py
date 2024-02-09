from src.types import (
    BaseApplication,
    BaseApplicationFactory
)
from src.bot import Bot
from src.configurator import Configurator
from src.core.enums import ApplicationWorkingMode
from src.core.schemas import (
    Arguments,
    Settings
)
from src.core.logging import logger


class ApplicationFactory(BaseApplicationFactory):
    @classmethod
    def create(cls, arguments: Arguments, settings: Settings) -> BaseApplication:
        logger.info(f'Launching in {arguments.mode.value} mode')

        match arguments.mode:
            case ApplicationWorkingMode.BOT:
                return Bot(
                    arguments=arguments,
                    settings=settings
                )
            case ApplicationWorkingMode.CONFIGURATOR:
                return Configurator(
                    arguments=arguments,
                    settings=settings
                )
