#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Time frequency (ERSP/ITC) controller
"""


__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"

from plots.time_frequency_ersp_itc.time_frequency_ersp_itc_listener import timeFrequencyErspItcListener
from plots.time_frequency_ersp_itc.time_frequency_ersp_itc_view import timeFrequencyErspItcView


class timeFrequencyErspItcController(timeFrequencyErspItcListener):
    def __init__(self, all_channels_names):
        self.main_listener = None
        self.time_frequency_ersp_itc_view = timeFrequencyErspItcView(all_channels_names)
        self.time_frequency_ersp_itc_view.set_listener(self)

        self.time_frequency_ersp_itc_view.show()

    def cancel_button_clicked(self):
        self.time_frequency_ersp_itc_view.close()

    def confirm_button_clicked(self, method_tfr, channel_selected, min_frequency, max_frequency):
        self.time_frequency_ersp_itc_view.close()
        self.main_listener.plot_time_frequency_information(method_tfr, channel_selected, min_frequency, max_frequency)

    def plot_ersp_itc(self, channel_selected, power, itc):
        self.time_frequency_ersp_itc_view.plot_ersp_itc(channel_selected, power, itc)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        self.time_frequency_ersp_itc_view.set_channels_selected(elements_selected)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
