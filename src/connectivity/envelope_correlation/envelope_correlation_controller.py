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
        self.main_listener = None
        self.envelope_correlation_view = envelopeCorrelationView(number_of_channels)
        self.envelope_correlation_view.set_listener(self)

        self.envelope_correlation_view.show()

        self.source_estimation_controller = None

    def cancel_button_clicked(self):
        self.envelope_correlation_view.close()

    def confirm_button_clicked(self):
        self.envelope_correlation_view.close()
        self.main_listener.envelope_correlation_information()

    """
    Plot
    """
    def plot_envelope_correlation(self, envelope_correlation_data, channel_names):
        self.envelope_correlation_view.plot_envelope_correlation(envelope_correlation_data, channel_names)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
