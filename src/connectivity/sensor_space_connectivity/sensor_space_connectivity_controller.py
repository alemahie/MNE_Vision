#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sensor Space Connectivity Controller
"""

from connectivity.sensor_space_connectivity.sensor_space_connectivity_listener import sensorSpaceConnectivityListener
from connectivity.sensor_space_connectivity.sensor_space_connectivity_view import sensorSpaceConnectivityView

from utils.data_exportation.data_exportation_controller import dataExportationController

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sensorSpaceConnectivityController(sensorSpaceConnectivityListener):
    def __init__(self, file_info):
        """
        Controller for compute the sensor space connectivity on the dataset.
        Create a new window for specifying some parameters.
        :param file_info: The information file of the MNE object.
        :type file_info: MNE.Info
        """
        self.main_listener = None
        self.sensor_space_connectivity_view = sensorSpaceConnectivityView(file_info)
        self.sensor_space_connectivity_view.set_listener(self)

        self.export_data_controller = None
        self.export_path = None

        self.sensor_space_connectivity_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.sensor_space_connectivity_view.close()

    def confirm_button_clicked(self):
        """
        Close the window and send the information to the main controller.
        """
        self.sensor_space_connectivity_view.close()
        self.main_listener.sensor_space_connectivity_information(self.export_path)

    def additional_parameters_clicked(self):
        """
        Create a new window for specifying the exportation path of the computation of the sensor space connectivity.
        """
        self.export_data_controller = dataExportationController()
        self.export_data_controller.set_listener(self)

    def additional_parameters_information(self, export_path):
        """
        Retrieve the exportation path for the sensor space connectivity data computed.
        :param export_path: Path where the sensor space connectivity data will be stored.
        :type export_path: str
        """
        self.export_path = export_path

    """
    Plot
    """
    def plot_sensor_space_connectivity(self, sensor_space_connectivity_data):
        """
        Send the information to the view to plot the sensor space connectivity.
        :param sensor_space_connectivity_data: The sensor space connectivity data.
        :type sensor_space_connectivity_data: list of, list of float
        """
        self.sensor_space_connectivity_view.plot_sensor_space_connectivity(sensor_space_connectivity_data)

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
