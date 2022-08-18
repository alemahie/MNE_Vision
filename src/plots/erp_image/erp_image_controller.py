#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ERP image controller
"""

from plots.erp_image.erp_image_listener import erpImageListener
from plots.erp_image.erp_image_view import erpImageView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class erpImageController(erpImageListener):
    def __init__(self, all_channels_names):
        """
        Controller for computing an ERP image on the dataset.
        Create a new window for specifying some parameters.
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        """
        self.main_listener = None
        self.erp_image_view = erpImageView(all_channels_names)
        self.erp_image_view.set_listener(self)

        self.erp_image_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.erp_image_view.close()

    def confirm_button_clicked(self, channel_selected):
        """
        Close the window and send the information to the main controller.
        :param channel_selected: The channel selected.
        :type channel_selected: str
        """
        self.erp_image_view.close()
        self.main_listener.plot_ERP_image_information(channel_selected)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :param elements_selected: Elements selected in the multiple elements' selector.
        :type elements_selected: list of str
        """
        self.erp_image_view.set_channels_selected(elements_selected)

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
