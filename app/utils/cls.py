from .import_utils import import_module


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Customizable:
    cls_path: str = None

    def __new__(cls, *args, **kwargs):
        if cls in Customizable.__subclasses__() and cls.cls_path:
            subclass = import_module(cls.cls_path)
            if issubclass(subclass, Customizable):
                return subclass(*args, **kwargs)

        new_instance = super(Customizable, cls).__new__(cls, *args, **kwargs)
        return new_instance
