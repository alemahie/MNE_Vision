#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plots runnable
"""

import numpy as np
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject

from mne.time_frequency import psd_welch, psd_multitaper, tfr_morlet, tfr_multitaper, tfr_stockwell

from utils.view.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


# Power Spectral Density
class powerSpectralDensityWorkerSignals(QObject):
    """
    Contain the signals used by the power spectral density runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class powerSpectralDensityRunnable(QRunnable):
    def __init__(self, file_data, method_psd, minimum_frequency, maximum_frequency, minimum_time, maximum_time):
        """
        Runnable for the computation of the power spectral density of the given data.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
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
        super().__init__()
        self.signals = powerSpectralDensityWorkerSignals()

        self.file_data = file_data
        self.method_psd = method_psd
        self.minimum_frequency = minimum_frequency
        self.maximum_frequency = maximum_frequency
        self.tmin = minimum_time
        self.tmax = maximum_time
        self.psds = None
        self.freqs = None

    def run(self):
        """
        Launch the computation of the power spectral density on the given data.
        Notifies the main model that the computation is finished.
        """
        try:
            if self.method_psd == "Welch":
                self.psds, self.freqs = psd_welch(self.file_data, fmin=self.minimum_frequency, fmax=self.maximum_frequency,
                                                  tmin=self.tmin, tmax=self.tmax)
            elif self.method_psd == "Multitaper":
                self.psds, self.freqs = psd_multitaper(self.file_data, fmin=self.minimum_frequency, fmax=self.maximum_frequency,
                                                       tmin=self.tmin, tmax=self.tmax)
            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error has occured during the computation of the PSD"
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()

    def get_psds(self):
        """
        Get the power spectral density's data
        :return: The actual power spectral density's data computed
        :rtype: list of, list of, list of float
        """
        return self.psds

    def get_freqs(self):
        """
        Get the frequencies of the power spectral density computation.
        :return: The frequencies at which the power spectral density is computed.
        :rtype: list of float
        """
        return self.freqs


# Time Frequency
class timeFrequencyWorkerSignals(QObject):
    """
    Contain the signals used by the time-frequency runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class timeFrequencyRunnable(QRunnable):
    def __init__(self, file_data, method_tfr, channel_selected, min_frequency, max_frequency, n_cycles):
        """
        Runnable for the computation of the time-frequency analysis of the given data.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param method_tfr: Method used for computing the time-frequency analysis.
        :type method_tfr: str
        :param channel_selected: Channel on which the time-frequency analysis will be computed.
        :type channel_selected: str
        :param min_frequency: Minimum frequency from which the time-frequency analysis will be computed.
        :type min_frequency: float
        :param max_frequency: Maximum frequency from which the time-frequency analysis will be computed.
        :type max_frequency: float
        :param n_cycles: Number of cycles used by the time-frequency analysis for his computation.
        :type n_cycles: int
        """
        super().__init__()
        self.signals = timeFrequencyWorkerSignals()

        self.file_data = file_data
        self.method_tfr = method_tfr
        self.channel_selected = channel_selected
        self.min_frequency = min_frequency
        self.max_frequency = max_frequency
        self.n_cycles = n_cycles
        self.power = None
        self.itc = None

    def run(self):
        """
        Launch the computation of the time-frequency analysis on the given data.
        Notifies the main model that the computation is finished.
        If to extreme parameters are given and the computation fails, an error message is displayed describing the error.
        Notifies the main model when an error occurs.
        """
        try:
            freqs = np.arange(self.min_frequency, self.max_frequency)
            if self.method_tfr == "Morlet":
                self.power, self.itc = tfr_morlet(self.file_data, freqs=freqs, n_cycles=self.n_cycles,
                                                  picks=self.channel_selected)
            elif self.method_tfr == "Multitaper":
                self.power, self.itc = tfr_multitaper(self.file_data, freqs=freqs, n_cycles=self.n_cycles,
                                                      picks=self.channel_selected)
            elif self.method_tfr == "Stockwell":
                self.power, self.itc = tfr_stockwell(self.file_data, freqs=freqs, n_cycles=self.n_cycles,
                                                     picks=self.channel_selected)
            self.signals.finished.emit()
        except ValueError as error:
            error_message = "An error as occurred during the computation of the time frequency analysis."
            detailed_message = str(error)
            error_window = errorWindow(error_message, detailed_message)
            error_window.show()
            self.signals.error.emit()

    def get_channel_selected(self):
        """
        Get the channel selected for the computation.
        :return: The channel selected.
        :rtype: str
        """
        return self.channel_selected

    def get_power(self):
        """
        Get the "power" data of the time-frequency analysis computation.
        :return: "power" data of the time-frequency analysis computation.
        :rtype: MNE.AverageTFR
        """
        return self.power

    def get_itc(self):
        """
        Get the "itc" data of the time-frequency analysis computation.
        :return: "itc" data of the time-frequency analysis computation.
        :rtype: MNE.AverageTFR
        """
        return self.itc
