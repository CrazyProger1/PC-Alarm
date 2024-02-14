import asyncio

import flet as ft

from i18n import set_language

from src.core.languages import (
    get_available_languages
)
from src.utils.events import (
    EventChannel
)
from .enums import (
    ConfiguratorMessage,
    PubSubEvent
)


class CustomControl(ft.UserControl):
    events = EventChannel()

    def __init__(self, arguments, settings):
        super().__init__()

        self._arguments = arguments
        self._settings = settings

        self.events.subscribe(self.translate, PubSubEvent.LANGUAGE_CHANGED)
        self.events.subscribe(self.update_sync_to_async, PubSubEvent.LANGUAGE_CHANGED)
        self.events.subscribe(self.save, PubSubEvent.SAVE)

        self.translate()

    def update_sync_to_async(self):
        asyncio.create_task(self.update_async())

    def translate(self):
        pass

    def save(self):
        pass


class TokenBox(CustomControl):
    def __init__(self, *args, **kwargs):
        self._telegram_token_text = ft.Text()
        self._telegram_token_field = ft.TextField(
            hint_text='token'
        )

        self._content = ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        self._telegram_token_text,
                        self._telegram_token_field
                    ]
                )
            ]
        )

        super().__init__(*args, **kwargs)

    def translate(self):
        self._telegram_token_text.value = str(ConfiguratorMessage.TELEGRAM_TOKEN)
        self._telegram_token_field.value = self._settings.env.bot_token

    def save(self):
        token = self._telegram_token_field.value
        self._settings.env.bot_token = token

    def build(self):
        return self._content


class TelegramIDBox(CustomControl):
    def __init__(self, *args, **kwargs):
        self._telegram_id_text = ft.Text()
        self._telegram_id_field = ft.TextField(hint_text='id')

        self._content = ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        self._telegram_id_text,
                        self._telegram_id_field
                    ]
                )
            ]
        )
        super().__init__(*args, **kwargs)

    def translate(self):
        self._telegram_id_text.value = str(ConfiguratorMessage.TELEGRAM_USERID)
        self._telegram_id_field.value = self._settings.env.admin_id

    def save(self):
        self._settings.env.admin_id = int(self._telegram_id_field.value)

    def build(self):
        return self._content


class LanguageBox(CustomControl):
    def __init__(self, *args, **kwargs):
        self._language_text = ft.Text()
        self._language_dropdown = ft.Dropdown(
            on_change=self._handle_changed,
        )
        self._content = ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        self._language_text,
                        self._language_dropdown
                    ]
                )
            ]
        )

        self._languages = {}
        self._load_languages()

        super().__init__(*args, **kwargs)

    def _load_languages(self):
        for language in get_available_languages():
            self._languages[ConfiguratorMessage.LANGUAGE_NAME.language(language)] = language

        self._language_dropdown.options = [
            ft.dropdown.Option(option) for option in self._languages.keys()
        ]

    async def _handle_changed(self, event: ft.ControlEvent):
        language = self._languages.get(event.data)
        set_language(language)
        self.events.publish(PubSubEvent.LANGUAGE_CHANGED)

    def translate(self):
        self._language_text.value = str(ConfiguratorMessage.LANGUAGE)
        asyncio.create_task(self._language_text.update_async())

    def save(self):
        language = self._languages.get(self._language_dropdown.value, 'en')
        self._settings.configurator.language = language

    def build(self):
        return self._content


class ActionPanel(CustomControl):

    def __init__(self, *args, **kwargs):
        self._button_save = ft.TextButton(
            expand=True,
            height=50,
            on_click=self._handle_save
        )
        self._content = ft.Row(
            expand=True,
            controls=[
                self._button_save
            ]
        )
        super().__init__(*args, **kwargs)

    def _handle_save(self, event):
        self.events.publish(PubSubEvent.SAVE)

    def translate(self):
        self._button_save.text = str(ConfiguratorMessage.SAVE)

    def build(self):
        return self._content
