#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Event Values Controller
"""

from edit.event_values.event_values_listener import eventValuesListener
from edit.event_values.event_values_view import eventValuesView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class eventValuesController(eventValuesListener):
    def __init__(self, event_values, event_ids):
        self.main_listener = None
        self.event_values_view = eventValuesView(event_values, event_ids)
        self.event_values_view.set_listener(self)

        self.event_values_view.show()

        self.event_values = event_values
        self.event_ids = event_ids
        self.current_event_number = 0
        self.update_event_displayed()

    def cancel_button_clicked(self):
        self.event_values_view.close()

    def confirm_button_clicked(self):
        self.event_values_view.close()

    def previous_button_clicked(self):
        if self.current_event_number == 0:
            self.current_event_number = len(self.event_values) - 1
        else:
            self.current_event_number -= 1
        self.update_event_displayed()

    def next_button_clicked(self):
        if self.current_event_number == len(self.event_values)-1:
            self.current_event_number = 0
        else:
            self.current_event_number += 1
        self.update_event_displayed()

    def editing_finished_clicked(self, event_number):
        self.current_event_number = event_number
        self.update_event_displayed()

    """
    Updates
    """
    def update_event_displayed(self):
        event_name, epoch_number = self.get_event_info_from_number(self.current_event_number)
        self.event_values_view.update_event_displayed(self.current_event_number, event_name, epoch_number)

    """
    Getters
    """
    def get_event_info_from_number(self, event_number):
        current_event_id = self.event_values[event_number][2]
        current_event_name = None
        for event_name in self.event_ids.keys():
            if self.event_ids[event_name] == current_event_id:
                current_event_name = event_name
                break
        epoch_number = event_number
        return current_event_name, epoch_number

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
