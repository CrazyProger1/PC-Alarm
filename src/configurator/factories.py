import flet as ft

from .types import BaseGUIFactory
from .controls import (
    TokenBox,
    TelegramIDBox,
    LanguageBox,
    ActionPanel
)


class GUIFactory(BaseGUIFactory):
    def create_token_box(self) -> ft.Control:
        return TokenBox(
            arguments=self._arguments,
            settings=self._settings
        )

    def create_telegram_id_box(self) -> ft.Control:
        return TelegramIDBox(
            arguments=self._arguments,
            settings=self._settings
        )

    def create_language_box(self) -> ft.Control:
        return LanguageBox(
            arguments=self._arguments,
            settings=self._settings
        )

    def create_action_panel(self) -> ft.Control:
        return ActionPanel(
            arguments=self._arguments,
            settings=self._settings
        )

    def create_gui(self) -> ft.Control:
        return ft.Column(
            expand=True,
            controls=[
                self.create_token_box(),
                self.create_telegram_id_box(),
                self.create_language_box(),
                self.create_action_panel()
            ]
        )
