#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Channel location view
"""

from PyQt6.QtGui import QDoubleValidator, QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QGridLayout, QLabel, QHBoxLayout, QPushButton

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class channelLocationView(QWidget):
    def __init__(self, number_of_channels):
        super().__init__()
        self.channel_location_listener = None

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        self.channel_name_line = QLineEdit()
        self.only_double = QDoubleValidator()
        self.x_coordinate_line = QLineEdit()
        self.x_coordinate_line.setValidator(self.only_double)
        self.y_coordinate_line = QLineEdit()
        self.y_coordinate_line.setValidator(self.only_double)
        self.z_coordinate_line = QLineEdit()
        self.z_coordinate_line.setValidator(self.only_double)

        self.info_widget = QWidget()
        self.info_grid_layout = QGridLayout()
        self.info_grid_layout.addWidget(QLabel("Channel location information : "), 0, 0)
        self.info_grid_layout.addWidget(QLabel("Channel name : "), 1, 0)
        self.info_grid_layout.addWidget(QLabel("X coordinate : "), 2, 0)
        self.info_grid_layout.addWidget(QLabel("Y coordinate : "), 3, 0)
        self.info_grid_layout.addWidget(QLabel("Z coordinate : "), 4, 0)
        self.info_grid_layout.addWidget(self.channel_name_line, 1, 1)
        self.info_grid_layout.addWidget(self.x_coordinate_line, 2, 1)
        self.info_grid_layout.addWidget(self.y_coordinate_line, 3, 1)
        self.info_grid_layout.addWidget(self.z_coordinate_line, 4, 1)
        self.info_widget.setLayout(self.info_grid_layout)

        self.channel_change_info_widget = QWidget()
        self.channel_change_info_layout = QHBoxLayout()
        self.channel_change_info_layout.addWidget(QLabel(f"Channel number : (out of {number_of_channels} channels)"))
        self.channel_change_info_widget.setLayout(self.channel_change_info_layout)

        self.change_channel_widget = QWidget()
        self.change_channel_layout = QHBoxLayout()
        self.previous_button = QPushButton("&Previous", self)
        self.previous_button.clicked.connect(self.previous_button_trigger)
        self.next_button = QPushButton("&Next", self)
        self.next_button.clicked.connect(self.next_button_trigger)
        self.only_int = QIntValidator(1, number_of_channels, self)
        self.channel_number = QLineEdit()
        self.channel_number.setValidator(self.only_int)
        self.channel_number.editingFinished.connect(self.editing_finished_trigger)
        self.change_channel_layout.addWidget(self.previous_button)
        self.change_channel_layout.addWidget(self.channel_number)
        self.change_channel_layout.addWidget(self.next_button)
        self.change_channel_widget.setLayout(self.change_channel_layout)

        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_channel_location_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_channel_location_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.info_widget)
        self.vertical_layout.addWidget(self.channel_change_info_widget)
        self.vertical_layout.addWidget(self.change_channel_widget)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    """
    Triggers
    """

    def cancel_channel_location_trigger(self):
        self.channel_location_listener.cancel_button_clicked()

    def confirm_channel_location_trigger(self):
        self.channel_location_listener.confirm_button_clicked()

    def previous_button_trigger(self):
        self.channel_location_listener.previous_button_clicked()

    def next_button_trigger(self):
        self.channel_location_listener.next_button_clicked()

    def editing_finished_trigger(self):
        channel_number = int(self.channel_number.text())-1
        self.channel_location_listener.editing_finished_clicked(channel_number)

    """
    Updates
    """
    def update_channel_displayed(self, channel_number, channel_name, x_coordinate, y_coordinate, z_coordinate):
        self.channel_name_line.setText(channel_name)
        self.x_coordinate_line.setText(str(round(x_coordinate, 3)))
        self.y_coordinate_line.setText(str(round(y_coordinate, 3)))
        self.z_coordinate_line.setText(str(round(z_coordinate, 3)))
        self.channel_number.setText(str(channel_number + 1))

    """
    Setters
    """

    def set_listener(self, listener):
        self.channel_location_listener = listener
