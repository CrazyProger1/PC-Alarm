import json

from abc import ABC


class Config(dict):

    def __getattr__(self, item):
        return self.__getitem__(item)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __repr__(self):
        return json.dumps(dict(self), indent=1)


class FileConfig(Config, ABC):
    path: str = None

    @classmethod
    def load(cls, *args, **kwargs):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        raise NotImplementedError
