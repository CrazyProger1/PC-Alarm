from .config import Config
from app.utils.import_utils import import_module


class PyConfig(Config):
    def __init__(self, data: dict):
        super(PyConfig, self).__init__(data)

    @classmethod
    def import_file(cls, path: str):
        mod = import_module(path)
        data = {}

        for key, value in vars(mod).items():
            if key.startswith('__') or key.startswith('_') or not key.isupper():
                continue
            data.update({key: value})

        return cls(data)
