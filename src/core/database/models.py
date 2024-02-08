import peewee

from src.settings import (
    OWNER_GROUP,
    ADMIN_GROUP
)
from .constants import (
    MAX_GROUP_NAME_LENGTH,
    MAX_LANGUAGE_NAME_LENGTH
)


class Group(peewee.Model):
    name = peewee.CharField(max_length=MAX_GROUP_NAME_LENGTH, primary_key=True)


class Languages(peewee.Model):
    name = peewee.CharField(max_length=MAX_LANGUAGE_NAME_LENGTH, primary_key=True)


class Users(peewee.Model):
    id = peewee.IntegerField(primary_key=True)
    language = peewee.ForeignKeyField(Languages, on_delete='CASCADE', on_update='CASCADE')
    group = peewee.ForeignKeyField(Group, on_delete='CASCADE', on_update='CASCADE')
    alarm_active = peewee.BooleanField(default=False)

    @property
    def is_owner(self) -> bool:
        return self.group.name in (ADMIN_GROUP, OWNER_GROUP)

    @property
    def is_admin(self) -> bool:
        return self.group.name == ADMIN_GROUP
