#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dataset info view
"""

from PyQt6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtGui import QIntValidator

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class datasetInfoView(QWidget):
    def __init__(self, sampling_rate, number_of_frames, start_time):
        """
        Window displaying the dataset's information.
        :param sampling_rate: The sampling rate
        :type sampling_rate: float
        :param number_of_frames: The number of frames
        :type number_of_frames: int
        :param start_time: The start time of an epoch or the raw file.
        :type start_time: float
        """
        super().__init__()
        self.dataset_info_listener = None

        self.setWindowTitle("Dataset Information")

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.only_int = QIntValidator()
        self.sampling_rate = QLineEdit()
        self.sampling_rate.setValidator(self.only_int)
        self.sampling_rate.setText(str(sampling_rate))
        self.time_points_epochs = QLineEdit()
        self.time_points_epochs.setValidator(self.only_int)
        self.time_points_epochs.setText(str(number_of_frames))
        self.start_time = QLineEdit()
        self.start_time.setValidator(self.only_int)
        self.start_time.setText(str(start_time))

        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_dataset_info_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_dataset_info_trigger)

        self.grid_layout.addWidget(QLabel("Data sampling rate (Hz) : "), 0, 0)
        self.grid_layout.addWidget(self.sampling_rate, 0, 1)
        self.grid_layout.addWidget(QLabel("Time points per epochs (0 = Continuous) : "), 1, 0)
        self.grid_layout.addWidget(self.time_points_epochs, 1, 1)
        self.grid_layout.addWidget(QLabel("Start time (sec) (only for data epochs) : "), 2, 0)
        self.grid_layout.addWidget(self.start_time, 2, 1)
        self.grid_layout.addWidget(self.cancel, 3, 0)
        self.grid_layout.addWidget(self.confirm, 3, 1)

    """
    Triggers
    """
    def cancel_dataset_info_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.dataset_info_listener.cancel_button_clicked()

    def confirm_dataset_info_trigger(self):
        """
        Retrieve the channel name and location and send the information to the controller.
        """
        self.dataset_info_listener.confirm_button_clicked()

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: datasetInfoController
        """
        self.dataset_info_listener = listener
