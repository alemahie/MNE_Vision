#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Time frequency (ERSP/ITC) controller
"""

from plots.time_frequency_ersp_itc.time_frequency_ersp_itc_listener import timeFrequencyErspItcListener
from plots.time_frequency_ersp_itc.time_frequency_ersp_itc_view import timeFrequencyErspItcView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class timeFrequencyErspItcController(timeFrequencyErspItcListener):
    def __init__(self, all_channels_names, no_channels=False):
        """
        Controller for computing a time-frequency analysis on the dataset.
        Create a new window for specifying some parameters.
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        :param no_channels: Check if the channel selection must be done. Not necessary for the study plot.
        :type no_channels: bool
        """
        self.main_listener = None
        self.time_frequency_ersp_itc_view = timeFrequencyErspItcView(all_channels_names, no_channels)
        self.time_frequency_ersp_itc_view.set_listener(self)

        self.time_frequency_ersp_itc_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.time_frequency_ersp_itc_view.close()

    def confirm_button_clicked(self, method_tfr, channel_selected, min_frequency, max_frequency, n_cycles):
        """
        Close the window and send the information to the main controller.
        :param method_tfr: Method used for computing the time-frequency analysis.
        :type method_tfr: str
        :param channel_selected: Channel on which the time-frequency analysis will be computed.
        :type channel_selected: str
        :param min_frequency: Minimum frequency from which the time-frequency analysis will be computed.
        :type min_frequency: float
        :param max_frequency: Maximum frequency from which the time-frequency analysis will be computed.
        :type max_frequency: float
        :param n_cycles: Number of cycles used by the time-frequency analysis for his computation.
        :type n_cycles: int
        """
        self.time_frequency_ersp_itc_view.close()
        self.main_listener.plot_time_frequency_information(method_tfr, channel_selected, min_frequency, max_frequency,
                                                           n_cycles)

    def confirm_button_clicked_from_study(self, method_tfr, min_frequency, max_frequency, n_cycles):
        """
        Close the window and send the information to the study controller..
        :param method_tfr: Method used for computing the time-frequency analysis.
        :type method_tfr: str
        :param min_frequency: Minimum frequency from which the time-frequency analysis will be computed.
        :type min_frequency: float
        :param max_frequency: Maximum frequency from which the time-frequency analysis will be computed.
        :type max_frequency: float
        :param n_cycles: Number of cycles used by the time-frequency analysis for his computation.
        :type n_cycles: int
        """
        self.time_frequency_ersp_itc_view.close()
        self.main_listener.plot_time_frequency_information(method_tfr, min_frequency, max_frequency, n_cycles)

    def plot_ersp_itc(self, channel_selected, power, itc):
        """
        Send the information to the view for the plotting of the time-frequency analysis.
        :param channel_selected: The channel selected for the time-frequency analysis.
        :type channel_selected: str
        :param power: "power" data of the time-frequency analysis computation.
        :type power: MNE.AverageTFR
        :param itc: "itc" data of the time-frequency analysis computation.
        :type itc: MNE.AverageTFR
        """
        self.time_frequency_ersp_itc_view.plot_ersp_itc(channel_selected, power, itc)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :param elements_selected: Elements selected in the multiple elements' selector.
        :type elements_selected: str
        """
        self.time_frequency_ersp_itc_view.set_channels_selected(elements_selected)

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
