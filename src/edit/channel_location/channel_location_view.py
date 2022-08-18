#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Channel location view
"""

from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QGridLayout, QLabel, QHBoxLayout, QPushButton

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class channelLocationView(QWidget):
    def __init__(self, number_of_channels):
        """
        Window displaying the channels' information of the dataset.
        :param number_of_channels: The number of channels.
        :type number_of_channels: int
        """
        super().__init__()
        self.channel_location_listener = None

        self.setWindowTitle("Channel Location")

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
        self.channel_number_label = QLabel(f"Channel number : (out of {number_of_channels} channels)")
        self.channel_change_info_layout.addWidget(self.channel_number_label)
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

        self.delete_insert_widget = QWidget()
        self.delete_insert_layout = QHBoxLayout()
        self.delete_button = QPushButton("&Delete event", self)
        self.delete_button.clicked.connect(self.delete_button_trigger)
        self.insert_button = QPushButton("&Insert event", self)
        self.insert_button.clicked.connect(self.insert_button_trigger)
        self.delete_insert_layout.addWidget(self.delete_button)
        self.delete_insert_layout.addWidget(self.insert_button)
        self.delete_insert_widget.setLayout(self.delete_insert_layout)

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
        self.vertical_layout.addWidget(self.delete_insert_widget)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    """
    Triggers
    """
    def cancel_channel_location_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.channel_location_listener.cancel_button_clicked()

    def confirm_channel_location_trigger(self):
        """
        Retrieve the channel name and location and send the information to the controller.
        """
        channel_name = self.channel_name_line.text()
        x_coordinate = float(self.x_coordinate_line.text().replace(',', '.'))
        y_coordinate = float(self.y_coordinate_line.text().replace(',', '.'))
        z_coordinate = float(self.z_coordinate_line.text().replace(',', '.'))
        self.channel_location_listener.confirm_button_clicked(channel_name, x_coordinate, y_coordinate, z_coordinate)

    def previous_button_trigger(self):
        """
        Retrieve the channel name and location and send the information to the controller to display the previous channel.
        """
        channel_name = self.channel_name_line.text()
        x_coordinate = float(self.x_coordinate_line.text().replace(',', '.'))
        y_coordinate = float(self.y_coordinate_line.text().replace(',', '.'))
        z_coordinate = float(self.z_coordinate_line.text().replace(',', '.'))
        self.channel_location_listener.previous_button_clicked(channel_name, x_coordinate, y_coordinate, z_coordinate)

    def next_button_trigger(self):
        """
        Retrieve the channel name and location and send the information to the controller to display the next channel.
        """
        channel_name = self.channel_name_line.text()
        x_coordinate = float(self.x_coordinate_line.text().replace(',', '.'))
        y_coordinate = float(self.y_coordinate_line.text().replace(',', '.'))
        z_coordinate = float(self.z_coordinate_line.text().replace(',', '.'))
        self.channel_location_listener.next_button_clicked(channel_name, x_coordinate, y_coordinate, z_coordinate)

    def delete_button_trigger(self):
        """
        Send the information to the controller to delete the current channel.
        """
        self.channel_location_listener.delete_button_clicked()

    def insert_button_trigger(self):
        """
        Retrieve the channel name and location and send the information to the controller to insert a new channel.
        """
        channel_name = self.channel_name_line.text()
        x_coordinate = float(self.x_coordinate_line.text())
        y_coordinate = float(self.y_coordinate_line.text())
        z_coordinate = float(self.z_coordinate_line.text())
        self.channel_location_listener.insert_button_clicked(channel_name, x_coordinate, y_coordinate, z_coordinate)

    def editing_finished_trigger(self):
        """
        Retrieve the new channel number wanted to be displayed and send the information to the controller to display the
        wanted channel.
        """
        channel_number = int(self.channel_number.text())-1
        self.channel_location_listener.editing_finished_clicked(channel_number)

    """
    Updates
    """
    def update_channel_displayed(self, channel_number, channel_name, x_coordinate, y_coordinate, z_coordinate,
                                 number_of_channels):
        """
        Update the channel displayed on the window.
        :param channel_number: The channel number
        :type channel_number: int
        :param channel_name: Channel name
        :type channel_name: str
        :param x_coordinate: X coordinate of the channel's location
        :type x_coordinate: float
        :param y_coordinate: Y coordinate of the channel's location
        :type y_coordinate: float
        :param z_coordinate: Z coordinate of the channel's location
        :type z_coordinate: float
        :param number_of_channels: The number of channels
        :type number_of_channels: int
        """
        self.channel_name_line.setText(channel_name)
        self.x_coordinate_line.setText(str(round(x_coordinate, 3)))
        self.y_coordinate_line.setText(str(round(y_coordinate, 3)))
        self.z_coordinate_line.setText(str(round(z_coordinate, 3)))
        self.channel_number.setText(str(channel_number + 1))
        self.channel_number_label.setText(f"Channel number : (out of {number_of_channels} channels)")

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: channelLocationController
        """
        self.channel_location_listener = listener
