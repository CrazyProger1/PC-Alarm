import os

from typeguard import typechecked

from .exceptions import LoaderNotFoundError
from .types import (
    BaseLoader,
    BaseLoaderFactory
)
from ..clsutils import iter_subclasses


class LoaderFactory(BaseLoaderFactory):
    @classmethod
    @typechecked
    def create(cls, file: str) -> BaseLoader:
        if not os.path.isfile(file):
            raise FileNotFoundError(f'File not found: {file}')

        filext = os.path.splitext(file)[1] or os.path.splitext(file)[0]

        for loader_class in iter_subclasses(BaseLoader):
            if filext in loader_class.filetypes:
                return loader_class()
        raise LoaderNotFoundError(file=file)
