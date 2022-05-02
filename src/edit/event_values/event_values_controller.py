#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Event Values Controller
"""

import numpy as np

from copy import copy

from edit.event_values.event_values_listener import eventValuesListener
from edit.event_values.event_values_view import eventValuesView

from utils.error_window.error_window_view import errorWindowView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class eventValuesController(eventValuesListener):
    def __init__(self, event_values, event_ids, number_of_epochs):
        self.main_listener = None
        self.event_values_view = eventValuesView(event_values, event_ids)
        self.event_values_view.set_listener(self)

        self.event_values_view.show()

        self.event_values = np.copy(event_values)
        self.event_ids = copy(event_ids)

        self.number_of_epochs = number_of_epochs
        self.current_event_number = 0
        self.update_event_displayed()

    def cancel_button_clicked(self):
        self.event_values_view.close()

    def confirm_button_clicked(self, event_name, latency):
        if len(self.event_values) == self.number_of_epochs:
            self.update_event_data(event_name, latency)
            self.main_listener.event_values_finished(self.event_values, self.event_ids)
            self.event_values_view.close()
        else:
            error_message = f"You must have a number of events that is equal to the number of epochs (1 event per " \
                            f"epoch).\n There are {self.number_of_epochs} in your dataset"
            error_window_view = errorWindowView(error_message)
            error_window_view.show()

    def previous_button_clicked(self, event_name, latency):
        self.update_event_data(event_name, latency)
        if self.current_event_number == 0:
            self.current_event_number = len(self.event_values) - 1
        else:
            self.current_event_number -= 1
        self.update_event_displayed()

    def next_button_clicked(self, event_name, latency):
        self.update_event_data(event_name, latency)
        if self.current_event_number == len(self.event_values)-1:
            self.current_event_number = 0
        else:
            self.current_event_number += 1
        self.update_event_displayed()

    def delete_button_clicked(self):
        if len(self.event_values) > 1:
            self.event_values = np.delete(self.event_values, self.current_event_number, 0)
            if len(self.event_values) <= self.current_event_number:
                self.current_event_number -= 1
            self.event_values_view.set_event_values(self.event_values)
            self.update_event_ids()
            self.update_event_displayed()
        else:
            error_message = "You can not delete all the events."
            error_window_view = errorWindowView(error_message)
            error_window_view.show()

    def insert_button_clicked(self):
        if "none" not in self.event_ids.keys():
            self.insert_new_event_id()
        event_to_insert = np.array([self.event_values[self.current_event_number][0], 0, self.event_ids["none"]])
        self.event_values = np.insert(self.event_values, self.current_event_number+1, event_to_insert, axis=0)
        self.current_event_number += 1
        self.event_values_view.set_event_values(self.event_values)
        self.update_event_displayed()

    def editing_finished_clicked(self, event_number):
        self.current_event_number = event_number
        self.update_event_displayed()

    """
    Updates
    """
    def update_event_displayed(self):
        event_name, epoch_number, latency = self.get_event_info_from_number(self.current_event_number)
        self.event_values_view.update_event_displayed(self.current_event_number, event_name, epoch_number, latency)

    def update_event_data(self, event_name, latency):
        if event_name not in self.event_ids.keys():
            max_event_id = self.get_max_event_id()
            self.event_ids[event_name] = max_event_id+1
            self.event_values[self.current_event_number][2] = max_event_id+1
        else:
            self.event_values[self.current_event_number][2] = self.event_ids[event_name]
        self.event_values[self.current_event_number][0] = latency
        self.update_event_ids()

    def update_event_ids(self):
        events_to_delete = []
        for event in self.event_ids.keys():
            value = self.event_ids[event]
            present = False
            for element in self.event_values:
                if value == element[2]:
                    present = True
            if not present:
                events_to_delete.append(event)
        for event in events_to_delete:
            del self.event_ids[event]

    """
    Others
    """
    def insert_new_event_id(self):
        max_event_id = self.get_max_event_id()
        self.event_ids["none"] = max_event_id + 1

    """
    Getters
    """
    def get_event_info_from_number(self, event_number):
        latency = self.event_values[event_number][0]
        current_event_id = self.event_values[event_number][2]
        current_event_name = None
        for event_name in self.event_ids.keys():
            if self.event_ids[event_name] == current_event_id:
                current_event_name = event_name
                break
        epoch_number = event_number
        return current_event_name, epoch_number, latency

    def get_max_event_id(self):
        max_event_id = 0
        for event_name in self.event_ids.keys():
            event_id = self.event_ids[event_name]
            if event_id > max_event_id:
                max_event_id = event_id
        return max_event_id

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
