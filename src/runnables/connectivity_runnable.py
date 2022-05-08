#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Files runnable
"""

from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

from mne import read_epochs
from mne.io import read_raw_fif, read_raw_eeglab, read_epochs_eeglab

from utils import cnt_file_reader

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class connectivityWorkerSignals(QObject):
    finished = pyqtSignal()


class connectivityRunnable(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = connectivityWorkerSignals()

    def run(self):
        print("Run")
        self.signals.finished.emit()
