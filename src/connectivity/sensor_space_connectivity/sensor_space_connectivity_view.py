#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sensor Space Connectivity View
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout

from mne_connectivity.viz import plot_sensors_connectivity

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sensorSpaceConnectivityView(QWidget):
    def __init__(self, file_info):
        """
        Window displaying the parameters for computing the sensor space connectivity on the dataset.
        :param file_info: The information file of the MNE object.
        :type file_info: MNE.Info
        """
        super().__init__()
        self.sensor_space_connectivity_listener = None

        self.file_info = file_info

        self.setWindowTitle("Sensor Space Connectivity")

        self.vertical_layout = QVBoxLayout()

        # Exportation
        self.data_exportation_widget = QWidget()
        self.data_exportation_layout = QHBoxLayout()
        self.data_exportation_button = QPushButton("Data exportation")
        self.data_exportation_button.clicked.connect(self.data_exportation_trigger)
        self.data_exportation_layout.addWidget(self.data_exportation_button)
        self.data_exportation_widget.setLayout(self.data_exportation_layout)

        # Cancel Confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_sensor_space_connectivity_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_sensor_space_connectivity_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.data_exportation_widget)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)
        self.setLayout(self.vertical_layout)

    """
    Plot
    """
    def plot_sensor_space_connectivity(self, sensor_space_connectivity_data):
        """
        Plot the sensor space connectivity data.
        :param sensor_space_connectivity_data: The sensor space connectivity data.
        :type sensor_space_connectivity_data: list of, list of float
        """
        plot_sensors_connectivity(self.file_info, sensor_space_connectivity_data, picks=None)

    """
    Triggers
    """
    def cancel_sensor_space_connectivity_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.sensor_space_connectivity_listener.cancel_button_clicked()

    def confirm_sensor_space_connectivity_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        self.sensor_space_connectivity_listener.confirm_button_clicked()

    def data_exportation_trigger(self):
        """
        Open a new window asking for the path for the exportation of the sensor space connectivity data.
        """
        self.sensor_space_connectivity_listener.additional_parameters_clicked()

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: sensorSpaceConnectivityController
        """
        self.sensor_space_connectivity_listener = listener
