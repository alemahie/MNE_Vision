#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extract Epochs Controller
"""

from tools.extract_epochs.extract_epochs_listener import extractEpochsListener
from tools.extract_epochs.extract_epochs_view import extractEpochsView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"

from utils.view.error_window import errorWindow


class extractEpochsController(extractEpochsListener):
    def __init__(self, event_values, event_ids):
        """
        Controller for extracting epochs from the dataset.
        Create a new window for specifying some parameters.
        :param event_values: Event_id associated to each epoch/trial.
        :type event_values: list of, list of int
        :param event_ids: Name of the events associated to their id.
        :type event_ids: dict
        """
        self.main_listener = None
        self.extract_epochs_view = extractEpochsView(event_values, event_ids)
        self.extract_epochs_view.set_listener(self)

        self.extract_epochs_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.extract_epochs_view.close()

    def confirm_button_clicked(self, tmin, tmax, trials_selected):
        """
        Close the window and send the information to the main controller.
        :param tmin: Start time of the epoch to keep
        :type tmin: float
        :param tmax: End time of the epoch to keep
        :type tmax: float
        """
        self.extract_epochs_view.close()
        self.main_listener.extract_epochs_information(tmin, tmax, trials_selected)

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
            error_message = "Please select at least one element in the list. \n The source estimation can not be " \
                            "computed on 0 trials"
            error_window = errorWindow(error_message)
            error_window.show()
        else:
            self.extract_epochs_view.set_trials_selected(elements_selected, element_type)

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
