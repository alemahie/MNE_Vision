#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Download fsaverage MNE Data Model
"""

from PyQt5.QtCore import QThreadPool

from runnables.utils_runnable import downloadFsaverageMneDataRunnable

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class downloadFsaverageMneDataModel:
    def __init__(self):
        """
        Model for downloading the mne sample and fsaverage datasets.
        Creates the parallel runnable for the download
        """
        self.main_listener = None
        self.download_fsaverage_mne_data_runnable = None

    def download_fsaverage_mne_data(self):
        """
        Creates the parallel runnable for computing the envelope correlation between the channels of the dataset.
        """
        pool = QThreadPool.globalInstance()
        self.download_fsaverage_mne_data_runnable = downloadFsaverageMneDataRunnable()
        pool.start(self.download_fsaverage_mne_data_runnable)
        self.download_fsaverage_mne_data_runnable.signals.finished.connect(self.download_fsaverage_mne_data_computation_finished)

    def download_fsaverage_mne_data_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.main_listener.download_fsaverage_mne_data_computation_finished()

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the main listener so that the controller is able to communicate with the main controller.
        :param listener: main listener
        :type listener: downloadFsaverageMneDataController
        """
        self.main_listener = listener
