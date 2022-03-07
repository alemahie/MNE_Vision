#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filter controller
"""

from tools.filter.filter_view import filterView
from tools.filter.filter_listener import filterListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class filterController(filterListener):
    def __init__(self, all_channels_names):
        self.main_listener = None
        self.filter_view = filterView(all_channels_names)
        self.filter_view.set_listener(self)

        self.filter_view.show()

    def cancel_button_clicked(self):
        self.filter_view.close()

    def confirm_button_clicked(self, low_frequency, high_frequency, channels_selected):
        self.main_listener.filter_information(low_frequency, high_frequency, channels_selected)
        self.filter_view.close()

    """
    Getters
    """
    def get_channels_selected(self, channels_selected):
        self.filter_view.set_channels_selected(channels_selected)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
