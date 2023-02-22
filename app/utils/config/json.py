import functools

from .config import FileConfig
from app.utils.json import *


class JSONConfig(dict, FileConfig):
    def __init__(self, data: dict):
        super(JSONConfig, self).__init__(
            {
                key: value
                if not isinstance(value, dict)
                else JSONConfig(value)
                for key, value in data.items()
            })

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    @classmethod
    @functools.cache
    def load(cls, path: str) -> "JSONConfig":
        return cls(read_json(path))

    def save(self, path: str):
        write_json(path, dict(self))
