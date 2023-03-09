from app.database import Users
from app.utils.translator import _
from app.bot import events
from .types import Page
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

    async def on_initialize(self, user: Users, **kwargs):
        await self.show_keyboard(user, MainReplyKeyboard)  # == await MainReplyKeyboard().show(user)
