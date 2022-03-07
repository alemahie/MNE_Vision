#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Files runnable
"""

from PyQt6.QtCore import QRunnable, pyqtSignal, QObject
from mne.io import read_raw_eeglab, read_epochs_eeglab

from utils import cnt_file_reader

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class openCntFileWorkerSignals(QObject):
    finished = pyqtSignal()


class openCntFileRunnable(QRunnable):
    def __init__(self, path_to_file):
        super().__init__()
        self.signals = openCntFileWorkerSignals()

        self.path_to_file = path_to_file
        self.file_data = None

    def run(self):
        self.file_data = cnt_file_reader.get_raw_from_cnt(self.path_to_file)
        self.signals.finished.emit()

    def get_file_data(self):
        return self.file_data


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
            mne_item = read_raw_eeglab(self.path_to_file, preload=True)
            self.file_type = "Raw"
        except:
            mne_item = read_epochs_eeglab(self.path_to_file)
            self.file_type = "Epochs"
        self.file_data = mne_item
        self.signals.finished.emit()

    def get_file_data(self):
        return self.file_data

    def get_file_type(self):
        return self.file_type
