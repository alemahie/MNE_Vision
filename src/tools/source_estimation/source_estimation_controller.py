#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source estimation controller
"""

from tools.source_estimation.source_estimation_view import sourceEstimationView
from tools.source_estimation.source_estimation_listener import sourceEstimationListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sourceEstimationController(sourceEstimationListener):
    def __init__(self):
        self.main_listener = None
        self.source_estimation_view = sourceEstimationView()
        self.source_estimation_view.set_listener(self)

        self.source_estimation_view.show()

    def cancel_button_clicked(self):
        self.source_estimation_view.close()

    def confirm_button_clicked(self, source_estimation_method, save_data, load_data, n_jobs):
        self.source_estimation_view.close()
        self.main_listener.source_estimation_information(source_estimation_method, save_data, load_data, n_jobs)

    def plot_source_estimation(self, source_estimation_data):
        self.source_estimation_view.plot_source_estimation(source_estimation_data)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
