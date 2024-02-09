import os

import pytest
from pydantic import BaseModel, Field

from src.utils.settings import ENVLoader

TEST_FILE = 'tests/resources/test.env'


def create_file(content):
    with open(TEST_FILE, 'w') as f:
        f.write(content)


def test_load_str():
    create_file('token=hello_world')

    class Schema(BaseModel):
        token: str

    loader = ENVLoader()

    data = loader.load(TEST_FILE, Schema)

    assert data.token == 'hello_world'


def test_load_int():
    create_file('integer=123')

    class Schema(BaseModel):
        integer: int

    loader = ENVLoader()

    data = loader.load(TEST_FILE, Schema)

    assert data.integer == 123


def test_load_bool():
    create_file('boolean_true=True\nboolean_false=False')

    class Schema(BaseModel):
        boolean_true: bool
        boolean_false: bool

    loader = ENVLoader()

    data = loader.load(TEST_FILE, Schema)

    assert data.boolean_true is True
    assert data.boolean_false is False


def test_save_str():
    class Schema(BaseModel):
        token: str

    loader = ENVLoader()

    instance = Schema(token='123321')

    loader.save(TEST_FILE, instance)

    data = loader.load(TEST_FILE, Schema)

    assert data.token == '123321'


def test_file_not_found():
    loader = ENVLoader()

    class Schema(BaseModel):
        token: str

    with pytest.raises(FileNotFoundError):
        loader.load('abcd', Schema)
