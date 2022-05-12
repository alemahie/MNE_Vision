#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Files runnable
"""

from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

from mne import read_epochs, find_events
from mne.io import read_raw_fif, read_raw_eeglab, read_epochs_eeglab

from utils import cnt_file_reader

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class openFifFileWorkerSignals(QObject):
    finished = pyqtSignal()


class openFifFileRunnable(QRunnable):
    def __init__(self, path_to_file):
        super().__init__()
        self.signals = openFifFileWorkerSignals()

        self.path_to_file = path_to_file
        self.file_data = None
        self.file_type = None

    def run(self):
        try:
            if self.path_to_file[-7:-4] == "raw":
                self.file_type = "Raw"
                self.file_data = read_raw_fif(self.path_to_file, preload=True)
            else:
                self.file_type = "Epochs"
                self.file_data = read_epochs(self.path_to_file, preload=True)
        except TypeError:
            print("Error")
        self.signals.finished.emit()

    def get_file_data(self):
        return self.file_data

    def get_file_type(self):
        return self.file_type

    def get_path_to_file(self):
        return self.path_to_file


class openCntFileWorkerSignals(QObject):
    finished = pyqtSignal()


class openCntFileRunnable(QRunnable):
    def __init__(self, path_to_file):
        super().__init__()
        self.signals = openCntFileWorkerSignals()

        self.path_to_file = path_to_file
        self.file_data = None
        self.file_type = None

    def run(self):
        try:
            self.file_data = cnt_file_reader.get_raw_from_cnt(self.path_to_file)
            self.file_type = "Raw"
        except TypeError:
            print("Error")
        self.signals.finished.emit()

    def get_file_data(self):
        return self.file_data

    def get_file_type(self):
        return self.file_type

    def get_path_to_file(self):
        return self.path_to_file


class openSetFileWorkerSignals(QObject):
    finished = pyqtSignal()


class openSetFileRunnable(QRunnable):
    def __init__(self, path_to_file):
        super().__init__()
        self.signals = openSetFileWorkerSignals()

        self.path_to_file = path_to_file
        self.file_data = None
        self.file_type = None

    def run(self):
        try:
            self.file_data = read_raw_eeglab(self.path_to_file, preload=True)
            self.file_type = "Raw"
        except TypeError:
            self.file_data = read_epochs_eeglab(self.path_to_file)
            self.file_type = "Epochs"
        except FileNotFoundError:
            self.file_data = None
            self.file_type = None
        self.signals.finished.emit()

    def get_file_data(self):
        return self.file_data

    def get_file_type(self):
        return self.file_type

    def get_file_path_name(self):
        return self.path_to_file


class findEventsFromChannelWorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal()


class findEventsFromChannelRunnable(QRunnable):
    def __init__(self, file_data, stim_channel):
        super().__init__()
        self.signals = findEventsFromChannelWorkerSignals()

        self.file_data = file_data
        self.stim_channel = stim_channel
        self.read_events = None

    def run(self):
        try:
            self.read_events = find_events(self.file_data, stim_channel=self.stim_channel)
            self.signals.finished.emit()
        except Exception as e:
            print(e)
            self.signals.error.emit()

    def get_read_events(self):
        return self.read_events
