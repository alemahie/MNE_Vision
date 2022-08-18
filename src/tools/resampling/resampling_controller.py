#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Resampling controller
"""

from tools.resampling.resampling_view import resamplingView
from tools.resampling.resampling_listener import resamplingListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class resamplingController(resamplingListener):
    def __init__(self, frequency):
        """
        Controller for computing the resampling on the dataset.
        Create a new window for specifying some parameters.
        :param frequency: The frequency rate
        :type frequency: float
        """
        self.main_listener = None
        self.resampling_view = resamplingView(frequency)
        self.resampling_view.set_listener(self)

        self.resampling_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.resampling_view.close()

    def confirm_button_clicked(self, frequency):
        """
        Close the window and send the information to the main controller.
        :param frequency: The frequency rate
        :type frequency: float
        """
        self.main_listener.resampling_information(frequency)
        self.resampling_view.close()

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
