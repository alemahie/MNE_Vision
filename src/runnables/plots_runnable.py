#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plots runnable
"""

from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

from mne.time_frequency import psd_welch, psd_multitaper

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class powerSpectralDensityWorkerSignals(QObject):
    finished = pyqtSignal()


class powerSpectralDensityRunnable(QRunnable):
    def __init__(self, file_data, method_psd, minimum_frequency, maximum_frequency):
        super().__init__()
        self.signals = powerSpectralDensityWorkerSignals()

        self.file_data = file_data
        self.method_psd = method_psd
        self.minimum_frequency = minimum_frequency
        self.maximum_frequency = maximum_frequency
        self.psds = None
        self.freqs = None

    def run(self):
        if self.method_psd == "Welch":
            self.psds, self.freqs = psd_welch(self.file_data, fmin=self.minimum_frequency, fmax=self.maximum_frequency)
        elif self.method_psd == "Multitaper":
            self.psds, self.freqs = psd_multitaper(self.file_data, fmin=self.minimum_frequency, fmax=self.maximum_frequency)
        self.signals.finished.emit()

    def get_psds(self):
        return self.psds

    def get_freqs(self):
        return self.freqs
