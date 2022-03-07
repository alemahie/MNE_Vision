#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dataset info controller
"""

from edit.dataset_info.dataset_info_view import datasetInfoView
from edit.dataset_info.dataset_info_listener import datasetInfoListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class datasetInfoController(datasetInfoListener):
    def __init__(self, sampling_rate, time_points_epochs, start_time):
        self.main_listener = None
        self.dataset_info_view = datasetInfoView(sampling_rate, time_points_epochs, start_time)
        self.dataset_info_view.set_listener(self)

        self.dataset_info_view.show()

    def cancel_button_clicked(self):
        self.dataset_info_view.close()

    def confirm_button_clicked(self):
        self.dataset_info_view.close()

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
