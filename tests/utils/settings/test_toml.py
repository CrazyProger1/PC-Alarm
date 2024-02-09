import pytest
from pydantic import BaseModel

from src.utils.settings import TOMLLoader

TEST_FILE = 'tests/resources/test.toml'


def create_file(content, file=TEST_FILE):
    with open(file, 'w') as f:
        f.write(content)


def test_load():
    create_file('test_1 = 1')

    class Schema(BaseModel):
        test_1: int

    loader = TOMLLoader()

    data = loader.load(TEST_FILE, schema=Schema)

    assert data.test_1 == 1


def test_save():
    class Schema(BaseModel):
        test_1: int

    loader = TOMLLoader()
    loader.save(TEST_FILE, instance=Schema(test_1=123))

    data = loader.load(TEST_FILE, schema=Schema)

    assert data.test_1 == 123



def test_load_section():
    create_file('''
test_1 = 1

[section]
test_2 = 'abc'
''')

    class Section(BaseModel):
        test_2: str

    class Schema(BaseModel):
        test_1: int
        section: Section

    loader = TOMLLoader()

    data = loader.load(TEST_FILE, schema=Schema)

    assert data.section.test_2 == 'abc'


def test_file_not_found():
    class Schema(BaseModel):
        test_1: int

    loader = TOMLLoader()

    with pytest.raises(FileNotFoundError):
        loader.load('abcd', schema=Schema)