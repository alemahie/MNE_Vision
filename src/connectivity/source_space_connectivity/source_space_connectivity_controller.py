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
        """
        Controller for computing the source space connectivity on the dataset.
        Create a new window for specifying some parameters.
        :param number_of_channels: The number of channels.
        :type number_of_channels: int
        """
        self.main_listener = None
        self.source_space_connectivity_view = sourceSpaceConnectivityView(number_of_channels)
        self.source_space_connectivity_view.set_listener(self)

        self.source_space_connectivity_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.source_space_connectivity_view.close()

    def confirm_button_clicked(self, connectivity_method, spectrum_estimation_method, source_estimation_method, save_data,
                               load_data, n_jobs):
        """
        Close the window and send the information to the main controller.
        :param connectivity_method: Method used for computing the source space connectivity.
        :type connectivity_method: str
        :param spectrum_estimation_method: Method used for computing the spectrum estimation used inside the computation
        of the source space connectivity.
        :type spectrum_estimation_method: str
        :param source_estimation_method: Method used for computing the source estimation used inside the computation of
        the source space connectivity.
        :type source_estimation_method: str
        :param save_data: Boolean telling if the data computed must be saved into files.
        :type save_data: bool
        :param load_data: Boolean telling if the data used for the computation can be read from computer files.
        :type load_data: bool
        :param n_jobs: Number of processes used to compute the source estimation
        :type n_jobs: int
        """
        self.source_space_connectivity_view.close()
        self.main_listener.source_space_connectivity_information(connectivity_method, spectrum_estimation_method, source_estimation_method,
                                                                 save_data, load_data, n_jobs)

    def plot_source_space_connectivity(self, source_space_connectivity_data):
        """
        Send the information to the view to plot the source space connectivity.
        :param source_space_connectivity_data: The source space connectivity data.
        :type source_space_connectivity_data: list of, list of float
        """
        self.source_space_connectivity_view.plot_source_space_connectivity(source_space_connectivity_data)

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
