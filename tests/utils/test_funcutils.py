import pytest

from src.utils.funcutils import guard


@guard
def my_func(test: int):
    pass


@guard(ignore=('test',))
def my_func2(test: int):
    return test


def test_guard():
    with pytest.raises(TypeError):
        my_func('123')


def test_guard_ignore():
    assert my_func2('123') == '123'
