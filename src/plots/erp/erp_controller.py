#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ERP controller
"""

from plots.erp.erp_listener import erpListener
from plots.erp.erp_view import erpView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class erpController(erpListener):
    def __init__(self, all_channels_names):
        """
        Controller for computing the ERPs on the dataset.
        Create a new window for specifying some parameters.
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        """
        self.main_listener = None
        self.erp_view = erpView(all_channels_names)
        self.erp_view.set_listener(self)

        self.erp_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.erp_view.close()

    def confirm_button_clicked(self, channels_selected):
        """
        Close the window and send the information to the main controller.
        :param channels_selected: The channels selected.
        :type channels_selected: list of str
        """
        self.erp_view.close()
        self.main_listener.plot_ERPs_information(channels_selected)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :param elements_selected: Elements selected in the multiple elements' selector.
        :type elements_selected: list of str
        """
        self.erp_view.set_channels_selected(elements_selected)

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
