#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Download fsaverage MNE Data Controller
"""

from utils.download_fsaverage_mne_data.download_fsaverage_mne_data_listener import downloadFsaverageMneDataListener
from utils.download_fsaverage_mne_data.download_fsaverage_mne_data_model import downloadFsaverageMneDataModel
from utils.download_fsaverage_mne_data.download_fsaverage_mne_data_view import downloadFsaverageMneDataView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class downloadFsaverageMneDataController(downloadFsaverageMneDataListener):
    def __init__(self):
        """
        Controller for downloading the mne sample and fsaverage datasets.
        Create a new window for asking if the download wants to be done
        """
        self.main_listener = None
        self.download_fsaverage_mne_data_model = None
        self.download_fsaverage_mne_data_view = downloadFsaverageMneDataView()
        self.download_fsaverage_mne_data_view.set_listener(self)

        self.download_fsaverage_mne_data_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.download_fsaverage_mne_data_view.close()

    def confirm_button_clicked(self):
        """
        Close the window and send the information to the main controller.
        """
        self.download_fsaverage_mne_data_view.close()
        self.main_listener.download_fsaverage_mne_data_information()

    """
    Download
    """
    def download_fsaverage_mne_data(self):
        """
        Launch the download of the fsaverage and sample datasets.
        """
        self.download_fsaverage_mne_data_model = downloadFsaverageMneDataModel()
        self.download_fsaverage_mne_data_model.set_listener(self)
        self.download_fsaverage_mne_data_model.download_fsaverage_mne_data()

    def download_fsaverage_mne_data_computation_finished(self):
        self.main_listener.download_fsaverage_mne_data_computation_finished()

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
