#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Find Events From Channel Controller
"""

from file.find_events_from_channel.find_events_from_channel_listener import findEventsFromChannelListener
from file.find_events_from_channel.find_events_from_channel_view import findEventsFromChannelView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class findEventsFromChannelController(findEventsFromChannelListener):
    def __init__(self, all_channels_names):
        self.main_listener = None
        self.find_events_from_channel_view = findEventsFromChannelView(all_channels_names)
        self.find_events_from_channel_view.set_listener(self)

        self.find_events_from_channel_view.show()

    def cancel_button_clicked(self):
        self.find_events_from_channel_view.close()

    def confirm_button_clicked(self, stim_channel):
        self.find_events_from_channel_view.close()
        self.main_listener.find_events_from_channel_information(stim_channel)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        self.find_events_from_channel_view.set_channels_selected(elements_selected)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
