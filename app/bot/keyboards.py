from .types import ReplyKeyboard, InlineKeyboard


class MainReplyKeyboard(ReplyKeyboard):
    buttons = [
        'Settings',
        'Interaction'
    ]

    row_width = 2
