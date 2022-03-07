#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Resampling controller
"""

from tools.resampling.resampling_view import resamplingView
from tools.resampling.resampling_listener import resamplingListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class resamplingController(resamplingListener):
    def __init__(self, frequency):
        self.main_listener = None
        self.resampling_view = resamplingView(frequency)
        self.resampling_view.set_listener(self)

        self.resampling_view.show()

    def cancel_button_clicked(self):
        self.resampling_view.close()

    def confirm_button_clicked(self, frequency):
        self.main_listener.resampling_information(frequency)
        self.resampling_view.close()

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
