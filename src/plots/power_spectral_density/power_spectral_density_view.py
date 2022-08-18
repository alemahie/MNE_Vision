#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Power spectral density view
"""

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton, QLabel

from utils.view.error_window import errorWindow


__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class powerSpectralDensityView(QWidget):
    def __init__(self, minimum_time, maximum_time):
        """
        Window displaying the parameters for computing the power spectral density on the dataset.
        :param minimum_time: Minimum time of the epochs from which the power spectral density can be computed.
        :type minimum_time: float
        :param maximum_time: Maximum time of the epochs from which the power spectral density can be computed.
        :type maximum_time: float
        """
        super().__init__()
        self.power_spectral_density_listener = None

        self.setWindowTitle("Power Spectral Density")

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # self.method_box = QComboBox()
        # self.method_box.addItems(["Welch", "Multitaper"])

        self.minimum_frequency_line = QLineEdit("2,0")
        self.minimum_frequency_line.setValidator(QDoubleValidator())
        self.maximum_frequency_line = QLineEdit("25,0")
        self.maximum_frequency_line.setValidator(QDoubleValidator())
        self.minimum_time_line = QLineEdit(str(minimum_time))
        self.minimum_time_line.setValidator(QDoubleValidator(minimum_time, maximum_time, 3))
        self.maximum_time_line = QLineEdit(str(maximum_time))
        self.maximum_time_line.setValidator(QDoubleValidator(minimum_time, maximum_time, 3))
        self.time_points_line = QLineEdit("6 10 22")

        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_power_spectral_density_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_power_spectral_density_trigger)

        # self.grid_layout.addWidget(QLabel("Method for PSD : "), 0, 0)
        # self.grid_layout.addWidget(self.method_box, 0, 1)
        self.grid_layout.addWidget(QLabel("Minimum frequency of interest (Hz) : "), 1, 0)
        self.grid_layout.addWidget(self.minimum_frequency_line, 1, 1)
        self.grid_layout.addWidget(QLabel("Maximum frequency of interest (Hz) : "), 2, 0)
        self.grid_layout.addWidget(self.maximum_frequency_line, 2, 1)
        self.grid_layout.addWidget(QLabel("Minimum time of interest (sec) : "), 3, 0)
        self.grid_layout.addWidget(self.minimum_time_line, 3, 1)
        self.grid_layout.addWidget(QLabel("Maximum time of interest (sec) : "), 4, 0)
        self.grid_layout.addWidget(self.maximum_time_line, 4, 1)
        self.grid_layout.addWidget(QLabel("Time points for the topographies to plot (sec) : "), 5, 0)
        self.grid_layout.addWidget(self.time_points_line, 5, 1)
        self.grid_layout.addWidget(self.cancel, 6, 0)
        self.grid_layout.addWidget(self.confirm, 6, 1)

    @staticmethod
    def plot_psd(psd_fig, topo_fig):
        """
        Plot the power spectral density.
        :param psd_fig: The figure of the actual power spectral density's data computed
        :type psd_fig: matplotlib.Figure
        :param topo_fig: The figure of the topographies of the actual power spectral density's data computed
        :type topo_fig: matplotlib.Figure
        """
        try:
            topo_fig.show()
            psd_fig.show()
        except Exception as error:
            error_message = "An error has occurred during the computation of the PSD"
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()

    """
    Triggers
    """
    def cancel_power_spectral_density_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.power_spectral_density_listener.cancel_button_clicked()

    def confirm_power_spectral_density_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        # method_psd = self.method_box.currentText()
        minimum_frequency = None
        maximum_frequency = None
        if self.minimum_frequency_line.hasAcceptableInput():
            minimum_frequency = float(self.minimum_frequency_line.text().replace(',', '.'))
        if self.maximum_frequency_line.hasAcceptableInput():
            maximum_frequency = float(self.maximum_frequency_line.text().replace(',', '.'))
        minimum_time = float(self.minimum_time_line.text().replace(',', '.'))
        maximum_time = float(self.maximum_time_line.text().replace(',', '.'))
        topo_time_points = self.create_array_from_time_points()
        self.power_spectral_density_listener.confirm_button_clicked(minimum_frequency, maximum_frequency, minimum_time,
                                                                    maximum_time, topo_time_points)

    """
    Utils
    """
    def create_array_from_time_points(self):
        """
        Create an array of time points depending on the time points given.
        :return: The time points for the topomaps.
        :rtype: list of float
        """
        try:
            time_points = self.time_points_line.text()
            if time_points == "":
                return [6.0, 10.0, 22.0]
            else:
                split_time_points = time_points.split()
                float_time_points = []
                for time_point in split_time_points:
                    float_time_points.append(float(time_point.replace(',', '.')))
                return float_time_points
        except Exception as error:
            error_message = "The time points provided are not following the right format, please use integer separated " \
                            "by spaces."
            error_window = errorWindow(error_message)
            error_window.show()

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: powerSpectralDensityController
        """
        self.power_spectral_density_listener = listener
