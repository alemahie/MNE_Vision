#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Download fsaverage MNE Data View
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class downloadFsaverageMneDataView(QWidget):
    def __init__(self):
        """
        Window displaying and asking if the download wants to be done
        """
        super().__init__()
        self.download_fsaverage_mne_data_listener = None

        self.global_layout = QVBoxLayout()
        self.setLayout(self.global_layout)

        self.global_layout.addWidget(QLabel("Some data are needed to compute the source space, do you agree do download "
                                            "those data ?"))

        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_download_fsaverage_mne_data_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_download_fsaverage_mne_data_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.global_layout.addWidget(self.cancel_confirm_widget)


    """
    Triggers
    """
    def cancel_download_fsaverage_mne_data_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.download_fsaverage_mne_data_listener.cancel_button_clicked()

    def confirm_download_fsaverage_mne_data_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        self.download_fsaverage_mne_data_listener.confirm_button_clicked()

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: downloadFsaverageMneDataController
        """
        self.download_fsaverage_mne_data_listener = listener
