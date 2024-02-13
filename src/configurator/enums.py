from enum import Enum

from i18n import TranslatableEnum


class ConfiguratorMessage(TranslatableEnum):
    TELEGRAM_TOKEN = 'Telegram Bot Token'
    TELEGRAM_USERID = 'Telegram Admin-User ID'
    LANGUAGE = 'Language'
    SAVE = 'Save'


class PubSubMessage(Enum):
    LANGUAGE_CHANGED = 'language_changed'
