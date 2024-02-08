from abc import ABC, abstractmethod
from typing import Iterable


class BaseDependency(ABC):

    @abstractmethod
    def bind(self, value: any): ...

    @abstractmethod
    @property
    def value(self) -> any: ...

    @abstractmethod
    @property
    def container(self) -> "BaseContainer": ...

    @abstractmethod
    @property
    def name(self) -> str: ...


class BaseContainer(ABC):
    @abstractmethod
    @property
    def dependencies(self) -> Iterable[BaseDependency]: ...
