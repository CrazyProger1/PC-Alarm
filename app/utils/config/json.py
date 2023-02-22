import functools

from app.utils.json import *
from .config import FileConfig


class JSONConfig(FileConfig):
    def __init__(self, data: dict):
        super(JSONConfig, self).__init__(
            {
                key: value
                if not isinstance(value, dict)
                else JSONConfig(value)
                for key, value in data.items()
            })

    @classmethod
    @functools.cache
    def load(cls, path: str = None) -> "JSONConfig":
        return cls(read_json(path or cls.path))

    def save(self, path: str = None):
        write_json(path or self.path, dict(self))


