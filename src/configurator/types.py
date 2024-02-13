from abc import ABC, abstractmethod

import flet as ft

from src.core.schemas import (
    Arguments,
    Settings
)


class BaseGUIFactory(ABC):
    def __init__(self, arguments: Arguments, settings: Settings):
        self._arguments = arguments
        self._settings = settings

    @abstractmethod
    def create_token_box(self) -> ft.Control: ...

    @abstractmethod
    def create_telegram_id_box(self) -> ft.Control: ...

    @abstractmethod
    def create_language_box(self) -> ft.Control: ...

    @abstractmethod
    def create_action_panel(self) -> ft.Control: ...

    @abstractmethod
    def create_gui(self) -> ft.Control: ...
