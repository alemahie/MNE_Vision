#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SNR controller
"""

from tools.signal_to_noise_ratio.signal_to_noise_ratio_listener import signalToNoiseRatioListener
from tools.signal_to_noise_ratio.signal_to_noise_ratio_view import signalToNoiseRatioView

from utils.view.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class signalToNoiseRatioController(signalToNoiseRatioListener):
    def __init__(self, all_channels_names, event_values, event_ids):
        """
        Controller for computing the signal-to-noise ratio on the dataset.
        Create a new window for specifying some parameters.
        """
        self.main_listener = None
        self.snr_view = signalToNoiseRatioView(all_channels_names, event_values, event_ids)
        self.snr_view.set_listener(self)

        self.snr_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.snr_view.close()

    def confirm_button_clicked(self, snr_methods, source_method, read, write, picks, trials_selected):
        """
        Close the window and send the information to the main controller.
        """
        self.main_listener.snr_information(snr_methods, source_method, read, write, picks, trials_selected)
        self.snr_view.close()

    """
    Plots
    """
    def plot_SNRs(self, SNRs, SNR_methods):
        """
        Plot the SNRs
        :param SNRs: SNRs
        :type SNRs: list of, list of float
        :param SNR_methods: SNR methods
        :type SNR_methods: list of str
        """
        self.snr_view.plot_SNRs(SNRs, SNR_methods)

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
            self.snr_view.check_element_type(elements_selected, element_type)

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
