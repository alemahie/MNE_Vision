#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Power spectral density view
"""

from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel

from utils.channels_selector.channels_selector_controller import channelsSelectorController

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class erpView(QWidget):
    def __init__(self, all_channels_names):
        super().__init__()
        self.erp_listener = None
        self.all_channels_names = all_channels_names
        self.channels_selector_controller = None
        self.channels_selected = None

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.channels_selection_button = QPushButton("&Channels ...", self)
        self.channels_selection_button.clicked.connect(self.channels_selection_trigger)

        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_erp_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_erp_trigger)

        self.grid_layout.addWidget(QLabel("Channels : "), 0, 0)
        self.grid_layout.addWidget(self.channels_selection_button, 0, 1)
        self.grid_layout.addWidget(self.cancel, 1, 0)
        self.grid_layout.addWidget(self.confirm, 1, 1)

    """
    Triggers
    """
    def cancel_erp_trigger(self):
        self.erp_listener.cancel_button_clicked()

    def confirm_erp_trigger(self):
        self.erp_listener.confirm_button_clicked(self.channels_selected)

    def channels_selection_trigger(self):
        title = "Select the channels used for the ERP computation :"
        self.channels_selector_controller = channelsSelectorController(self.all_channels_names, title, box_checked=True)
        self.channels_selector_controller.set_listener(self.erp_listener)

    """
    Setters
    """
    def set_listener(self, listener):
        self.erp_listener = listener

    def set_channels_selected(self, channels_selected):
        self.channels_selected = channels_selected
