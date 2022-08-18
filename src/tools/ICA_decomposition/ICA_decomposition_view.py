#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ICA decomposition view
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QComboBox, QPushButton, QLabel

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class icaDecompositionView(QWidget):
    def __init__(self):
        """
        indow displaying the parameters for computing the ICA decomposition on the dataset.
        """
        super().__init__()
        self.ica_decomposition_listener = None

        self.setWindowTitle("ICA Decomposition")

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.method_selection = QComboBox()
        self.method_selection.addItems(["fastica", "infomax", "picard"])

        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_ica_decomposition_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_ica_decomposition_trigger)

        self.grid_layout.addWidget(QLabel("ICA decomposition method : "), 0, 0)
        self.grid_layout.addWidget(self.method_selection, 0, 1)
        self.grid_layout.addWidget(self.cancel, 1, 0)
        self.grid_layout.addWidget(self.confirm, 1, 1)

    """
    Triggers
    """
    def cancel_ica_decomposition_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.ica_decomposition_listener.cancel_button_clicked()

    def confirm_ica_decomposition_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        ica_method = self.method_selection.currentText()
        self.ica_decomposition_listener.confirm_button_clicked(ica_method)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: icaDecompositionController
        """
        self.ica_decomposition_listener = listener
