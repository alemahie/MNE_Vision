#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Resampling view
"""

from PyQt6.QtWidgets import QWidget, QGridLayout, QSpinBox, QPushButton, QLabel

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class resamplingView(QWidget):
    def __init__(self, frequency):
        super().__init__()
        self.resampling_listener = None

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.spinbox_value = QSpinBox()
        self.spinbox_value.setMinimum(1)
        self.spinbox_value.setMaximum(16384)
        self.spinbox_value.setValue(frequency)
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_filtering_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_filtering_trigger)

        self.grid_layout.addWidget(QLabel("Frequency (Hz) : "), 0, 0)
        self.grid_layout.addWidget(self.spinbox_value, 0, 1)
        self.grid_layout.addWidget(self.cancel, 1, 0)
        self.grid_layout.addWidget(self.confirm, 1, 1)

    """
    Triggers
    """
    def cancel_filtering_trigger(self):
        self.resampling_listener.cancel_button_clicked()

    def confirm_filtering_trigger(self):
        frequency = self.spinbox_value.value()
        self.resampling_listener.confirm_button_clicked(frequency)

    """
    Setters
    """
    def set_listener(self, listener):
        self.resampling_listener = listener
