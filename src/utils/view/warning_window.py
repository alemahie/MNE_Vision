#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Warning Window View
"""

from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class warningWindow(QWidget):
    def __init__(self, warning_message, ok_function):
        """
        Window displaying an error message.
        :param warning_message: The warning message.
        :type warning_message: str
        :param ok_function: The function called when the "ok" button is clicked.
        :type ok_function: a function/method.
        """
        super().__init__()

        self.listener = None
        self.ok_function = ok_function

        self.message_box = QMessageBox()
        self.message_box.setIcon(QMessageBox.Icon.Information)
        self.message_box.setText(warning_message)
        self.message_box.setWindowTitle("Warning.")
        self.message_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        self.message_box.buttonClicked.connect(self.message_button)

    def message_button(self, button):
        """
        Receive the signal of a button being clicked.
        :param button: The button object
        :type button: QPushButton
        """
        if button.text() == "OK":
            self.ok_function()

    def show(self):
        """
        Display the error message.
        """
        self.message_box.exec()

    def set_listener(self, listener):
        """
        Set the listener
        :param listener: The listener
        :type listener: mainController
        """
        self.listener = listener
