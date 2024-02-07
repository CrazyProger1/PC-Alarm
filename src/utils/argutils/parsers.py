import argparse
import inspect
from typing import Container, Sequence
from enum import Enum

from pydantic import BaseModel


class SchemedArgumentParser(argparse.ArgumentParser):
    def __init__(
            self,
            schema: type[BaseModel],
            *,
            ignore_fields: Container[str] | None = None,
            positional_arguments: Container[str] | None = None,
            short_aliases: dict[str, str] | None = None,
            **kwargs
    ):
        assert issubclass(schema, BaseModel), f"Schema must be subclass of {BaseModel}"

        super(SchemedArgumentParser, self).__init__(**kwargs)
        self._schema = schema
        self._ignore_fields = ignore_fields or set()
        self._positional_arguments = positional_arguments or set()
        self._short_aliases = short_aliases or {}

        if schema:
            self._add_arguments_from_schema()

    @staticmethod
    def _is_enum_field(field_type: type):
        return inspect.isclass(field_type) and issubclass(field_type, Enum)

    @staticmethod
    def _convert_enum_value(value: str, enum: type[Enum]):
        if issubclass(enum, int):
            return enum(int(value))
        return enum(value)

    def _convert_value(
            self,
            value: str,
            field_info
    ):

        field_type = field_info.annotation

        if self._is_enum_field(field_type):
            return self._convert_enum_value(value, enum=field_type)

        if field_info.metadata:
            for validator in field_info.metadata:
                try:
                    validator.func(value)
                except (ValueError, AssertionError):
                    raise ValueError()

        return value

    def _get_value_converter(self, field_info):
        def argument(value: str):
            return self._convert_value(value, field_info)

        return argument

    def _add_field_argument(
            self,
            name: str,
            info
    ):
        field_type: type = info.annotation

        args = []
        kwargs = {
            'default': info.default,
            'help': info.description,
            'type': self._get_value_converter(info),
        }
        if name not in self._positional_arguments:
            alias = self._short_aliases.get(
                name,
                info.serialization_alias or name
            )
            alias = alias.removeprefix('-')

            args.extend((f'-{alias[0]}', f'--{name}',))
        else:
            args.append(name)

            if not info.is_required():
                kwargs.update({'nargs': '?'})

        if self._is_enum_field(field_type):
            kwargs.update({
                'choices': list(map(lambda c: c, field_type))
            })

        self.add_argument(
            *args,
            **kwargs,
        )

    def _add_arguments_from_schema(self):
        fields = self._schema.model_fields

        for name, info in fields.items():
            if name not in self._ignore_fields:
                self._add_field_argument(
                    name=name,
                    info=info
                )

    def parse_schemed_args(
            self,
            args: Sequence[str] = None,
            namespace: argparse.Namespace = None
    ) -> BaseModel:
        namespace = self.parse_args(args=args, namespace=namespace)
        return self._schema.model_validate(namespace.__dict__)
