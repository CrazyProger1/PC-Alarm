import functools

from app.utils.filesystem import read, write
from dotenv import load_dotenv
from .config import FileConfig


class ENVConfig(FileConfig):
    def __init__(self, data: dict):
        super(ENVConfig, self).__init__(data)

    @classmethod
    @functools.cache
    def load(cls, path: str = None) -> "ENVConfig":
        content = read(path or cls.path)
        load_dotenv(path)

        data = {}

        for line in content.split('\n'):
            line = line.strip()
            if line:
                key, value = line.split('=')
                data.update({key: value})
        return cls(data)

    def save(self, path: str = None):
        content = ''
        for key, value in self.items():
            content += f'{key}={value}\n'

        write(path, content)
