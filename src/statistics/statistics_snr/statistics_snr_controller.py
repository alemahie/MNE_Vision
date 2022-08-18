#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics SNR controller
"""

from statistics.statistics_snr.statistics_snr_listener import statisticsSnrListener
from statistics.statistics_snr.statistics_snr_view import statisticsSnrView

from utils.view.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class statisticsSnrController(statisticsSnrListener):
    def __init__(self, all_channels_names, event_values, event_ids):
        """
        Controller for computing the signal-to-noise ratio on the dataset.
        Create a new window for specifying some parameters.
        """
        self.main_listener = None
        self.statistics_snr_view = statisticsSnrView(all_channels_names, event_values, event_ids)
        self.statistics_snr_view.set_listener(self)

        self.statistics_snr_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.statistics_snr_view.close()

    def confirm_button_clicked(self, snr_methods, source_method, read, write, picks, stats_first_variable, stats_second_variable):
        """
        Close the window and send the information to the main controller.
        :param snr_methods: The methods used for computing the SNR
        :type snr_methods: list of str
        :param source_method: The method used for computing the source estimation
        :type source_method: str
        :param read: Boolean telling if the data used for the computation can be read from computer files.
        :type read: bool
        :param write: Boolean telling if the data computed must be saved into files.
        :type write: bool
        :param picks: The list of channels selected used for the computation
        :type picks: list of str
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        self.main_listener.statistics_snr_information(snr_methods, source_method, read, write, picks, stats_first_variable, stats_second_variable)
        self.statistics_snr_view.close()

    """
    Plots
    """
    def plot_SNRs(self, first_SNRs, second_SNRs, t_values, SNR_methods):
        """
        Plot the SNRs
        :param first_SNRs: The SNRs computed over the first independent variable.
        :type first_SNRs: list of, list of float
        :param second_SNRs: The SNRs computed over the second independent variable.
        :type second_SNRs: list of, list of float
        :param t_values: T-values computed over the SNRs of the two independent variables.
        :type t_values: list of float
        :param SNR_methods: SNR methods
        :type SNR_methods: list of str
        """
        self.statistics_snr_view.plot_SNRs(first_SNRs, second_SNRs, t_values, SNR_methods)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected, element_type):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :param elements_selected: Elements selected in the multiple elements' selector.
        :type elements_selected: list of str
        :param element_type: Type of the element selected, used in case multiple element selector windows can be open in
        a window. Can thus distinguish the returned elements.
        :type element_type: str
        """
        if len(elements_selected) == 0:
            error_message = "Please select at least one element in the list. \n The SNR can not be computed on 0 trials"
            error_window = errorWindow(error_message)
            error_window.show()
        else:
            self.statistics_snr_view.check_element_type(elements_selected, element_type)

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
