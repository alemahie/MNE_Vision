#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Time frequency (ERSP/ITC) controller
"""


__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"

from plots.time_frequency_ersp_itc.time_frequency_ersp_itc_listener import timeFrequencyErspItcListener
from plots.time_frequency_ersp_itc.time_frequency_ersp_itc_view import timeFrequencyErspItcView


class timeFrequencyErspItcController(timeFrequencyErspItcListener):
    def __init__(self):
        self.main_listener = None
        self.time_frequency_ersp_itc_view = timeFrequencyErspItcView()
        self.time_frequency_ersp_itc_view.set_listener(self)

        self.time_frequency_ersp_itc_view.show()

    def cancel_button_clicked(self):
        self.time_frequency_ersp_itc_view.close()

    def confirm_button_clicked(self):
        self.time_frequency_ersp_itc_view.close()

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
