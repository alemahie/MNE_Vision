#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Topographies controller
"""

from plots.topographies.topographies_listener import topographiesListener
from plots.topographies.topographies_view import topographiesView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class topographiesController(topographiesListener):
    def __init__(self):
        """
        Controller for computing topographies on the dataset.
        Create a new window for specifying some parameters.
        """
        self.main_listener = None
        self.topographies_view = topographiesView()
        self.topographies_view.set_listener(self)

        self.topographies_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.topographies_view.close()

    def confirm_button_clicked(self, time_points, mode):
        """
        Close the window and send the information to the main controller.
        :param time_points: Time points at which the topographies will be plotted.
        :type time_points: list of float
        :param mode: Mode used for plotting the topographies.
        :type mode: str
        """
        self.topographies_view.close()
        self.main_listener.plot_topographies_information(time_points, mode)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :param elements_selected: Elements selected in the multiple elements' selector.
        :type elements_selected: list of str
        """
        self.topographies_view.set_channels_selected(elements_selected)

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
