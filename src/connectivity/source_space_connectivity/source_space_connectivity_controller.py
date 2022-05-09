#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source Space Connectivity Controller
"""

from connectivity.source_space_connectivity.source_space_connectivity_listener import sourceSpaceConnectivityListener
from connectivity.source_space_connectivity.source_space_connectivity_view import sourceSpaceConnectivityView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sourceSpaceConnectivityController(sourceSpaceConnectivityListener):
    def __init__(self, number_of_channels):
        self.main_listener = None
        self.source_space_connectivity_view = sourceSpaceConnectivityView(number_of_channels)
        self.source_space_connectivity_view.set_listener(self)

        self.source_space_connectivity_view.show()

    def cancel_button_clicked(self):
        self.source_space_connectivity_view.close()

    def confirm_button_clicked(self, source_estimation_method, save_data, load_data, n_jobs):
        self.source_space_connectivity_view.close()
        self.main_listener.source_space_connectivity_information(source_estimation_method, save_data, load_data, n_jobs)

    def plot_source_space_connectivity(self, source_space_connectivity_data):
        self.source_space_connectivity_view.plot_source_space_connectivity(source_space_connectivity_data)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
