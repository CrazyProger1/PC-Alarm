import argparse
import os
from typing import Iterable

from .. import imputils
from .i18n import extract_ids


def setup_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='i18n',
        description='Extracts translations from translatable enums'
    )

    parser.add_argument(
        'source',
        default='main.py',
        help='The source file to extract translations from (main file of application)',
        nargs='?'
    )

    parser.add_argument(
        'destination',
        default='main.po',
        help='Destination .po file',
        nargs='?'
    )

    return parser


def create_portable_object_file(ids: Iterable[str], destination_file: str):
    with open(destination_file, 'w', encoding='utf-8') as f:
        for msgid in ids:
            f.write(f'\nmsgid "{msgid}"\nmsgstr ""\n')


def main():
    parser = setup_argparse()
    args = parser.parse_args()

    source = args.source
    try:
        if os.path.isfile(source):
            imputils.import_module_by_filepath(source)
        else:
            imputils.import_module(source)
    except ImportError:
        raise ImportError(f"Failed to import source file {source}, make sure it exists")

    create_portable_object_file(extract_ids(), args.destination)


if __name__ == '__main__':
    main()
