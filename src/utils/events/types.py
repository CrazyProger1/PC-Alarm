from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable


class BaseEventChannel(ABC):

    @abstractmethod
    def publish(self, event: str | Enum, *args, **kwargs) -> None: ...

    @abstractmethod
    def subscribe(self, callback: Callable, event: str | Enum | None = None) -> None: ...
