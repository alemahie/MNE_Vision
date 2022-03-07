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
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class powerSpectralDensityView(QWidget):
    def __init__(self):
        super().__init__()
        self.power_spectral_density_listener = None

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.method_box = QComboBox()
        self.method_box.addItems(["Welch", "Multitaper"])

        self.minimum_frequency = QLineEdit("2,0")
        self.minimum_frequency.setValidator(QDoubleValidator())
        self.maximum_frequency = QLineEdit("25,0")
        self.maximum_frequency.setValidator(QDoubleValidator())

        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_power_spectral_density_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_power_spectral_density_trigger)

        self.grid_layout.addWidget(QLabel("Method for PSD : "), 0, 0)
        self.grid_layout.addWidget(self.method_box, 0, 1)
        self.grid_layout.addWidget(QLabel("Minimum frequency of interest : "), 1, 0)
        self.grid_layout.addWidget(self.minimum_frequency, 1, 1)
        self.grid_layout.addWidget(QLabel("Maximum frequency of interest : "), 2, 0)
        self.grid_layout.addWidget(self.maximum_frequency, 2, 1)
        self.grid_layout.addWidget(self.cancel, 3, 0)
        self.grid_layout.addWidget(self.confirm, 3, 1)

    def plot_psd(self, psds, freqs):
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
        if self.minimum_frequency.hasAcceptableInput():
            minimum_frequency = self.minimum_frequency.text()
            minimum_frequency = float(minimum_frequency.replace(',', '.'))
        if self.maximum_frequency.hasAcceptableInput():
            maximum_frequency = self.maximum_frequency.text()
            maximum_frequency = float(maximum_frequency.replace(',', '.'))
        self.power_spectral_density_listener.confirm_button_clicked(method_psd, minimum_frequency, maximum_frequency)

    """
    Setters
    """
    def set_listener(self, listener):
        self.power_spectral_density_listener = listener
