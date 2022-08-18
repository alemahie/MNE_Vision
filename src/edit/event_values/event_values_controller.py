#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Event Values Controller
"""

import numpy as np

from copy import copy

from edit.event_values.event_values_listener import eventValuesListener
from edit.event_values.event_values_view import eventValuesView

from utils.view.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class eventValuesController(eventValuesListener):
    def __init__(self, file_type, event_values, event_ids, number_of_epochs, number_of_frames):
        """
        Controller for editing the events' information
        Create a new window for displaying the events' information.
        :param file_type: The type of the file, either "Epochs" or "Raw"
        :type file_type: str
        :param event_values: Event values
        :type event_values: list of, list of int
        :param event_ids: Event ids
        :type event_ids: dict
        :param number_of_epochs: The number of epochs
        :type number_of_epochs: int
        :param number_of_frames: The number of frames
        :type number_of_frames: int
        """
        self.main_listener = None
        self.event_values_view = eventValuesView(event_values, event_ids, number_of_epochs, number_of_frames)
        self.event_values_view.set_listener(self)

        self.event_values_view.show()

        self.file_type = file_type
        self.event_values = np.copy(event_values)
        self.event_ids = copy(event_ids)
        self.number_of_epochs = number_of_epochs
        self.number_of_frames = number_of_frames
        self.current_event_number = 0

        self.update_event_displayed()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.event_values_view.close()

    def confirm_button_clicked(self, event_name, latency):
        """
        Close the window and send the information to the main controller.
        Display an error message if the number of events is different from the number of epochs, because there must be
        a event for each epoch.
        :param event_name: The event name.
        :type event_name: str
        :param latency: The latency of the event.
        :type latency: int
        """
        if self.file_type == "Raw" or len(self.event_values) == self.number_of_epochs:
            # If file type is not "Raw", then it is "Epochs" and number of event must be equal to number epochs.
            self.update_event_data(event_name, latency)
            self.main_listener.event_values_finished(self.event_values, self.event_ids)
            self.event_values_view.close()
        else:
            error_message = f"You must have a number of events that is equal to the number of epochs (1 event per " \
                            f"epoch).\n There are {self.number_of_epochs} in your dataset"
            error_window_view = errorWindow(error_message)
            error_window_view.show()

    def previous_button_clicked(self, event_name, latency):
        """
        Save the information of the last event displayed before displaying the information of the previous event.
        :param event_name: The event name.
        :type event_name: str
        :param latency: The latency of the event.
        :type latency: int
        """
        self.update_event_data(event_name, latency)
        if self.current_event_number == 0:
            self.current_event_number = len(self.event_values) - 1
        else:
            self.current_event_number -= 1
        self.update_event_displayed()

    def next_button_clicked(self, event_name, latency):
        """
        Save the information of the last event displayed before displaying the information of the next event.
        :param event_name: The event name.
        :type event_name: str
        :param latency: The latency of the event.
        :type latency: int
        """
        self.update_event_data(event_name, latency)
        if self.current_event_number == len(self.event_values)-1:
            self.current_event_number = 0
        else:
            self.current_event_number += 1
        self.update_event_displayed()

    def delete_button_clicked(self):
        """
        Delete the information of the event displayed.
        """
        if len(self.event_values) > 1:
            self.event_values = np.delete(self.event_values, self.current_event_number, 0)
            if len(self.event_values) <= self.current_event_number:
                self.current_event_number -= 1
            self.event_values_view.set_event_values(self.event_values)
            self.update_event_ids()
            self.update_event_displayed()
        else:
            error_message = "You can not delete all the events."
            error_window_view = errorWindow(error_message)
            error_window_view.show()

    def insert_button_clicked(self, event_name, latency):
        """
        Save the information of the last event displayed before inserting a new event.
        :param event_name: The event name.
        :type event_name: str
        :param latency: The latency of the event.
        :type latency: int
        """
        self.update_event_data(event_name, latency)
        if "none" not in self.event_ids.keys():
            self.insert_new_event_id()
        event_to_insert = np.array([self.event_values[self.current_event_number][0], 0, self.event_ids["none"]])
        self.event_values = np.insert(self.event_values, self.current_event_number+1, event_to_insert, axis=0)
        self.current_event_number += 1
        self.event_values_view.set_event_values(self.event_values)
        self.update_event_displayed()

    def editing_finished_clicked(self, event_number):
        """
        Load the event's information based on the event number given.
        :param event_number: The event number
        :type event_number: int
        """
        self.current_event_number = event_number
        self.update_event_displayed()

    """
    Updates
    """
    def update_event_displayed(self):
        """
        Update the information of the event displayed based on the current event number (could have change because of
        the next, previous, etc. button pushed.
        """
        event_name, latency = self.get_event_info_from_number(self.current_event_number)
        epoch_number = self.get_epoch_number_from_latency(latency)
        self.event_values_view.update_event_displayed(self.current_event_number, event_name, epoch_number, latency)

    def update_event_data(self, event_name, latency):
        """
        Update the information of an event.
        :param event_name: The event name.
        :type event_name: str
        :param latency: The latency of the event.
        :type latency: int
        """
        if event_name not in self.event_ids.keys():
            max_event_id = self.get_max_event_id()
            self.event_ids[event_name] = max_event_id+1
            self.event_values[self.current_event_number][2] = max_event_id+1
        else:
            self.event_values[self.current_event_number][2] = self.event_ids[event_name]
        self.event_values[self.current_event_number][0] = latency
        self.update_event_ids()

    def update_event_ids(self):
        """
        Update the event ids.
        When a new event is inserted or a new event type is created by changing one, a new event id is associated to it.
        If an event id has no event associated to it (e.g. because of the deletion of an event), the event id is removed.
        """
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
        """
        Insert a new event id in the dictionary containing all the event ids.
        """
        max_event_id = self.get_max_event_id()
        self.event_ids["none"] = max_event_id + 1

    """
    Getters
    """
    def get_event_info_from_number(self, event_number):
        """
        Get the information of an event based on an event number.
        :param event_number: The event number
        :type event_number: int
        :return: current_event_name: The event name.
        latency: The event latency.
        :rtype: str, int
        """
        latency = self.event_values[event_number][0]
        current_event_id = self.event_values[event_number][2]
        current_event_name = None
        for event_name in self.event_ids.keys():
            if self.event_ids[event_name] == current_event_id:
                current_event_name = event_name
                break
        return current_event_name, latency

    def get_max_event_id(self):
        """
        Get the greatest event id in the event ids dictionary.
        :return: max_event_id: The greatest event id
        :rtype: int
        """
        max_event_id = 0
        for event_name in self.event_ids.keys():
            event_id = self.event_ids[event_name]
            if event_id > max_event_id:
                max_event_id = event_id
        return max_event_id

    def get_epoch_number_from_latency(self, latency):
        """
        Get the number of the epoch associated to the latency given.
        :param latency: The latency
        :type latency: int
        :return: epoch_number: The epoch number
        :rtype: int
        """
        epoch_number = 0
        total_latency = 0
        for i in range(self.number_of_epochs):
            total_latency += self.number_of_frames
            if total_latency > latency:
                break
            else:
                epoch_number += 1
        return epoch_number

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
