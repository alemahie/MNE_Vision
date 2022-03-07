#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Channels selector controller
"""

from utils.channels_selector.channels_selector_view import channelsSelectorView
from utils.channels_selector.channels_selector_listener import channelsSelectorListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class channelsSelectorController(channelsSelectorListener):
    def __init__(self, all_channels_names, title, box_checked=True):
        self.main_listener = None
        self.channels_selector_view = channelsSelectorView(all_channels_names, title, box_checked)
        self.channels_selector_view.set_listener(self)

        self.channels_selector_view.show()

    def cancel_button_clicked(self):
        self.channels_selector_view.close()

    def confirm_button_clicked(self, channels_selected):
        self.main_listener.get_channels_selected(channels_selected)
        self.channels_selector_view.close()

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
