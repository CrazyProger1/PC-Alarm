from abc import ABC


class Config:
    def __getitem__(self, item):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __getattr__(self, item):
        raise NotImplementedError

    def __setattr__(self, key, value):
        raise NotImplementedError


class FileConfig(Config, ABC):
    path: str = None

    @classmethod
    def load(cls, *args, **kwargs):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        raise NotImplementedError
