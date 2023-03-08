import peewee
import functools

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
    short_name = peewee.CharField(max_length=SHORT_LANG_NAME, primary_key=True)
    full_name = peewee.CharField(max_length=FULL_LANG_NAME)

    @staticmethod
    @functools.cache
    def get_default():
        return Languages.get_by_id('en')


class Categories(Model):
    name = peewee.CharField(max_length=CATEGORY_NAME, primary_key=True)
    access_level = peewee.IntegerField()

    @staticmethod
    @functools.cache
    def get_default():
        return Categories.get_by_id('Anonymous')

    @staticmethod
    @functools.cache
    def get_admin():
        return Categories.get_by_id('Admin')

    @staticmethod
    @functools.cache
    def get_banned():
        return Categories.get_by_id('Banned')


class Users(Model):
    id = peewee.IntegerField(primary_key=True)
    username = peewee.CharField(USERNAME)
    first_name = peewee.CharField(FIRST_NAME)
    last_name = peewee.CharField(LAST_NAME, null=True)
    language = peewee.ForeignKeyField(Languages, on_delete='SET DEFAULT', default=Languages.get_default)
    category = peewee.ForeignKeyField(Categories, on_delete='SET DEFAULT', default=Categories.get_default)

    def is_admin(self):
        return self.category == Categories.get_admin()

    def is_banned(self):
        return self.category == Categories.get_banned()
