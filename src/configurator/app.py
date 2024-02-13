import flet as ft
from i18n import set_language

from src.types import BaseApplication
from src.settings import (
    TITLE,
    WINDOW_SIZE
)
from src.core.logging import logger
from src.core.schemas import (
    Arguments,
    Settings
)
from .factories import GUIFactory
from .types import BaseGUIFactory


class Configurator(BaseApplication):
    def __init__(self, arguments: Arguments, settings: Settings):
        set_language(settings.configurator.language)

        self._gui_factory: BaseGUIFactory = GUIFactory(
            arguments=arguments,
            settings=settings
        )
        super().__init__(arguments, settings)

    def _setup_page(self, page: ft.Page):
        page.theme_mode = ft.ThemeMode.DARK
        page.window_max_width = WINDOW_SIZE[0]
        page.window_max_height = WINDOW_SIZE[1]
        page.window_width = WINDOW_SIZE[0]
        page.window_height = WINDOW_SIZE[1]
        page.window_min_width = WINDOW_SIZE[0]
        page.window_min_height = WINDOW_SIZE[1]
        page.title = TITLE

    async def _gui(self, page: ft.Page):
        self._setup_page(page=page)
        main_control = self._gui_factory.create_gui()
        logger.info('GUI initialized')
        await page.add_async(main_control)

    async def run(self):
        await ft.app_async(
            target=self._gui
        )
        logger.info('GUI destroyed')
