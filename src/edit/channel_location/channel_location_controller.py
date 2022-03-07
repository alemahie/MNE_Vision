#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Channel location controller
"""

from edit.channel_location.channel_location_listener import channelLocationListener
from edit.channel_location.channel_location_view import channelLocationView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class channelLocationController(channelLocationListener):
    def __init__(self, channel_locations, channel_names):
        self.main_listener = None
        self.dataset_info_view = channelLocationView(len(channel_names))
        self.dataset_info_view.set_listener(self)

        self.dataset_info_view.show()
        
        self.channel_locations = channel_locations
        self.channel_names = channel_names
        self.current_channel_number = 0
        self.update_channel_displayed()

    def cancel_button_clicked(self):
        self.dataset_info_view.close()

    def confirm_button_clicked(self):
        self.dataset_info_view.close()
        
    def previous_button_clicked(self):
        if self.current_channel_number == 0:
            self.current_channel_number = len(self.channel_names)-1
        else:
            self.current_channel_number -= 1
        self.update_channel_displayed()

    def next_button_clicked(self):
        if self.current_channel_number == len(self.channel_names)-1:
            self.current_channel_number = 0
        else:
            self.current_channel_number += 1
        self.update_channel_displayed()

    def editing_finished_clicked(self, channel_number):
        self.current_channel_number = channel_number
        self.update_channel_displayed()

    """
    Updates
    """
    def update_channel_displayed(self):
        channel_name, channel_location = self.get_channel_info_from_number(self.current_channel_number)
        x_coordinate = channel_location[1]
        y_coordinate = channel_location[0]
        z_coordinate = channel_location[2]
        self.dataset_info_view.update_channel_displayed(self.current_channel_number, channel_name, x_coordinate, y_coordinate, z_coordinate)

    """
    Getters
    """
    def get_channel_info_from_number(self, channel_number):
        channel_name = self.channel_names[channel_number]
        channel_location = self.channel_locations[channel_name]
        return channel_name, channel_location

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
