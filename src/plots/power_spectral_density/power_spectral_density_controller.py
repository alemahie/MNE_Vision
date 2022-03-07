#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Power spectral density controller
"""

from plots.power_spectral_density.power_spectral_density_listener import powerSpectralDensityListener
from plots.power_spectral_density.power_spectral_density_view import powerSpectralDensityView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class powerSpectralDensityController(powerSpectralDensityListener):
    def __init__(self):
        self.main_listener = None
        self.power_spectral_density_view = powerSpectralDensityView()
        self.power_spectral_density_view.set_listener(self)

        self.power_spectral_density_view.show()

    def cancel_button_clicked(self):
        self.power_spectral_density_view.close()

    def confirm_button_clicked(self, method_psd, minimum_frequency, maximum_frequency):
        self.main_listener.plot_spectra_maps_information(method_psd, minimum_frequency, maximum_frequency)
        self.power_spectral_density_view.close()

    def plot_psd(self, psds, freqs):
        self.power_spectral_density_view.plot_psd(psds, freqs)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
