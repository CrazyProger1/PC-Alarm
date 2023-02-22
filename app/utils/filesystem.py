from pathlib import Path


def check_file(path: str):
    file = Path(path)

    if not file.exists():
        raise FileExistsError(f'File does not exists: {path}')

    if not file.is_file():
        raise ValueError(f'Not a file: {path}')


def read(path: str, mode: str = 'r'):
    check_file(path)
    with open(path, mode) as f:
        return f.read()


def write(path: str, data: bytes | str, mode: str = 'w'):
    with open(path, mode) as f:
        return f.write(data)