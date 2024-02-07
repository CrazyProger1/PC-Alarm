from typing import Iterable

import flet as ft

from src.settings import (
    TITLE,
    WINDOW_SIZE
)
from .controls import (
    TokenFieldControl,
    TelegramIDFiledControl,
    LanguageChoiceControl,
    ActionPanelControl
)


def setup_page(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.window_max_width = WINDOW_SIZE[0]
    page.window_max_height = WINDOW_SIZE[1]
    page.window_width = WINDOW_SIZE[0]
    page.window_height = WINDOW_SIZE[1]
    page.window_min_width = WINDOW_SIZE[0]
    page.window_min_height = WINDOW_SIZE[1]
    page.title = TITLE


def setup_gui() -> Iterable[ft.Control]:
    token_field = TokenFieldControl()
    telegram_id_field = TelegramIDFiledControl()
    language_choice = LanguageChoiceControl()
    action_panel = ActionPanelControl()
    return [
        ft.Column(
            expand=True,
            controls=[
                token_field,
                telegram_id_field,
                language_choice,
                action_panel
            ]
        )
    ]


async def gui(page: ft.Page):
    setup_page(page=page)
    controls = setup_gui()
    await page.add_async(*controls)
