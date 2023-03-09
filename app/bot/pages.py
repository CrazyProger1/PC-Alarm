from aiogram import types
from app.database import Users
from app.utils.translator import _
from app.bot import events
from .types import Page, Keyboard
from .permissions import IsNotBanned
from .keyboards import *


class MainPage(Page):
    path = 'main'
    default = True
    permission_classes = (
        IsNotBanned,
    )
    keyboard_classes = (
        MainReplyKeyboard,
    )

    def __init__(self, *args, **kwargs):
        super(MainPage, self).__init__(*args, **kwargs)
        self.add_callback(events.INIT, self.on_initialize)

        # MainReplyKeyboard().add_callback(events.BUTTON_CLICKED, self.on_button_clicked)  # only for MainReplyKeyboard
        self.add_callback(events.BUTTON_CLICKED, self.on_button_clicked)  # for all keyboards

    async def on_initialize(self, user: Users, **kwargs):
        await self.show_keyboard(user, MainReplyKeyboard)  # == await MainReplyKeyboard().show(user)

    async def on_button_clicked(self, keyboard: Keyboard, button: str, user: Users, message: types.Message, **kwargs):
        if isinstance(keyboard, MainReplyKeyboard):
            print(button)
