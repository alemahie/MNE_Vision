#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Time frequency (ERSP/ITC) view
"""

from PyQt6.QtWidgets import QPushButton, QWidget, QGridLayout

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class timeFrequencyErspItcView(QWidget):
    def __init__(self):
        super().__init__()
        self.time_frequency_ersp_itc_listener = None

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_time_frequency_ersp_itc_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_time_frequency_ersp_itc_trigger)

        self.grid_layout.addWidget(self.cancel, 0, 0)
        self.grid_layout.addWidget(self.confirm, 0, 1)

    """
    Triggers
    """
    def cancel_time_frequency_ersp_itc_trigger(self):
        self.time_frequency_ersp_itc_listener.cancel_button_clicked()

    def confirm_time_frequency_ersp_itc_trigger(self):
        self.time_frequency_ersp_itc_listener.confirm_button_clicked()

    """
    Setters
    """
    def set_listener(self, listener):
        self.time_frequency_ersp_itc_listener = listener
