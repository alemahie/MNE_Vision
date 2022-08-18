#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Load Data Info Controller
"""

from file.load_data_info.load_data_info_listener import loadDataInfoListener
from file.load_data_info.load_data_info_view import loadDataInfoView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class loadDataInfoController(loadDataInfoListener):
    def __init__(self, channel_names, tmin, tmax):
        """
        Controller for loading the additional data information when a dataset is loaded into the software.
        Create a new window for displaying the information.
        :param channel_names: Channels' names
        :type channel_names: list of str
        :param tmin: Start time of the epoch or raw file
        :type tmin: float
        :param tmax: End time of the epoch or raw file
        :type tmax: float
        """
        self.main_listener = None
        self.load_data_info_view = loadDataInfoView(channel_names, tmin, tmax)
        self.load_data_info_view.set_listener(self)

        self.load_data_info_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.load_data_info_view.close()

    def confirm_button_clicked(self, montage, channels_selected, tmin, tmax, dataset_name):
        """
        Close the window and send the information to the main controller
        :param montage: Montage of the headset
        :type montage: str
        :param channels_selected: Channels selected
        :type channels_selected: list of str
        :param tmin: Start time of the epoch or raw file to keep
        :type tmin: float
        :param tmax: End time of the epoch or raw file to keep
        :type tmax: float
        :param dataset_name: The name of the loaded dataset.
        :type dataset_name: str
        """
        self.load_data_info_view.close()
        self.main_listener.load_data_info_information(montage, channels_selected, tmin, tmax, dataset_name)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :param elements_selected: Elements selected in the multiple elements' selector.
        :type elements_selected: list of str
        """
        self.load_data_info_view.set_channels_selected(elements_selected)

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
