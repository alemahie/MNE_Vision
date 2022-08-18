#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Channel Location Controller
"""

import numpy as np

from copy import copy

from edit.channel_location.channel_location_listener import channelLocationListener
from edit.channel_location.channel_location_view import channelLocationView

from utils.view.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class channelLocationController(channelLocationListener):
    def __init__(self, channel_locations, channel_names):
        """
        Controller for editing the channels' locations.
        Create a new window for displaying the channels' information.
        :param channel_locations: Channel location
        :type channel_locations: dict
        :param channel_names: Channel names
        :type channel_names: list of str
        """
        self.main_listener = None
        self.dataset_info_view = channelLocationView(len(channel_names))
        self.dataset_info_view.set_listener(self)

        self.dataset_info_view.show()
        
        self.channel_locations = copy(channel_locations)
        self.channel_names = copy(channel_names)

        self.current_channel_number = 0
        self.number_of_channels_original = len(channel_names)
        self.update_channel_displayed()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.dataset_info_view.close()

    def confirm_button_clicked(self, channel_name, x_coordinate, y_coordinate, z_coordinate):
        """
        Close the window and send the information to the main controller.
        Save the information of the last channel displayed before sending the information to the controller.
        :param channel_name: Channel name
        :type channel_name: str
        :param x_coordinate: X coordinate of the channel's location
        :type x_coordinate: float
        :param y_coordinate: Y coordinate of the channel's location
        :type y_coordinate: float
        :param z_coordinate: Z coordinate of the channel's location
        :type z_coordinate: float
        """
        if self.channel_name_is_free(channel_name):
            self.update_channel_data(channel_name, x_coordinate, y_coordinate, z_coordinate)
            if self.number_of_channels_original == len(self.channel_names):
                self.main_listener.channel_location_finished(self.channel_locations, self.channel_names)
                self.dataset_info_view.close()
            else:
                error_message = "You have a different number of channels than in your dataset. Please set up the correct " \
                                "number of channels."
                error_window = errorWindow(error_message)
                error_window.show()
        
    def previous_button_clicked(self, channel_name, x_coordinate, y_coordinate, z_coordinate):
        """
        Save the information of the last channel displayed before displaying the information of the previous channel.
        :param channel_name: Channel name
        :type channel_name: str
        :param x_coordinate: X coordinate of the channel's location
        :type x_coordinate: float
        :param y_coordinate: Y coordinate of the channel's location
        :type y_coordinate: float
        :param z_coordinate: Z coordinate of the channel's location
        :type z_coordinate: float
        """
        if self.channel_name_is_free(channel_name):
            self.update_channel_data(channel_name, x_coordinate, y_coordinate, z_coordinate)
            if self.current_channel_number == 0:
                self.current_channel_number = len(self.channel_names)-1
            else:
                self.current_channel_number -= 1
            self.update_channel_displayed()

    def next_button_clicked(self, channel_name, x_coordinate, y_coordinate, z_coordinate):
        """
        Save the information of the last channel displayed before displaying the information of the next channel.
        :param channel_name: Channel name
        :type channel_name: str
        :param x_coordinate: X coordinate of the channel's location
        :type x_coordinate: float
        :param y_coordinate: Y coordinate of the channel's location
        :type y_coordinate: float
        :param z_coordinate: Z coordinate of the channel's location
        :type z_coordinate: float
        """
        if self.channel_name_is_free(channel_name):
            self.update_channel_data(channel_name, x_coordinate, y_coordinate, z_coordinate)
            if self.current_channel_number == len(self.channel_names)-1:
                self.current_channel_number = 0
            else:
                self.current_channel_number += 1
            self.update_channel_displayed()

    def delete_button_clicked(self):
        """
        Delete the information of the channel displayed.
        """
        if len(self.channel_names) > 1:
            channel_name = self.channel_names[self.current_channel_number]
            del self.channel_names[self.current_channel_number]
            del self.channel_locations[channel_name]
            self.update_channel_displayed()
        else:
            error_message = "You can not delete all the events."
            error_window_view = errorWindow(error_message)
            error_window_view.show()

    def insert_button_clicked(self, channel_name, x_coordinate, y_coordinate, z_coordinate):
        """
        Save the information of the last channel displayed before inserting a new channel.
        :param channel_name: Channel name
        :type channel_name: str
        :param x_coordinate: X coordinate of the channel's location
        :type x_coordinate: float
        :param y_coordinate: Y coordinate of the channel's location
        :type y_coordinate: float
        :param z_coordinate: Z coordinate of the channel's location
        :type z_coordinate: float
        """
        if self.channel_name_is_free(channel_name):
            self.update_channel_data(channel_name, x_coordinate, y_coordinate, z_coordinate)
            self.insert_new_channel()
            self.current_channel_number += 1
            self.update_channel_displayed()

    def editing_finished_clicked(self, channel_number):
        """
        Load the channel's information based on the channel number given.
        :param channel_number: Channel number
        :type channel_number: int
        """
        self.current_channel_number = channel_number
        self.update_channel_displayed()

    """
    Updates
    """
    def update_channel_displayed(self):
        """
        Update the information of the channel displayed based on the current channel number (could have change because of
        the next, previous, etc. button pushed.
        """
        channel_name, channel_location = self.get_channel_info_from_number(self.current_channel_number)
        x_coordinate = channel_location[1]
        y_coordinate = channel_location[0]
        z_coordinate = channel_location[2]
        self.dataset_info_view.update_channel_displayed(self.current_channel_number, channel_name, x_coordinate,
                                                        y_coordinate, z_coordinate, len(self.channel_names))

    def update_channel_data(self, channel_name, x_coordinate, y_coordinate, z_coordinate):
        """
        Update the information of a channel.
        :param channel_name: Channel name
        :type channel_name: str
        :param x_coordinate: X coordinate of the channel's location
        :type x_coordinate: float
        :param y_coordinate: Y coordinate of the channel's location
        :type y_coordinate: float
        :param z_coordinate: Z coordinate of the channel's location
        :type z_coordinate: float
        """
        self.channel_names[self.current_channel_number] = channel_name
        self.channel_locations[channel_name] = np.array([y_coordinate, x_coordinate, z_coordinate])

    def insert_new_channel(self):
        """
        Insert a new channel in the data.
        """
        new_channel_idx = 0
        while True:
            new_channel_name = "none-" + str(new_channel_idx)
            if new_channel_name not in self.channel_names:
                self.channel_names.insert(self.current_channel_number+1, new_channel_name)
                self.channel_locations[new_channel_name] = np.array([0.0, 0.0, 0.0])
                break
            new_channel_idx += 1

    def channel_name_is_free(self, channel_name):
        """
        Check if the channel name provided is available or not. If it is not available, display an error message and the
        user must set a new name for the channel.
        :param channel_name: The channel name.
        :type channel_name: str
        :return: True if the channel name is available. False otherwise.
        :rtype: bool
        """
        for i, value in enumerate(self.channel_names):
            if channel_name == value and i != self.current_channel_number:
                error_message = "This channel name is already taken. Please choose another name for this channel."
                error_window = errorWindow(error_message)
                error_window.show()
                return False
        return True

    """
    Getters
    """
    def get_channel_info_from_number(self, channel_number):
        """
        Get the information of a channel based on a channel number.
        :param channel_number: The channel number
        :type channel_number: int
        :return: channel_name: The channel name.
        channel_location: The channel location.
        :rtype: str, list of float
        """
        channel_name = self.channel_names[channel_number]
        channel_location = self.channel_locations[channel_name]
        return channel_name, channel_location

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the main listener so that the controller is able to communicate with the main controller.
        :param listener: main listener
        :type listener: mainController
        """
        self.main_listener = listener
