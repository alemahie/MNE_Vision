#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics Time frequency (ERSP/ITC) controller
"""

from statistics.statistics_ersp_itc.statistics_ersp_itc_listener import statisticsErspItcListener
from statistics.statistics_ersp_itc.statistics_ersp_itc_view import statisticsErspItcView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class statisticsErspItcController(statisticsErspItcListener):
    def __init__(self, all_channels_names, event_ids):
        """
        Controller for computing a time-frequency analysis on the dataset.
        Create a new window for specifying some parameters.
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        :param event_ids: The events' ids
        :type event_ids: dict
        """
        self.main_listener = None
        self.statistics_ersp_itc_view = statisticsErspItcView(all_channels_names, event_ids)
        self.statistics_ersp_itc_view.set_listener(self)

        self.statistics_ersp_itc_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.statistics_ersp_itc_view.close()

    def confirm_button_clicked(self, method_tfr, channel_selected, min_frequency, max_frequency, n_cycles,
                               stats_first_variable, stats_second_variable):
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
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        self.statistics_ersp_itc_view.close()
        self.main_listener.statistics_ersp_itc_information(method_tfr, channel_selected, min_frequency, max_frequency,
                                                           n_cycles, stats_first_variable, stats_second_variable)

    """
    Plots
    """
    def plot_ersp_itc(self, channel_selected, power_one, itc_one, power_two, itc_two):
        """
        Send the information to the view for the plotting of the time-frequency analysis.
        :param channel_selected: The channel selected for the time-frequency analysis.
        :type channel_selected: str
        :param power_one: "power" data of the time-frequency analysis computation of the first independent variable.
        :type power_one: MNE.AverageTFR
        :param itc_one: "itc" data of the time-frequency analysis computation of the first independent variable.
        :type itc_one: MNE.AverageTFR
        :param power_two: "power" data of the time-frequency analysis computation of the second independent variable.
        :type power_two: MNE.AverageTFR
        :param itc_two: "itc" data of the time-frequency analysis computation of the second independent variable.
        :type itc_two: MNE.AverageTFR
        """
        self.statistics_ersp_itc_view.plot_ersp_itc(channel_selected, power_one, itc_one, power_two, itc_two)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :param elements_selected: Elements selected in the multiple elements' selector.
        :type elements_selected: str
        """
        self.statistics_ersp_itc_view.set_channels_selected(elements_selected)

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
