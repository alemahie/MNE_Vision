#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dataset info controller
"""

from edit.dataset_info.dataset_info_view import datasetInfoView
from edit.dataset_info.dataset_info_listener import datasetInfoListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"

from utils.view.error_window import errorWindow


class datasetInfoController(datasetInfoListener):
    def __init__(self, all_channels_names):
        """
        Controller for editing some dataset information.
        Create a new window for displaying the dataset's information.
        """
        self.main_listener = None
        self.dataset_info_view = datasetInfoView(all_channels_names)
        self.dataset_info_view.set_listener(self)

        self.dataset_info_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.dataset_info_view.close()

    def confirm_button_clicked(self, channels_selected):
        """
        Close the window and send the information to the main controller.
        """
        self.main_listener.dataset_info_information(channels_selected)
        self.dataset_info_view.close()

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
            error_message = "Please select at least one element in the list. \n The SNR can not be computed on 0 trials"
            error_window = errorWindow(error_message)
            error_window.show()
        else:
            self.dataset_info_view.check_element_type(elements_selected, element_type)

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
