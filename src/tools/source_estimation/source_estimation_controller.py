#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source estimation controller
"""

from tools.source_estimation.source_estimation_view import sourceEstimationView
from tools.source_estimation.source_estimation_listener import sourceEstimationListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sourceEstimationController(sourceEstimationListener):
    def __init__(self, title=None):
        """
        Controller for computing the source estimation on the dataset.
        Create a new window for specifying some parameters.
        :param title: Title of window
        :type title: str
        """
        self.main_listener = None
        self.source_estimation_view = sourceEstimationView(title)
        self.source_estimation_view.set_listener(self)

        self.source_estimation_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.source_estimation_view.close()

    def confirm_button_clicked(self, source_estimation_method, save_data, load_data, n_jobs):
        """
        Close the window and send the information to the main controller.
        :param source_estimation_method: The method used to compute the source estimation
        :type source_estimation_method: str
        :param save_data: Boolean telling if the data computed must be saved into files.
        :type save_data: bool
        :param load_data: Boolean telling if the data used for the computation can be read from computer files.
        :type load_data: bool
        :param n_jobs: Number of processes used to compute the source estimation
        :type n_jobs: int
        """
        self.source_estimation_view.close()
        self.main_listener.source_estimation_information(source_estimation_method, save_data, load_data, n_jobs)

    def plot_source_estimation(self, source_estimation_data):
        """
        Send the information to the view for plotting the source estimation.
        :param source_estimation_data: The source estimation's data.
        :type source_estimation_data: MNE.SourceEstimation
        """
        self.source_estimation_view.plot_source_estimation(source_estimation_data)

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
