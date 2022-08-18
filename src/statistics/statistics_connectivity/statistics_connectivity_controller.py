#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics Connectivity Controller
"""

from statistics.statistics_connectivity.statistics_connectivity_listener import statisticsConnectivityListener
from statistics.statistics_connectivity.statistics_connectivity_view import statisticsConnectivityView

from utils.data_exportation.data_exportation_controller import dataExportationController

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class statisticsConnectivityController(statisticsConnectivityListener):
    def __init__(self, number_of_channels, file_data, event_ids):
        """
        Controller for computing the envelope correlation on the dataset.
        Create a new window for specifying some parameters.
        :param number_of_channels: The number of channels
        :type number_of_channels: int
        :param file_data: The dataset data
        :type file_data: MNE.Info
        :param event_ids: The events' ids
        :type event_ids: dict
        """
        self.main_listener = None
        self.envelope_correlation_view = statisticsConnectivityView(number_of_channels, file_data, event_ids)
        self.envelope_correlation_view.set_listener(self)

        self.source_estimation_controller = None
        self.export_data_controller = None
        self.export_path = None

        self.envelope_correlation_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.envelope_correlation_view.close()

    def confirm_button_clicked(self, psi, fmin, fmax, connectivity_method, n_jobs, stats_first_variable, stats_second_variable):
        """
        Close the window and send the information to the main controller.
        :param psi: Check if the computation of the Phase Slope Index must be done. The PSI give an indication to the
        directionality of the connectivity.
        :type psi: bool
        :param fmin: Minimum frequency from which the envelope correlation will be computed.
        :type fmin: float
        :param fmax: Maximum frequency from which the envelope correlation will be computed.
        :type fmax: float
        :param connectivity_method: Method used for computing the source space connectivity.
        :type connectivity_method: str
        :param n_jobs: Number of processes used to compute the source estimation
        :type n_jobs: int
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        self.envelope_correlation_view.close()
        self.main_listener.statistics_connectivity_information(psi, fmin, fmax, connectivity_method, n_jobs, self.export_path,
                                                               stats_first_variable, stats_second_variable)

    def additional_parameters_clicked(self):
        """
        Create a new window for specifying the exportation path of the computation of the envelope correlation.
        """
        self.export_data_controller = dataExportationController()
        self.export_data_controller.set_listener(self)

    def additional_parameters_information(self, export_path):
        """
        Retrieve the exportation path for the envelope correlation data computed.
        :param export_path: Path where the envelope correlation data will be stored.
        :type export_path: str
        """
        self.export_path = export_path

    """
    Plot
    """
    def plot_envelope_correlation(self, connectivity_data_one, connectivity_data_two, psi_data_one, psi_data_two, channel_names):
        """
        Send the information to the view to plot the connectivity and the statistics computed on it.
        :param connectivity_data_one: The envelope correlation data of the first independent variable to plot.
        :type connectivity_data_one: list of, list of float
        :param connectivity_data_two: The envelope correlation data of the second independent variable to plot.
        :type connectivity_data_two: list of, list of float
        :param psi_data_one: Values of the computation of the PSI, if None then the computation has not been done.
        The PSI give an indication to the directionality of the connectivity of the first independent variable.
        :type psi_data_one: list of, list of float
        :param psi_data_two: Values of the computation of the PSI, if None then the computation has not been done.
        The PSI give an indication to the directionality of the connectivity of the second independent variable.
        :type psi_data_two: list of, list of float
        :param channel_names: Channels' names
        :type channel_names: list of str
        """
        self.envelope_correlation_view.plot_envelope_correlation(connectivity_data_one, connectivity_data_two, psi_data_one,
                                                                 psi_data_two, channel_names)

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
