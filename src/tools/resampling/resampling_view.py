#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Resampling view
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QSpinBox, QPushButton, QLabel

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class resamplingView(QWidget):
    def __init__(self, frequency):
        """
         Window displaying the parameters for computing the resampling on the dataset.
        :param frequency: The frequency rate
        :type frequency: float
        """
        super().__init__()
        self.resampling_listener = None

        self.setWindowTitle("Resampling")

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.spinbox_value = QSpinBox()
        self.spinbox_value.setMinimum(1)
        self.spinbox_value.setMaximum(16384)
        self.spinbox_value.setValue(frequency)
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_resampling_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_resampling_trigger)

        self.grid_layout.addWidget(QLabel("Frequency (Hz) : "), 0, 0)
        self.grid_layout.addWidget(self.spinbox_value, 0, 1)
        self.grid_layout.addWidget(self.cancel, 1, 0)
        self.grid_layout.addWidget(self.confirm, 1, 1)

    """
    Triggers
    """
    def cancel_resampling_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.resampling_listener.cancel_button_clicked()

    def confirm_resampling_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        frequency = self.spinbox_value.value()
        self.resampling_listener.confirm_button_clicked(frequency)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: resamplingController
        """
        self.resampling_listener = listener
