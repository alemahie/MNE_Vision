#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extract Epochs View
"""

from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QWidget, QPushButton, QLineEdit, QGridLayout, QLabel

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class extractEpochsView(QWidget):
    def __init__(self):
        """
        Window displaying the parameters for extracting epochs from the dataset.
        """
        super().__init__()
        self.extract_epochs_listener = None

        self.setWindowTitle("Extract Epochs")

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.tmin_line = QLineEdit("-1,0")
        self.tmin_line.setValidator(QDoubleValidator())
        self.tmax_line = QLineEdit("1,0")
        self.tmax_line.setValidator(QDoubleValidator())

        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_extract_epochs_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_extract_epochs_trigger)

        self.grid_layout.addWidget(QLabel("Epoch start (sec) : "), 0, 0)
        self.grid_layout.addWidget(self.tmin_line, 0, 1)
        self.grid_layout.addWidget(QLabel("Epoch end (sec) : "), 1, 0)
        self.grid_layout.addWidget(self.tmax_line, 1, 1)
        self.grid_layout.addWidget(self.cancel, 2, 0)
        self.grid_layout.addWidget(self.confirm, 2, 1)

    """
    Triggers
    """
    def cancel_extract_epochs_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.extract_epochs_listener.cancel_button_clicked()

    def confirm_extract_epochs_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        tmin = None
        tmax = None
        if self.tmin_line.hasAcceptableInput():
            tmin = self.tmin_line.text()
            tmin = float(tmin.replace(',', '.'))
        if self.tmin_line.hasAcceptableInput():
            tmax = self.tmax_line.text()
            tmax = float(tmax.replace(',', '.'))
        self.extract_epochs_listener.confirm_button_clicked(tmin, tmax)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: extractEpochsController
        """
        self.extract_epochs_listener = listener
