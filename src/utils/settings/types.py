from abc import ABC, abstractmethod
from typing import Container, Iterable

from pydantic import BaseModel


class BaseLoader(ABC):
    filetypes: Container[str]

    @abstractmethod
    def load(self, file: str, schema: type[BaseModel], **kwargs) -> BaseModel: ...

    @abstractmethod
    def save(self, file: str, data: BaseModel, ignore_fields: Iterable[str] = None, **kwargs) -> None: ...


class BaseLoaderFactory(ABC):
    @classmethod
    @abstractmethod
    def create(cls, file: str) -> BaseLoader: ...
