import flet as ft

from .enums import ConfiguratorMessages


class TokenFieldControl(ft.UserControl):
    def build(self):
        return ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Text(ConfiguratorMessages.TELEGRAM_TOKEN),
                        ft.TextField(hint_text='token')
                    ]
                )
            ]
        )


class TelegramIDFiledControl(ft.UserControl):
    def build(self):
        return ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Text(ConfiguratorMessages.TELEGRAM_USERID),
                        ft.TextField(hint_text='id')
                    ]
                )
            ]
        )


class LanguageChoiceControl(ft.UserControl):
    def build(self):
        return ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    controls=[
                        ft.Text(ConfiguratorMessages.LANGUAGE),
                        ft.Dropdown(
                            options=[
                                ft.dropdown.Option('English'),
                                ft.dropdown.Option('Ukrainian'),
                                ft.dropdown.Option('Somalian'),
                            ],
                        )
                    ]
                )
            ]
        )


class ActionPanelControl(ft.UserControl):
    def build(self):
        return ft.Row(
            expand=True,
            controls=[ft.TextButton(
                text=ConfiguratorMessages.SAVE,
                expand=True,
                height=50,
            ), ]
        )
