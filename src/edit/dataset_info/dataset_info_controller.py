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


class datasetInfoController(datasetInfoListener):
    def __init__(self, sampling_rate, number_of_frames, start_time):
        """
        Controller for editing some dataset information.
        Create a new window for displaying the dataset's information.
        :param sampling_rate: The sampling rate
        :type sampling_rate: float
        :param number_of_frames: The number of frames
        :type number_of_frames: int
        :param start_time: The start time of an epoch or the raw file.
        :type start_time: float
        """
        self.main_listener = None
        self.dataset_info_view = datasetInfoView(sampling_rate, number_of_frames, start_time)
        self.dataset_info_view.set_listener(self)

        self.dataset_info_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.dataset_info_view.close()

    def confirm_button_clicked(self):
        """
        Close the window and send the information to the main controller.
        """
        self.dataset_info_view.close()

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
