import flet as ft

from .enums import (
    ConfiguratorMessage,
    PubSubMessage
)


class CustomControl(ft.UserControl):
    def __init__(self, arguments, settings):
        super().__init__()

        self._arguments = arguments
        self._settings = settings
        self.translate()

    async def _on_message(self, message: str):
        match message:
            case PubSubMessage.LANGUAGE_CHANGED:
                self.translate()
                await self.update_async()

    def translate(self):
        pass

    async def did_mount_async(self):
        await self.page.pubsub.subscribe_async(self._on_message)


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
        self._telegram_token_text.value = ConfiguratorMessage.TELEGRAM_TOKEN

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
        self._telegram_id_text.value = ConfiguratorMessage.TELEGRAM_USERID

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
        super().__init__(*args, **kwargs)

    async def _handle_changed(self, event: ft.ControlEvent):
        await self.page.pubsub.send_all_async(PubSubMessage.LANGUAGE_CHANGED)

    def translate(self):
        self._language_dropdown.options = [
            ft.dropdown.Option('English'),
            ft.dropdown.Option('Ukrainian'),
            ft.dropdown.Option('Somalian'),
        ]
        self._language_text.value = ConfiguratorMessage.LANGUAGE

    def build(self):
        return self._content


class ActionPanel(CustomControl):

    def __init__(self, *args, **kwargs):
        self._button_save = ft.TextButton(
            expand=True,
            height=50,
        )
        self._content = ft.Row(
            expand=True,
            controls=[
                self._button_save
            ]
        )
        super().__init__(*args, **kwargs)

    def translate(self):
        self._button_save.text = ConfiguratorMessage.SAVE

    def build(self):
        return self._content
