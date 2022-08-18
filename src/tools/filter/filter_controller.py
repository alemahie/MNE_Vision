#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filter controller
"""

from tools.filter.filter_view import filterView
from tools.filter.filter_listener import filterListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class filterController(filterListener):
    def __init__(self, all_channels_names):
        """
        Controller for computing the filtering on the dataset.
        Create a new window for specifying some parameters.
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        """
        self.main_listener = None
        self.filter_view = filterView(all_channels_names)
        self.filter_view.set_listener(self)

        self.filter_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.filter_view.close()

    def confirm_button_clicked(self, low_frequency, high_frequency, channels_selected, filter_method):
        """
        Close the window and send the information to the main controller.
        :param low_frequency: Lowest frequency from where the data will be filtered.
        :type low_frequency: float
        :param high_frequency: Highest frequency from where the data will be filtered.
        :type high_frequency: float
        :param channels_selected: Channels on which the filtering will be performed.
        :type channels_selected: list of str
        :param filter_method: Method used for the filtering, either FIR or IIR.
        :type filter_method: str
        """
        self.filter_view.close()
        self.main_listener.filter_information(low_frequency, high_frequency, channels_selected, filter_method)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :param elements_selected: Elements selected in the multiple elements' selector.
        :type elements_selected: list of str
        """
        self.filter_view.set_channels_selected(elements_selected)

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
