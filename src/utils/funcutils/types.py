import inspect
from functools import wraps
from typing import Callable, Container


def guard(func: Callable = None, /, *, ignore: Container[str] = None) -> Callable:
    ignore = ignore or set()

    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        for i, (name, info) in enumerate(signature.parameters.items()):
            if name in ignore:
                continue

            tp = info.annotation
            default = info.default

            try:
                value = kwargs.get(name, args[i])
            except IndexError:
                value = default
                if default == inspect.Parameter.empty:
                    continue

            if not isinstance(value, tp):
                raise TypeError(f'Wrong type of {name}, it must be type of {tp}')
        return func(*args, **kwargs)

    def decorator(f: Callable = None):
        nonlocal func
        func = f
        return wraps(func)(wrapper)

    if not func:
        return decorator
    else:
        return wraps(func)(wrapper)
