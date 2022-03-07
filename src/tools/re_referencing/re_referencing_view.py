#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Re-referencing View
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QButtonGroup, QCheckBox, QPushButton, QGridLayout, QHBoxLayout, QLabel

from utils.channels_selector.channels_selector_controller import channelsSelectorController

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class reReferencingView(QWidget):
    def __init__(self, reference, all_channels_names):
        super().__init__()
        self.re_referencing_listener = None
        self.channels_selector_controller = None
        self.all_channels_names = all_channels_names
        self.channels_selected = None

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        # Average of all channels & Select a specific channel
        self.re_referencing_mode_widget = QWidget()
        self.re_referencing_mode_buttons = QButtonGroup()

        self.average_check_box = QCheckBox()
        self.average_check_box.setChecked(True)
        self.average_check_box.setText("Compute average reference")
        self.re_referencing_mode_buttons.addButton(self.average_check_box, 1)   # Button with ID 1
        self.channel_check_box = QCheckBox()
        self.channel_check_box.setText("Re-reference data to channel(s) : ")
        self.re_referencing_mode_buttons.addButton(self.channel_check_box, 2)  # Button with ID 2
        self.channels_selection_button = QPushButton("&Channels ...", self)
        self.channels_selection_button.clicked.connect(self.channels_selection_trigger)

        self.check_box_layout = QGridLayout()
        self.check_box_layout.addWidget(self.average_check_box, 0, 0)
        self.check_box_layout.addWidget(self.channel_check_box, 1, 0)
        self.check_box_layout.addWidget(self.channels_selection_button, 1, 1)
        self.re_referencing_mode_widget.setLayout(self.check_box_layout)

        # Cancel & Confirm buttons
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_re_referencing_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_re_referencing_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        # Final layout
        self.vertical_layout.addWidget(QLabel("Current reference : " + reference))
        self.vertical_layout.addWidget(self.re_referencing_mode_widget)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    """
    Triggers
    """
    def cancel_re_referencing_trigger(self):
        self.re_referencing_listener.cancel_button_clicked()

    def confirm_re_referencing_trigger(self):
        checked_button = self.re_referencing_mode_buttons.checkedButton()
        button_id = self.re_referencing_mode_buttons.id(checked_button)
        references = None
        if button_id == 1:      # Average of all channels for reference
            references = "average"
        elif button_id == 2:    # Selected channel for reference
            references = self.channels_selected
        if references is None:
            print("No channels selected.")
        else:
            self.re_referencing_listener.confirm_button_clicked(references)

    def channels_selection_trigger(self):
        title = "Select the channels used for the re-referencing :"
        self.channels_selector_controller = channelsSelectorController(self.all_channels_names, title, box_checked=False)
        self.channels_selector_controller.set_listener(self.re_referencing_listener)

    """
    Setters
    """
    def set_listener(self, listener):
        self.re_referencing_listener = listener

    def set_channels_selected(self, channels_selected):
        self.channels_selected = channels_selected
