import inspect
from types import ModuleType

import pytest

from src.utils.imputils import (
    import_module_by_filepath,
    import_class_by_filepath
)


def test_import_module_by_filepath():
    module = import_module_by_filepath('tests/resources/imports/test.py')

    assert isinstance(module, ModuleType)
    assert hasattr(module, 'TestClass')


def test_import_class_by_filepath():
    cls = import_class_by_filepath(
        'tests/resources/imports/test.py',
        class_name='TestClass'
    )

    assert inspect.isclass(cls)


def test_import_unexisting_module_by_filepath():
    with pytest.raises(ImportError):
        import_module_by_filepath('nothing')
