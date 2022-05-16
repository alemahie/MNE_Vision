#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Power spectral density controller
"""

from plots.power_spectral_density.power_spectral_density_listener import powerSpectralDensityListener
from plots.power_spectral_density.power_spectral_density_view import powerSpectralDensityView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class powerSpectralDensityController(powerSpectralDensityListener):
    def __init__(self, minimum_time, maximum_time):
        """
        Controller for computing the power spectral density on the dataset.
        Create a new window for specifying some parameters.
        :param minimum_time: Minimum time of the epochs from which the power spectral density can be computed.
        :type minimum_time: float
        :param maximum_time: Maximum time of the epochs from which the power spectral density can be computed.
        :type maximum_time: float
        """
        self.main_listener = None
        self.power_spectral_density_view = powerSpectralDensityView(minimum_time, maximum_time)
        self.power_spectral_density_view.set_listener(self)

        self.power_spectral_density_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.power_spectral_density_view.close()

    def confirm_button_clicked(self, method_psd, minimum_frequency, maximum_frequency, minimum_time, maximum_time):
        """
        Close the window and send the information to the main controller.
        :param method_psd: Method used to compute the power spectral density.
        :type method_psd: str
        :param minimum_frequency: Minimum frequency from which the power spectral density will be computed.
        :type minimum_frequency: float
        :param maximum_frequency: Maximum frequency from which the power spectral density will be computed.
        :type maximum_frequency: float
        :param minimum_time: Minimum time of the epochs from which the power spectral density will be computed.
        :type minimum_time: float
        :param maximum_time: Maximum time of the epochs from which the power spectral density will be computed.
        :type maximum_time: float
        """
        self.main_listener.plot_spectra_maps_information(method_psd, minimum_frequency, maximum_frequency, minimum_time,
                                                         maximum_time)
        self.power_spectral_density_view.close()

    def plot_psd(self, psds, freqs):
        """
        Send the information to the view for plotting the power spectral density computed.
        :param psds: The actual power spectral density data computed
        :type psds: list of, list of, list of float
        :param freqs: The frequencies at which the power spectral density is computed.
        :type freqs: list of float
        """
        self.power_spectral_density_view.plot_psd(psds, freqs)

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
