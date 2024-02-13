from enum import Enum
from typing import Callable

from typeguard import typechecked

from .types import BaseEventChannel


class EventChannel(BaseEventChannel):
    def __init__(self):
        self._subscribers = {'__all__': []}

    @typechecked
    def publish(self, event: str | Enum, *args, **kwargs) -> None:
        callbacks = self._subscribers['__all__'].copy()
        callbacks.extend(self._subscribers.get(event, []))

        for callback in callbacks:
            callback(*args, **kwargs)

    @typechecked
    def subscribe(self, callback: Callable, event: str | Enum | None = None) -> None:
        if event is not None:
            if event not in self._subscribers:
                self._subscribers[event] = []
            self._subscribers[event].append(callback)
        else:
            self._subscribers['__all__'].append(callback)


class AsyncEventChannel(EventChannel):

    @typechecked
    async def publish(self, event: str | Enum, *args, **kwargs) -> None:
        callbacks = self._subscribers['__all__'].copy()
        callbacks.extend(self._subscribers.get(event, []))

        for callback in callbacks:
            await callback(*args, **kwargs)
