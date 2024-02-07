from .enums import TranslatableEnum
from .. import clsutils


def extract_ids() -> set[str]:
    ids = set()
    for subenum in clsutils.iter_subclasses(TranslatableEnum):
        for item in subenum:
            msgid = item.value
            ids.add(msgid)
    return ids
