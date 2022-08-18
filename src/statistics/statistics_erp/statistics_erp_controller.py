#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics ERP controller
"""

from statistics.statistics_erp.statistics_erp_listener import statisticsErpListener
from statistics.statistics_erp.statistics_erp_view import statisticsErpView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class statisticsErpController(statisticsErpListener):
    def __init__(self, all_channels_names, event_ids):
        """
        Controller for computing the ERPs on the dataset.
        Create a new window for specifying some parameters.
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        :param event_ids: The events' ids
        :type event_ids: dict
        """
        self.main_listener = None
        self.statistics_erp_view = statisticsErpView(all_channels_names, event_ids)
        self.statistics_erp_view.set_listener(self)

        self.statistics_erp_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.statistics_erp_view.close()

    def confirm_button_clicked(self, channels_selected, stats_first_variable, stats_second_variable):
        """
        Close the window and send the information to the main controller.
        :param channels_selected: The channels selected.
        :type channels_selected: list of str
        """
        self.statistics_erp_view.close()
        self.main_listener.statistics_erp_information(channels_selected, stats_first_variable, stats_second_variable)

    """
    Plots
    """
    def plot_erps(self, channels_selected, file_data, stats_first_variable, stats_second_variable):
        """
        Plot the ERPs
        :param channels_selected: The channels selected for the computation
        :type channels_selected: list of str
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        self.statistics_erp_view.plot_erps(channels_selected, file_data, stats_first_variable, stats_second_variable)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :param elements_selected: Elements selected in the multiple elements' selector.
        :type elements_selected: list of str
        """
        self.statistics_erp_view.set_channels_selected(elements_selected)

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
