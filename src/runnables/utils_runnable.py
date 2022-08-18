#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utils runnable
"""

import os

from PyQt5.QtCore import QRunnable, pyqtSignal, QObject

from mne.datasets import fetch_fsaverage
from mne.datasets.sample import data_path

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


# Download fsaverage MNE data
class downloadFsaverageMneDataWorkerSignals(QObject):
    """
    Contain the signals used by the download fsaverage MNE data runnable.
    """
    finished = pyqtSignal()


class downloadFsaverageMneDataRunnable(QRunnable):
    def __init__(self):
        """
        Runnable for the downloading the fsaverage and sample datasets.
        """
        super().__init__()
        self.signals = downloadFsaverageMneDataWorkerSignals()

    def run(self):
        """
        Launch the computation of the filtering on the given data.
        Notifies the main model that the computation is finished.
        """
        try:
            os.mkdir(os.path.expanduser('~') + "/mne_data")
        except:
            pass
        try:
            os.mkdir(os.path.expanduser('~') + "/mne_data/MNE-fsaverage-data")
        except:
            pass
        subjects_dir = str(data_path()) + "/subjects/"
        fetch_fsaverage(subjects_dir=subjects_dir)
        self.signals.finished.emit()
