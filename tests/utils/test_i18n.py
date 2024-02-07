import gettext
import os

from src.utils.i18n import (
    extract_ids,
    TranslatableEnum
)

gettext.bindtextdomain('main', 'tests/resources/i18n/')
gettext.textdomain('main')
os.environ['LANG'] = 'en_US'


class FirstTranslatableEnum(TranslatableEnum):
    TEST = 'test'
    ABC = 'abc'
    BBC = 'bbc'


def test_extract_ids():
    ids = tuple(extract_ids())

    assert len(ids) == 3


def test_translatable_enum():
    assert FirstTranslatableEnum.TEST.value == gettext.gettext('test')
    assert FirstTranslatableEnum.ABC.value == gettext.gettext('abc')
    assert FirstTranslatableEnum.BBC.value == gettext.gettext('bbc')
