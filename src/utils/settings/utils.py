from pydantic import BaseModel
from typeguard import typechecked

from .factories import LoaderFactory
from .types import BaseLoader


@typechecked
def load(file: str, schema: type[BaseModel], loader: BaseLoader = None) -> BaseModel:
    if not loader:
        loader = LoaderFactory.create(file=file)

    return loader.load(
        file=file,
        schema=schema
    )
