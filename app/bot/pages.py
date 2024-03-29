from app.bot import events
from app.utils import filesystem

from .keyboards import *
from .permissions import *
from .types import Page, Keyboard, Executor, Command


class BasePage(Page):
    path = 'base'
    permission_classes = (
        IsNotBanned,
        IsOwnerOrAdminOrHigher
    )

    page_transfers: dict[str, str] = {}

    def __init__(self, *args, **kwargs):
        super(BasePage, self).__init__(*args, **kwargs)
        self.add_callback(events.INIT, self.on_initialize)
        self.add_callback(events.DESTROY, self.on_destroy)
        self.add_callback(events.BUTTON_CLICKED, self.on_button_clicked)

    @staticmethod
    async def execute_command(text_command: str, *args, **kwargs):
        command = Command(text_command, args)
        executor = Executor.get(command)
        if executor:
            return await executor.execute(command, **kwargs)

    async def on_initialize(self, user: Users, **kwargs):
        await self.keyboards[0].show(user)

    async def on_destroy(self, user: Users, **kwargs):
        await self.keyboards[0].hide(user)

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
        MainPageReplyKeyboard,
    )

    page_transfers = {
        'Interaction': 'interaction',
        'Settings': 'settings',
        'Add Owner': 'add_owner'
    }

    async def on_button_clicked(self, keyboard: Keyboard, button: str, user: Users, message: types.Message, **kwargs):
        await super(MainPage, self).on_button_clicked(keyboard, button, user, message, **kwargs)

        commands = {
            'Turn ON Alarm': 'turn_on_alarm',
            'Turn OFF Alarm': 'turn_off_alarm',
            'Make Photo': 'photo',
            'Make Screenshot': 'screenshot'
        }
        kwgs = {'user': user, 'message': message}
        args = []

        command = commands.get(button)

        if command:
            await self.execute_command(command, *args, **kwgs)


class SettingsPage(BasePage):
    path = 'main.settings'

    keyboard_classes = (
        SettingsPageReplyKeyboard,
    )
    page_transfers = {
        'Language': 'language'
    }


class InteractionPage(BasePage):
    path = 'main.interaction'

    keyboard_classes = (
        InteractionPageReplyKeyboard,
    )
    page_transfers = {
        'Say': 'say',
        'Music': 'music',
        'Beep': 'beep'
    }

    async def on_button_clicked(self, keyboard: Keyboard, button: str, user: Users, message: types.Message, **kwargs):
        await super(InteractionPage, self).on_button_clicked(keyboard, button, user, message, **kwargs)

        commands = {
            'Shutdown PC': 'shutdown',
            'Restart PC': 'restart',
            'End Session': 'end_session'
        }
        kwgs = {'user': user, 'message': message}
        args = []

        command = commands.get(button)

        if command:
            await self.execute_command(command, *args, **kwgs)


class SayPage(BasePage):
    path = 'main.interaction.say'

    keyboard_classes = (
        SayPageReplyKeyboard,
    )

    def __init__(self, *args, **kwargs):
        super(SayPage, self).__init__(*args, **kwargs)
        self.add_callback(events.MESSAGE, self.on_message)

    async def on_message(self, message: types.Message, user: Users, **kwargs):
        if self.keyboards[0].get_pressed(message.text, user.language) == 'Back':
            return
        await self.execute_command('say', message.text, message=message, user=user)


class MusicPage(BasePage):
    path = 'main.interaction.music'
    keyboard_classes = (
        MusicPageReplyKeyboard,
    )

    def __init__(self, *args, **kwargs):
        super(MusicPage, self).__init__(*args, **kwargs)
        self.add_callback(events.MEDIA, self.on_media)

    async def on_media(self, message: types.Message, user: Users, **kwargs):
        if message.content_type in {'voice', 'audio'}:
            if message.content_type == 'voice':
                file = await message.voice.get_file()

                path = filesystem.safe_filename('.ogg', 'sound')
            else:
                file = await message.audio.get_file()
                path = filesystem.safe_filename('.mp3', 'sound')

            await self.bot.download_file(file.file_path, destination=path)
            await self.execute_command('music', path, user=user, message=message)


class BeepPage(BasePage):
    path = 'main.interaction.beep'
    keyboard_classes = (
        BeepPageReplyKeyboard,
    )

    def __init__(self, *args, **kwargs):
        super(BeepPage, self).__init__(*args, **kwargs)
        self.add_callback(events.MESSAGE, self.on_message)

    async def on_message(self, message: types.Message, user: Users, **kwargs):
        text = message.text.strip().split(' ')[0]
        if text.isdigit():
            await self.execute_command('beep', int(text), user=user, message=message)


class LanguagePage(BasePage):
    path = 'main.settings.language'
    keyboard_classes = (
        LanguagePageReplyKeyboard,
        LanguageSelectingInlineKeyboard
    )

    def __init__(self, *args, **kwargs):
        super(LanguagePage, self).__init__(*args, **kwargs)
        self.add_callback(events.CALLBACK, self.on_callback)

    async def on_initialize(self, user: Users, **kwargs):
        await super(LanguagePage, self).on_initialize(user, **kwargs)
        await self.show_keyboard(user, LanguageSelectingInlineKeyboard)

    async def on_destroy(self, user: Users, **kwargs):
        await super(LanguagePage, self).on_destroy(user, **kwargs)
        await self.hide_keyboard(user, LanguageSelectingInlineKeyboard)

    async def on_callback(self, callback: types.CallbackQuery, user: Users, **kwargs):
        await self.execute_command('set', 'language', callback.data, user=user, message=None)


class OwnerAddingPage(BasePage):
    path = 'main.add_owner'
    keyboard_classes = (
        OwnerAddingPageReplyKeyboard,
    )
    permission_classes = (
        IsAdmin,
    )

    def __init__(self, *args, **kwargs):
        super(OwnerAddingPage, self).__init__(*args, **kwargs)
        self.add_callback(events.MESSAGE, self.on_message)

    async def on_message(self, message: types.Message, user: Users, **kwargs):
        if self.keyboards[0].get_pressed(message.text, user.language) == 'Back':
            return
        await self.execute_command('add_owner', message.text, user=user, message=message)
