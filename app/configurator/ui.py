# -*- coding: utf-8 -*-


# Form implementation generated from reading ui file 'configurator_design_2.ui'
#
# Created by: PyQt5 UI code generator 5.15.8
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import functools

from PyQt5 import QtCore, QtGui, QtWidgets
from app.settings import settings
from app.utils import logging, config
from app.utils.translator import _
from app.database import Languages


class Configurator(QtWidgets.QMainWindow):
    WINDOW_SIZE = (480, 332)
    MAIN_TEXT_STYLE = 'font: 8pt "Segoe Print";'
    TITLE_TEXT_STYLE = 'font: 14pt "Segoe Print";'
    WINDOW_STYLE = '''
QPushButton{
    background-color: rgb(0, 0, 0);
    color: rgb(0, 255, 0);
}
QComboBox{
    color: rgb(0, 255, 0);
}
QComboBox QAbstractItemView
{
    background-color: rgb(0, 0, 0);
    selection-background-color: rgb(100, 100, 100); 
    color: rgb(0, 255, 0);
}
QLabel{
    color: rgb(0, 255, 0);
}
QWidget{
    background-color: rgb(0, 0, 0);
}
QPushButton:hover{
    border: 1px solid rgb(0, 255, 0);
}
QPushButton:pressed{
    background-color: rgb(130, 130, 130);
}
QLineEdit{
    background-color: rgb(0, 0, 0);
    border: 1px dashed rgb(255, 255, 255);
    color: rgb(0, 255, 0);
}
QLineEdit:hover{
    border: 1px solid rgb(255, 255, 255);
}
QComboBox:hover{
    border: 1px solid rgb(255, 255, 255);
}
QListWidget{
    color: rgb(0, 255, 0);
    background-color: rgb(0, 0, 0);
    font: 8pt "Segoe Print";
    border: 1px dashed rgb(255, 255, 255);
}'''

    def __init__(self):
        super(Configurator, self).__init__()
        self.central_widget = QtWidgets.QWidget(self)
        self.save_button = QtWidgets.QPushButton(self.central_widget)
        self.token_line = QtWidgets.QLineEdit(self.central_widget)
        self.admin_tgid_line = QtWidgets.QLineEdit(self.central_widget)
        self.token_label = QtWidgets.QLabel(self.central_widget)
        self.admin_tgid_label = QtWidgets.QLabel(self.central_widget)
        self.program_label = QtWidgets.QLabel(self.central_widget)
        self.language_selecting = QtWidgets.QComboBox(self.central_widget)
        self.language_label = QtWidgets.QLabel(self.central_widget)
        self._setup()

    def _setup(self):
        self.setObjectName("MainWindow")
        self.setAutoFillBackground(False)
        self.setStyleSheet(self.WINDOW_STYLE)

        self.resize(*self.WINDOW_SIZE)

        self.central_widget.setObjectName('central_widget')

        self.save_button.setGeometry(QtCore.QRect(10, 280, 461, 41))
        self.save_button.setStyleSheet(self.MAIN_TEXT_STYLE)
        self.save_button.setObjectName('save_button')
        self.save_button.clicked.connect(self._on_save)

        self.token_line.setGeometry(QtCore.QRect(10, 80, 461, 31))
        self.token_line.setObjectName('token_line')
        self.token_line.setText(settings.BOT.TOKEN)

        self.admin_tgid_line.setGeometry(QtCore.QRect(10, 150, 461, 31))
        self.admin_tgid_line.setObjectName('admin_tgid_line')
        self.admin_tgid_line.setText(str(settings.BOT.ADMIN))

        self.token_label.setGeometry(QtCore.QRect(10, 60, 191, 16))
        self.token_label.setStyleSheet(self.MAIN_TEXT_STYLE)
        self.token_label.setObjectName('token_label')

        self.admin_tgid_label.setGeometry(QtCore.QRect(10, 130, 191, 16))
        self.admin_tgid_label.setStyleSheet(self.MAIN_TEXT_STYLE)
        self.admin_tgid_label.setObjectName('admin_tgid_label')

        self.program_label.setGeometry(QtCore.QRect(20, 10, 441, 41))
        self.program_label.setStyleSheet(self.TITLE_TEXT_STYLE)
        self.program_label.setObjectName('program_label')

        self.language_selecting.setGeometry(QtCore.QRect(10, 230, 461, 31))
        self.language_selecting.setAutoFillBackground(False)
        self.language_selecting.setStyleSheet(self.MAIN_TEXT_STYLE)
        self.language_selecting.setObjectName('language_selecting')

        for _ in self._get_langs():
            self.language_selecting.addItem('')

        self.language_selecting.currentIndexChanged.connect(self._on_language_changed)

        self.language_label.setGeometry(QtCore.QRect(10, 200, 191, 20))
        self.language_label.setStyleSheet(self.MAIN_TEXT_STYLE)
        self.language_label.setObjectName('language_label')

        self.setCentralWidget(self.central_widget)

        self._retranslate_ui()

        QtCore.QMetaObject.connectSlotsByName(self)

    @functools.cache
    def _get_langs(self) -> tuple:
        return Languages.select()

    def _get_selected_language(self):
        return self._get_langs()[self.language_selecting.currentIndex()]

    def _on_language_changed(self):
        lang_short_name = self._get_selected_language().short_name
        logging.logger.debug(f'Language {lang_short_name} selected')
        settings.L18N.UI_LANGUAGE = lang_short_name
        self._retranslate_ui()

    def _on_save(self):
        logging.logger.debug(f'Configuration saved')

        json_config = config.JSONConfig.load(settings.FILES['JSON_CONFIG_FILE'])
        json_config.ui_language = settings.L18N.UI_LANGUAGE
        json_config.save(settings.FILES['JSON_CONFIG_FILE'])

        env_config = config.ENVConfig.load(settings.FILES['ENV_CONFIG_FILE'])
        env_config.TOKEN = self.token_line.text()
        env_config.ADMIN = self.admin_tgid_line.text()
        env_config.save(settings.FILES['ENV_CONFIG_FILE'])

    def _retranslate_ui(self):
        curr_lang_pk = settings.L18N.UI_LANGUAGE
        curr_lang = Languages.get_by_id(curr_lang_pk)

        self.setWindowTitle(_('Configurator', language=curr_lang))
        self.save_button.setText(_('Save', language=curr_lang))
        self.token_label.setText(_('Token:', language=curr_lang))
        self.admin_tgid_label.setText(_('Admin Telegram-ID:', language=curr_lang))
        self.program_label.setText(
            _('{0} V{1} by crazyproger1', language=curr_lang).format(
                settings.APP.NAME,
                settings.APP.VERSION
            ))

        for i, lang in enumerate(Languages.select()):
            self.language_selecting.setItemText(i, lang.full_name)

        self.language_label.setText(_('Languages', language=curr_lang))
