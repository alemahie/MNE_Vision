#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sensor Space Connectivity Controller
"""

from connectivity.sensor_space_connectivity.spectral_connectivity_listener import sensorSpaceConnectivityListener
from connectivity.sensor_space_connectivity.spectral_connectivity_view import sensorSpaceConnectivityView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sensorSpaceConnectivityController(sensorSpaceConnectivityListener):
    def __init__(self, file_info):
        self.main_listener = None
        self.sensor_space_connectivity_view = sensorSpaceConnectivityView(file_info)
        self.sensor_space_connectivity_view.set_listener(self)

        self.sensor_space_connectivity_view.show()

    def cancel_button_clicked(self):
        self.sensor_space_connectivity_view.close()

    def confirm_button_clicked(self):
        self.sensor_space_connectivity_view.close()
        self.main_listener.sensor_space_connectivity_information()

    def plot_sensor_space_connectivity(self, sensor_space_connectivity_data):
        self.sensor_space_connectivity_view.plot_sensor_space_connectivity(sensor_space_connectivity_data)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
