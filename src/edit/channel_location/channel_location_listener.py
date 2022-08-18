#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Channel location listener
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class channelLocationListener(ABC):
    """
    Listener doing the connection between the controller and the view for displaying the channels' information.
    It retrieves the information from the view to send it to the controller.
    """

    @abstractmethod
    def cancel_button_clicked(self):
        pass

    @abstractmethod
    def confirm_button_clicked(self, channel_name, x_coordinate, y_coordinate, z_coordinate):
        pass

    @abstractmethod
    def previous_button_clicked(self, channel_name, x_coordinate, y_coordinate, z_coordinate):
        pass

    @abstractmethod
    def next_button_clicked(self, channel_name, x_coordinate, y_coordinate, z_coordinate):
        pass

    @abstractmethod
    def delete_button_clicked(self):
        pass

    @abstractmethod
    def insert_button_clicked(self, channel_name, x_coordinate, y_coordinate, z_coordinate):
        pass

    @abstractmethod
    def editing_finished_clicked(self, channel_number):
        pass
