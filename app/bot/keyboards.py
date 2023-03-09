from .types import ReplyKeyboard, InlineKeyboard
from .keys import *


class MainReplyKeyboard(ReplyKeyboard):
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
    caption_key = MAIN_REPLY_KEYBOARD_CAPTION_KEY


class SettingsReplyKeyboard(ReplyKeyboard):
    buttons = (
        'Back',
    )
    row_width = 2
    caption_key = SETTINGS_REPLY_KEYBOARD_CAPTION_KEY


class InteractionReplyKeyboard(ReplyKeyboard):
    buttons = (
        'Shutdown PC',
        'Restart PC',
        'End Session',
        'Say',
        'Music',
        'Noise',
        'Back'
    )
    row_width = 3
    caption_key = INTERACTION_REPLY_KEYBOARD_CAPTION_KEY
