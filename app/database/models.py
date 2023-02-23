import peewee

from .connection import connection
from .state import UserState
from .limits import *


class Model(peewee.Model):
    __instances = {}

    class Meta:
        database = connection

    def __new__(cls, *args, **kwargs):
        pk_field = cls._meta.primary_key.name
        pk_val = kwargs.pop(pk_field, None)

        instance = cls.__instances.get(pk_val)
        if instance:
            return instance
        new_instance = super(Model, cls).__new__(cls)
        new_instance.state = UserState()
        return new_instance

    def __setattr__(self, key, value):
        pk_field = self._meta.primary_key.name

        if key == pk_field:
            self.__instances.update({value: self})

        super(Model, self).__setattr__(key, value)


class Languages(Model):
    short_name = peewee.CharField(max_length=SHORT_LANG_NAME)
    full_name = peewee.CharField(max_length=FULL_LANG_NAME, primary_key=True)
    pack_file = peewee.CharField(max_length=LANG_PACK_FILE)

    @staticmethod
    def get_default():
        return Languages.get_by_id('English')


class Categories(Model):
    name = peewee.CharField(max_length=CATEGORY_NAME, primary_key=True)
    access_level = peewee.IntegerField()

    @staticmethod
    def get_default():
        return Categories.get_by_id('Anonymous')

    @staticmethod
    def get_admin():
        return Categories.get_by_id('Admin')


class Users(Model):
    id = peewee.IntegerField(primary_key=True)
    username = peewee.CharField(USERNAME)
    first_name = peewee.CharField(FIRST_NAME)
    last_name = peewee.CharField(LAST_NAME, null=True)
    language = peewee.ForeignKeyField(Languages, on_delete='SET DEFAULT', default=Languages.get_default)
    category = peewee.ForeignKeyField(Languages, on_delete='SET DEFAULT', default=Categories.get_default)
