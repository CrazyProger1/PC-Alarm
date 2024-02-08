import argparse
import inspect
from abc import ABC, abstractmethod
from typing import Container, Sequence, Callable
from enum import Enum

from pydantic import BaseModel
from typeguard import typechecked


class BaseSchemedArgumentParser(argparse.ArgumentParser, ABC):
    @abstractmethod
    def parse_schemed_args(
            self,
            args: Sequence[str] | None = None,
            namespace: argparse.Namespace | None = None
    ) -> BaseModel: ...


class SchemedArgumentParser(BaseSchemedArgumentParser):
    @typechecked
    def __init__(
            self,
            schema: type[BaseModel],
            *,
            ignore_fields: Container[str] | None = None,
            positional_arguments: Container[str] | None = None,
            short_aliases: dict[str, str] | None = None,
            **kwargs
    ):
        super(SchemedArgumentParser, self).__init__(**kwargs)
        self._schema = schema
        self._ignore_fields = ignore_fields or set()
        self._positional_arguments = positional_arguments or set()
        self._short_aliases = short_aliases or {}

        if schema:
            self._add_arguments_from_schema()

    @staticmethod
    def _is_enum(enum) -> bool:
        return inspect.isclass(enum) and issubclass(enum, Enum)

    @staticmethod
    def _build_argument_action(call: Callable):
        return type(
            'action',
            (argparse.Action,),
            {'__call__': call}
        )

    def _is_positional_argument(self, name: str):
        return name in self._positional_arguments


    def _get_argument_type(self, field_info):
        field_type = field_info.annotation

        if not self._is_enum(enum=field_type):
            return field_type

    def _add_field_argument(self, field_name: str, field_info):
        actual_name = field_info.alias or field_name
        short_name = self._short_aliases.get(
            field_name,
            self._short_aliases.get(actual_name, actual_name)
        ).removeprefix('-').removeprefix('--')[0]

        args = []
        kwargs = {
            'default': field_info.default,
            'help': field_info.description,
        }

        if self._is_positional_argument(name=actual_name):
            if not field_info.is_required():
                kwargs.update({'nargs': '?'})

            args.append(actual_name)
        else:
            args.extend((f'-{short_name}', f'--{actual_name}'))

        self.add_argument(
            *args,
            **kwargs
        )

    def _add_arguments_from_schema(self):
        fields = self._schema.model_fields

        for name, info in fields.items():
            if name in self._ignore_fields:
                continue

            self._add_field_argument(
                field_name=name,
                field_info=info
            )

    @typechecked
    def parse_schemed_args(
            self,
            args: Sequence[str] | None = None,
            namespace: argparse.Namespace | None = None
    ) -> BaseModel:
        namespace = self.parse_args(args=args, namespace=namespace)
        return self._schema.model_validate(namespace.__dict__)
