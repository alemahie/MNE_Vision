#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ERP image view
"""

from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel

from utils.elements_selector.elements_selector_controller import multipleSelectorController

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class erpImageView(QWidget):
    def __init__(self, all_channels_names):
        super().__init__()
        self.erp_image_listener = None
        self.all_channels_names = all_channels_names
        self.channels_selector_controller = None
        self.channel_selected = None

        self.setWindowTitle("Event Related Potentials Image")

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.channels_selection_button = QPushButton("&Channels ...", self)
        self.channels_selection_button.clicked.connect(self.channels_selection_trigger)

        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_erp_image_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_erp_image_trigger)

        self.grid_layout.addWidget(QLabel("Channels : "), 0, 0)
        self.grid_layout.addWidget(self.channels_selection_button, 0, 1)
        self.grid_layout.addWidget(self.cancel, 1, 0)
        self.grid_layout.addWidget(self.confirm, 1, 1)

    """
    Triggers
    """
    def cancel_erp_image_trigger(self):
        self.erp_image_listener.cancel_button_clicked()

    def confirm_erp_image_trigger(self):
        self.erp_image_listener.confirm_button_clicked(self.channel_selected)

    def channels_selection_trigger(self):
        title = "Select the channels used for the ERP image computation :"
        self.channels_selector_controller = multipleSelectorController(self.all_channels_names, title, box_checked=False,
                                                                       unique_box=True)
        self.channels_selector_controller.set_listener(self.erp_image_listener)

    """
    Setters
    """
    def set_listener(self, listener):
        self.erp_image_listener = listener

    def set_channels_selected(self, channel_selected):
        self.channel_selected = channel_selected
