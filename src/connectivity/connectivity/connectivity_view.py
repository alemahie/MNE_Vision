#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Connectivity view
"""

from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class connectivityView(QWidget):
    def __init__(self):
        super().__init__()
        self.connectivity_listener = None

        self.setWindowTitle("Connectivity")

        self.vertical_layout = QVBoxLayout()

        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_connectivity_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_connectivity_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.cancel_confirm_widget)
        self.setLayout(self.vertical_layout)

    """
    Triggers
    """
    def cancel_connectivity_trigger(self):
        self.connectivity_listener.cancel_button_clicked()

    def confirm_connectivity_trigger(self):
        self.connectivity_listener.confirm_button_clicked()
    """
    Setters
    """
    def set_listener(self, listener):
        self.connectivity_listener = listener
