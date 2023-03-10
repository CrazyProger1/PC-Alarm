import sys
import os
import argparse
import random
import re

from pathlib import Path
from dataclasses import dataclass


@dataclass
class Translation:
    key: str
    location: str


def log_pos(text):
    if progargs.verbose:
        print(f'+{text}')


def log_neg(text):
    if progargs.verbose:
        print(f'-{text}')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='Extrans-Script',
        description=f'Extrans-Script helps to extract translations from py files (pygettext analog)'
    )
    parser.add_argument(
        '-o', '--outfile',
        help='output .pot file'
    )
    parser.add_argument(
        '-d', '--domain',
        help='domain (by default = base)',
        default='base'
    )
    parser.add_argument(
        '-p', '--prefix',
        help='translate func name (by default = _)',
        default='_'
    )
    parser.add_argument(
        '-v', '--verbose',
        help='verbose',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-e', '--expression',
        help='regular expression',
        default=None
    )
    parser.add_argument(
        '-l', '--location',
        help='add detection location (filepath)',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-i', '--ignore',
        help='file or dir names to ignore',
        nargs='+',
        default=()
    )
    parser.add_argument(
        'target',
        help='input directory or file',

    )

    return parser.parse_args()


def extract_from_file(path: Path):
    if path.name in to_ignore:
        return ()
    elif path.suffix != '.py':
        return ()

    log_pos(f'Working on {path}')

    with open(path, 'r', encoding='utf-8') as sf:
        cont = sf.read()

        result = re.findall(pattern, cont)
        log_pos(f'Found: {len(result)}')
        if progargs.location:
            location = str(path.relative_to(progargs.target))
        else:
            location = None
        return map(lambda k: Translation(k, location), result)


def extract_from_dir(path: Path):
    if path.name in to_ignore:
        return ()
    log_pos(f'Working on {path}')
    for file in path.iterdir():
        if file.is_file():
            for key in extract_from_file(file):
                yield key
        else:
            for key in extract_from_dir(file):
                yield key


def extract():
    log_pos('Extracting...')
    target_path = Path(progargs.target)
    if target_path.is_file():
        return extract_from_file(target_path)
    else:
        log_pos('Using recursive mode')
        return extract_from_dir(target_path)


def gen_default_pot(path):
    py_loc = Path(sys.exec_prefix)
    log_pos(f'Python located at {py_loc}')
    pygettext_path = py_loc / 'Tools/i18n/pygettext.py'

    temp_file = f'empty{random.randint(1, 100000000000)}.py'
    with open(temp_file, 'w') as ef:
        pass
    command = f'python {pygettext_path} -d {progargs.domain} -o {path} ' \
              f'{temp_file}'

    log_pos(f'Generating default .pot with command: {command}')
    os.system(command)
    os.remove(temp_file)


def save_pot(translations):
    path = Path(progargs.outfile or progargs.domain + ".pot").absolute()
    gen_default_pot(path)

    with open(path, 'a') as pf:
        for translation in translations:
            pf.write('\n')
            if progargs.location:
                pf.write(f'# {translation.location}\n')
            pf.write(f'msgid "{translation.key}"\n')
            pf.write(f'msgstr ""\n')
    log_pos(f'Done. Saved to {path}')


def main():
    save_pot(extract())


if __name__ == '__main__':
    progargs = parse_args()
    pattern = progargs.expression or fr'\W\{progargs.prefix}\(["\'](.*)["\'][\),]'
    to_ignore = set(progargs.ignore) or set()
    to_ignore.update(('venv', '.idea', '.git', '__pycache__'))
    log_pos(f'Ignoring names: {", ".join(to_ignore)}')
    log_pos(f'Regexp: {pattern}')
    main()
