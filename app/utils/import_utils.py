import importlib
import importlib.util
import os.path

_imported = {}


def _import_module_by_filepath(module_name: str, filepath: str):
    if not os.path.exists(filepath):
        return None
    try:
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        imported_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(imported_module)
        return imported_module
    except AttributeError:
        return None


def _import_module_by_alternative_path(path: str, sep='.'):
    try:
        components = path.split(sep)
        imported_module = __import__(components[0])
        for comp in components[1:]:
            imported_module = getattr(imported_module, comp)
        return imported_module
    except AttributeError:
        return None


def import_module(path: str):
    if path in _imported.keys():
        return _imported.get(path)

    imported_module = _import_module_by_alternative_path(path, sep='.')
    if not imported_module:
        module_name = path.split('.')[-1]
        filepath = path.replace('.', '\\')

        for possible_filepath in (filepath, filepath + '.py', filepath + '\\__init__.py'):
            imported_module = _import_module_by_filepath(module_name, possible_filepath)
            if imported_module:
                break

    if not imported_module:
        raise ModuleNotFoundError(f'Module "{path}" not found!', path=path)
    return imported_module