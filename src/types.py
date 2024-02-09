from abc import ABC, abstractmethod

from src.core.schemas import (
    Arguments,
    Settings
)


class BaseApplication(ABC):
    def __init__(self, arguments: Arguments, settings: Settings):
        self._arguments = arguments
        self._settings = settings

    @abstractmethod
    async def run(self): ...


class BaseApplicationFactory(ABC):
    @classmethod
    @abstractmethod
    def create(cls, arguments: Arguments, settings: Settings) -> BaseApplication: ...
