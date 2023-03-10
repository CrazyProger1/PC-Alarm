from typing import Callable


class EventEmitter:
    def __init__(self):
        self._callbacks = {}

    def add_callback(self, event: int, callback: Callable):
        callbacks = self._callbacks.get('event')

        if not callbacks:
            callbacks = []
            self._callbacks[event] = callbacks

        callbacks.append(callback)

    async def _call(self, event: int, **kwargs):
        for callback in self._callbacks.get(event, ()):
            args = []
            if callback != getattr(self, callback.__name__, None):
                args.append(self)
            await callback(*args, **kwargs)
