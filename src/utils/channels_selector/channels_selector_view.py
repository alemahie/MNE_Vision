#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Channels selector View
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QLabel, QCheckBox

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class channelsSelectorView(QWidget):
    def __init__(self, all_channels_names, title, box_checked):
        super().__init__()
        self.channels_selector_listener = None

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        # Channels
        self.channels_widget = QWidget()
        self.channels_vbox_layout = QVBoxLayout()

        self.select_unselect_widget = QWidget()
        self.select_unselect_hbox_layout = QHBoxLayout()
        self.select_all_channels = QPushButton("&Select All", self)
        self.select_all_channels.clicked.connect(self.select_all_channels_trigger)
        self.unselect_all_channels = QPushButton("&Unselect All", self)
        self.unselect_all_channels.clicked.connect(self.unselect_all_channels_trigger)
        self.select_unselect_hbox_layout.addWidget(self.select_all_channels)
        self.select_unselect_hbox_layout.addWidget(self.unselect_all_channels)
        self.select_unselect_widget.setLayout(self.select_unselect_hbox_layout)

        self.channels_vbox_layout.addWidget(self.select_unselect_widget)
        self.create_check_boxes(all_channels_names, box_checked)
        self.channels_widget.setLayout(self.channels_vbox_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.channels_widget)

        # Cancel & Confirm buttons
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(QLabel(title))
        self.vertical_layout.addWidget(self.scroll_area)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    def create_check_boxes(self, all_channels_names, box_checked):
        for i, channel in enumerate(all_channels_names):
            check_box = QCheckBox()
            check_box.setChecked(box_checked)
            check_box.setText(channel)
            self.channels_vbox_layout.addWidget(check_box)

    """
    Triggers
    """
    def cancel_trigger(self):
        self.channels_selector_listener.cancel_button_clicked()

    def confirm_trigger(self):
        channels_selected = self.get_all_channels_selected()
        self.channels_selector_listener.confirm_button_clicked(channels_selected)

    def select_all_channels_trigger(self):
        for i in range(1, self.channels_vbox_layout.count()):
            check_box = self.channels_vbox_layout.itemAt(i).widget()
            check_box.setChecked(True)

    def unselect_all_channels_trigger(self):
        for i in range(1, self.channels_vbox_layout.count()):
            check_box = self.channels_vbox_layout.itemAt(i).widget()
            check_box.setChecked(False)

    """
    Setters
    """
    def set_listener(self, listener):
        self.channels_selector_listener = listener

    """
    Getters
    """
    def get_all_channels_selected(self):
        all_channels = []
        for i in range(1, self.channels_vbox_layout.count()):
            check_box = self.channels_vbox_layout.itemAt(i).widget()
            if check_box.isChecked():
                all_channels.append(check_box.text())
        return all_channels
