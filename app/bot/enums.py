from enum import Enum


class ContentType(Enum):
    MESSAGE = 1
    COMMAND = 2
    MEDIA = 3
    CALLBACK = 4
