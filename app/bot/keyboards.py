from .types import ReplyKeyboard, InlineKeyboard
from .keys import *


class MainPageReplyKeyboard(ReplyKeyboard):
    buttons = (
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
    buttons = (
        'Back',
    )
    row_width = 2
    caption_key = SETTINGS_PAGE_REPLY_KEYBOARD_CAPTION_KEY


class InteractionPageReplyKeyboard(ReplyKeyboard):
    buttons = (
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
    buttons = (
        'Back',
    )
    row_width = 1
    caption_key = SAY_PAGE_REPLY_KEYBOARD_CAPTION_KEY


class MusicPageReplyKeyboard(ReplyKeyboard):
    buttons = (
        'Back',
    )

    row_width = 1
    caption_key = MUSIC_PAGE_REPLY_KEYBOARD_CAPTION_KEY


class BeepPageReplyKeyboard(ReplyKeyboard):
    buttons = (
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
