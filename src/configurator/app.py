import flet as ft
from src.types import BaseApplication
from .gui import gui


class Configurator(BaseApplication):
    async def run(self):
        await ft.app_async(
            target=gui
        )
