import inspect
import os.path
from types import ModuleType

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
