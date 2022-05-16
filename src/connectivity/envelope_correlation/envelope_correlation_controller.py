#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Envelope Correlation Controller
"""

from connectivity.envelope_correlation.envelope_correlation_listener import envelopeCorrelationListener
from connectivity.envelope_correlation.envelope_correlation_view import envelopeCorrelationView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class envelopeCorrelationController(envelopeCorrelationListener):
    def __init__(self, number_of_channels):
        """
        Controller for computing the envelope correlation on the dataset.
        Create a new window for specifying some parameters.
        :param number_of_channels: The number of channels
        :type number_of_channels: int
        """
        self.main_listener = None
        self.envelope_correlation_view = envelopeCorrelationView(number_of_channels)
        self.envelope_correlation_view.set_listener(self)

        self.envelope_correlation_view.show()

        self.source_estimation_controller = None

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.envelope_correlation_view.close()

    def confirm_button_clicked(self):
        """
        Close the window and send the information to the main controller.
        """
        self.envelope_correlation_view.close()
        self.main_listener.envelope_correlation_information()

    """
    Plot
    """
    def plot_envelope_correlation(self, envelope_correlation_data, channel_names):
        """
        Send the information to the view to plot the envelope correlation.
        :param envelope_correlation_data: The envelope correlation data to plot.
        :type envelope_correlation_data: list of, list of float
        :param channel_names: Channels' names
        :type channel_names: list of str
        """
        self.envelope_correlation_view.plot_envelope_correlation(envelope_correlation_data, channel_names)

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
