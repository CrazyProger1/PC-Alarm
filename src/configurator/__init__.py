import flet as ft

from .gui import gui


async def run_configurator():
    await ft.app_async(
        target=gui
    )


__all__ = [
    'run_configurator'
]
