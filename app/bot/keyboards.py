from .types import ReplyKeyboard, InlineKeyboard
from .keys import *


class MainReplyKeyboard(ReplyKeyboard):
    buttons = [
        'Settings',
        'Interaction'
    ]

    row_width = 2
    caption_key = MAIN_REPLY_KEYBOARD_CAPTION_KEY
