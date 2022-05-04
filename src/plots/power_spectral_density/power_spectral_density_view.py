#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Power spectral density view
"""

import numpy as np
from matplotlib import pyplot as plt

from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton, QLabel

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class powerSpectralDensityView(QWidget):
    def __init__(self, minimum_time, maximum_time):
        super().__init__()
        self.power_spectral_density_listener = None

        self.setWindowTitle("Power Spectral Density")

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.method_box = QComboBox()
        self.method_box.addItems(["Welch", "Multitaper"])

        self.minimum_frequency_line = QLineEdit("2,0")
        self.minimum_frequency_line.setValidator(QDoubleValidator())
        self.maximum_frequency_line = QLineEdit("25,0")
        self.maximum_frequency_line.setValidator(QDoubleValidator())
        self.minimum_time_line = QLineEdit(str(minimum_time))
        self.minimum_time_line.setValidator(QDoubleValidator(minimum_time, maximum_time, 3))
        self.maximum_time_line = QLineEdit(str(maximum_time))
        self.maximum_time_line.setValidator(QDoubleValidator(minimum_time, maximum_time, 3))

        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_power_spectral_density_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_power_spectral_density_trigger)

        self.grid_layout.addWidget(QLabel("Method for PSD : "), 0, 0)
        self.grid_layout.addWidget(self.method_box, 0, 1)
        self.grid_layout.addWidget(QLabel("Minimum frequency of interest (Hz) : "), 1, 0)
        self.grid_layout.addWidget(self.minimum_frequency_line, 1, 1)
        self.grid_layout.addWidget(QLabel("Maximum frequency of interest (Hz) : "), 2, 0)
        self.grid_layout.addWidget(self.maximum_frequency_line, 2, 1)
        self.grid_layout.addWidget(QLabel("Minimum time of interest (sec) : "), 3, 0)
        self.grid_layout.addWidget(self.minimum_time_line, 3, 1)
        self.grid_layout.addWidget(QLabel("Maximum time of interest (sec) : "), 4, 0)
        self.grid_layout.addWidget(self.maximum_time_line, 4, 1)
        self.grid_layout.addWidget(self.cancel, 5, 0)
        self.grid_layout.addWidget(self.confirm, 5, 1)

    @staticmethod
    def plot_psd(psds, freqs):
        psds_plot = 10 * np.log10(psds)
        psds_mean = psds_plot.mean(axis=(0, 1))
        psds_std = psds_plot.std(axis=(0, 1))
        plt.plot(freqs, psds_mean, color='b')
        plt.fill_between(freqs, psds_mean - psds_std, psds_mean + psds_std, color='b', alpha=.2)
        plt.title("PSD spectrum")
        plt.ylabel("Power Spectral Density [dB]")
        plt.xlabel("Frequency [Hz]")
        plt.show()

    """
    Triggers
    """
    def cancel_power_spectral_density_trigger(self):
        self.power_spectral_density_listener.cancel_button_clicked()

    def confirm_power_spectral_density_trigger(self):
        method_psd = self.method_box.currentText()
        minimum_frequency = None
        maximum_frequency = None
        if self.minimum_frequency_line.hasAcceptableInput():
            minimum_frequency = float(self.minimum_frequency_line.text().replace(',', '.'))
        if self.maximum_frequency_line.hasAcceptableInput():
            maximum_frequency = float(self.maximum_frequency_line.text().replace(',', '.'))
        minimum_time = float(self.minimum_time_line.text().replace(',', '.'))
        maximum_time = float(self.maximum_time_line.text().replace(',', '.'))
        self.power_spectral_density_listener.confirm_button_clicked(method_psd, minimum_frequency, maximum_frequency,
                                                                    minimum_time, maximum_time)

    """
    Setters
    """
    def set_listener(self, listener):
        self.power_spectral_density_listener = listener
