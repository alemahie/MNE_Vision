#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics PSD Controller
"""

from statistics.statistics_psd.statistics_psd_listener import statisticsPsdListener
from statistics.statistics_psd.statistics_psd_view import statisticsPsdView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class statisticsPsdController(statisticsPsdListener):
    def __init__(self, minimum_time, maximum_time, event_ids, all_channels_names):
        """
        Controller for computing the power spectral density on the dataset.
        Create a new window for specifying some parameters.
        :param minimum_time: Minimum time of the epochs from which the power spectral density can be computed.
        :type minimum_time: float
        :param maximum_time: Maximum time of the epochs from which the power spectral density can be computed.
        :type maximum_time: float
        :param event_ids: The events' ids
        :type event_ids: dict
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        """
        self.main_listener = None
        self.statistics_psd_view = statisticsPsdView(minimum_time, maximum_time, event_ids, all_channels_names)
        self.statistics_psd_view.set_listener(self)

        self.statistics_psd_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.statistics_psd_view.close()

    def confirm_button_clicked(self, minimum_frequency, maximum_frequency, minimum_time, maximum_time, topo_time_points,
                               channel_selected, stats_first_variable, stats_second_variable):
        """
        Close the window and send the information to the main controller.
        :param minimum_frequency: Minimum frequency from which the power spectral density will be computed.
        :type minimum_frequency: float
        :param maximum_frequency: Maximum frequency from which the power spectral density will be computed.
        :type maximum_frequency: float
        :param minimum_time: Minimum time of the epochs from which the power spectral density will be computed.
        :type minimum_time: float
        :param maximum_time: Maximum time of the epochs from which the power spectral density will be computed.
        :type maximum_time: float
        :param topo_time_points: The time points for the topomaps.
        :type topo_time_points: list of float
        :param channel_selected: Channel selected for the ERP.
        :type channel_selected: str
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        self.main_listener.statistics_psd_information(minimum_frequency, maximum_frequency, minimum_time, maximum_time,
                                                      topo_time_points, channel_selected, stats_first_variable, stats_second_variable)
        self.statistics_psd_view.close()

    def plot_psd(self, psd_fig_one, topo_fig_one, psd_fig_two, topo_fig_two):
        """
        Send the information to the view for plotting the power spectral density computed.
        :param psd_fig_one: The figure of the actual power spectral density's data computed on the first independent variable
        :type psd_fig_one: matplotlib.Figure
        :param topo_fig_one: The figure of the topographies of the actual power spectral density's data computed on the first independent variable
        :type topo_fig_one: matplotlib.Figure
        :param psd_fig_two: The figure of the actual power spectral density's data computed on the second independent variable
        :type psd_fig_two: matplotlib.Figure
        :param topo_fig_two: The figure of the topographies of the actual power spectral density's data computed on the second independent variable
        :type topo_fig_two: matplotlib.Figure
        """
        self.statistics_psd_view.plot_psd(psd_fig_one, topo_fig_one, psd_fig_two, topo_fig_two)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :param elements_selected: Elements selected in the multiple elements' selector.
        :type elements_selected: list of str
        """
        self.statistics_psd_view.set_channels_selected(elements_selected)

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
