#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extract Epochs Controller
"""

from tools.extract_epochs.extract_epochs_listener import extractEpochsListener
from tools.extract_epochs.extract_epochs_view import extractEpochsView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class extractEpochsController(extractEpochsListener):
    def __init__(self):
        """
        Controller for extracting epochs from the dataset.
        Create a new window for specifying some parameters.
        """
        self.main_listener = None
        self.extract_epochs_view = extractEpochsView()
        self.extract_epochs_view.set_listener(self)

        self.extract_epochs_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.extract_epochs_view.close()

    def confirm_button_clicked(self, tmin, tmax):
        """
        Close the window and send the information to the main controller.
        :param tmin: Start time of the epoch to keep
        :type tmin: float
        :param tmax: End time of the epoch to keep
        :type tmax: float
        """
        self.extract_epochs_view.close()
        self.main_listener.extract_epochs_information(tmin, tmax)

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
