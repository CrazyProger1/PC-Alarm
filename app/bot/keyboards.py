from .keys import *
from .types import ReplyKeyboard, InlineKeyboard


class MainPageReplyKeyboard(ReplyKeyboard):
    button_keys = (
        'Settings',
        'Add Owner',
        'Turn ON Alarm',
        'Turn OFF Alarm',
        'Make Photo',
        'Make Screenshot',
        'Interaction'
    )

    row_width = 2
    caption_key = MAIN_PAGE_REPLY_KEYBOARD_CAPTION_KEY


class SettingsPageReplyKeyboard(ReplyKeyboard):
    button_keys = (
        'Language',
        'Back'

    )
    row_width = 1
    caption_key = SETTINGS_PAGE_REPLY_KEYBOARD_CAPTION_KEY


class InteractionPageReplyKeyboard(ReplyKeyboard):
    button_keys = (
        'Shutdown PC',
        'Restart PC',
        'End Session',
        'Say',
        'Music',
        'Beep',
        'Back'
    )
    row_width = 3
    caption_key = INTERACTION_PAGE_REPLY_KEYBOARD_CAPTION_KEY


class SayPageReplyKeyboard(ReplyKeyboard):
    button_keys = (
        'Back',
    )
    row_width = 1
    caption_key = SAY_PAGE_REPLY_KEYBOARD_CAPTION_KEY


class MusicPageReplyKeyboard(ReplyKeyboard):
    button_keys = (
        'Back',
    )

    row_width = 1
    caption_key = MUSIC_PAGE_REPLY_KEYBOARD_CAPTION_KEY


class BeepPageReplyKeyboard(ReplyKeyboard):
    button_keys = (
        '20000 mHz',
        '18000 mHz',
        '15000 mHz',
        '13000 mHz',
        '10000 mHz',
        '5000 mHz',
        'Back',
    )

    row_width = 2
    caption_key = BEEP_PAGE_REPLY_KEYBOARD_CAPTION_KEY


class LanguagePageReplyKeyboard(ReplyKeyboard):
    button_keys = (
        'Back',
    )

    row_width = 1
    caption_key = LANGUAGE_PAGE_REPLY_KEYBOARD_CAPTION_KEY


class LanguageSelectingInlineKeyboard(InlineKeyboard):
    pass
