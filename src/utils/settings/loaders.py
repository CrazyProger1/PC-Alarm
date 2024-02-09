import os.path
from typing import Iterable

import toml
import json
from pydantic import BaseModel
from typeguard import typechecked

from .types import BaseLoader
from .exceptions import (
    FileFormatError
)


class TOMLLoader(BaseLoader):
    filetypes = {
        '.toml',
    }

    @typechecked
    def load(self, file: str, schema: type[BaseModel], **kwargs) -> BaseModel:
        if not os.path.isfile(file):
            raise FileNotFoundError(f'File not found: {file}')

        try:
            raw: dict = toml.load(file)
            return schema.model_validate(raw, **kwargs)
        except toml.TomlDecodeError as e:
            raise FileFormatError(file=file, msg=str(e))

    @typechecked
    def save(self, file: str, data: BaseModel, ignore_fields: Iterable[str] | None = None, **kwargs) -> None:
        if not ignore_fields:
            ignore_fields = set()

        with open(file, 'w', encoding='utf-8') as f:
            raw: dict = data.model_dump()
            for field in ignore_fields:
                raw.pop(field)
            toml.dump(raw, f)


class JSONLoader(BaseLoader):
    filetypes = {
        '.json',
    }

    @typechecked
    def load(self, file: str, schema: type[BaseModel], **kwargs) -> BaseModel:
        pass

    @typechecked
    def save(self, file: str, data: BaseModel, ignore_fields: Iterable[str], **kwargs) -> None:
        pass


class ENVLoader(BaseLoader):
    filetypes = {
        '.env',
    }

    def load(self, file: str, schema: type[BaseModel], **kwargs) -> BaseModel:
        pass

    def save(self, file: str, data: BaseModel, ignore_fields: Iterable[str], **kwargs) -> None:
        pass
