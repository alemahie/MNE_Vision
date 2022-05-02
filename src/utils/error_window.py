#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Error Window View
"""

from PyQt6.QtWidgets import QWidget, QMessageBox

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class errorWindow(QWidget):
    def __init__(self, error_message):
        super().__init__()

        self.message_box = QMessageBox()
        self.message_box.setIcon(QMessageBox.Icon.Information)
        self.message_box.setText(error_message)
        self.message_box.setWindowTitle("An error has occurred.")
        self.message_box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

    def show(self):
        self.message_box.exec()
