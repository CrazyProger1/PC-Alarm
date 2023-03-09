from aiogram import types

from app.bot import events
from app.database import Users
from .keyboards import *
from .permissions import IsNotBanned
from .types import Page, Keyboard, Executor, Command


class BasePage(Page):
    path = 'base'
    permission_classes = (
        IsNotBanned,
    )

    page_transfers: dict[str, str] = {}

    def __init__(self, *args, **kwargs):
        super(BasePage, self).__init__(*args, **kwargs)
        self.add_callback(events.INIT, self.on_initialize)

        # MainReplyKeyboard().add_callback(events.BUTTON_CLICKED, self.on_button_clicked)  # only for MainReplyKeyboard
        self.add_callback(events.BUTTON_CLICKED, self.on_button_clicked)  # for all keyboards

    @staticmethod
    async def execute_command(command, **kwargs):
        executor = Executor.get(command)
        await executor.execute(command, **kwargs)

    async def on_initialize(self, user: Users, **kwargs):
        await self.keyboards[0].show(user)

    async def on_button_clicked(self, keyboard: Keyboard, button: str, user: Users, message: types.Message, **kwargs):
        if button == 'Back':
            await self.back(user)
            return

        next_page = self.page_transfers.get(button)

        if next_page:
            await self.next(user, next_page)


class MainPage(BasePage):
    path = 'main'
    default = True

    keyboard_classes = (
        MainReplyKeyboard,
    )

    page_transfers = {
        'Interaction': 'interaction',
        'Settings': 'settings'
    }

    async def turn_on_alarm(self, **kwargs):
        await self.execute_command(Command('turn_on_alarm', []), **kwargs)

    async def turn_off_alarm(self, **kwargs):
        await self.execute_command(Command('turn_off_alarm', []), **kwargs)

    async def on_button_clicked(self, keyboard: Keyboard, button: str, user: Users, message: types.Message, **kwargs):
        await super(MainPage, self).on_button_clicked(keyboard, button, user, message, **kwargs)

        match button:
            case 'Turn ON Alarm':
                await self.turn_on_alarm(
                    user=user,
                    message=message,
                    **kwargs
                )
            case 'Turn OFF Alarm':
                await self.turn_off_alarm(
                    user=user,
                    message=message,
                    **kwargs
                )


class SettingsPage(BasePage):
    path = 'main.settings'

    keyboard_classes = (
        SettingsReplyKeyboard,
    )


class InteractionPage(BasePage):
    path = 'main.interaction'

    keyboard_classes = (
        InteractionReplyKeyboard,
    )
