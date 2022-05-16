#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filter view
"""

from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QGridLayout, QLabel

from utils.elements_selector.elements_selector_controller import multipleSelectorController

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class filterView(QWidget):
    def __init__(self, all_channels_names):
        """
        Window displaying the parameters for computing the filtering on the dataset.
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        """
        super().__init__()
        self.filter_listener = None
        self.all_channels_names = all_channels_names
        self.channels_selector_controller = None
        self.channels_selected = None

        self.setWindowTitle("Filtering")

        self.low_frequency_line = QLineEdit("0,1")
        self.low_frequency_line.setValidator(QDoubleValidator())
        self.high_frequency_line = QLineEdit("45,0")
        self.high_frequency_line.setValidator(QDoubleValidator())

        self.channels_selection_button = QPushButton("&Channels ...", self)
        self.channels_selection_button.clicked.connect(self.channels_selection_trigger)

        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_filtering_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_filtering_trigger)

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.create_grid_layout()

    def create_grid_layout(self):
        """
        Add the widgets on the grid layout.
        """
        info_labels = ["Low Frequency (Hz) : ", "High Frequency (Hz) : ", "Channels : "]
        for i, label in enumerate(info_labels):
            self.grid_layout.addWidget(QLabel(label), i, 0)
        self.grid_layout.addWidget(self.low_frequency_line, 0, 1)
        self.grid_layout.addWidget(self.high_frequency_line, 1, 1)
        self.grid_layout.addWidget(self.channels_selection_button, 2, 1)
        self.grid_layout.addWidget(self.cancel, 3, 0)
        self.grid_layout.addWidget(self.confirm, 3, 1)

    """
    Triggers
    """
    def cancel_filtering_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.filter_listener.cancel_button_clicked()

    def confirm_filtering_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        low_frequency = None
        high_frequency = None
        if self.low_frequency_line.hasAcceptableInput():
            low_frequency = self.low_frequency_line.text()
            low_frequency = float(low_frequency.replace(',', '.'))
        if self.high_frequency_line.hasAcceptableInput():
            high_frequency = self.high_frequency_line.text()
            high_frequency = float(high_frequency.replace(',', '.'))
        self.filter_listener.confirm_button_clicked(low_frequency, high_frequency, self.channels_selected)

    def channels_selection_trigger(self):
        """
        Open the multiple selector window.
        The user can select multiple channels.
        """
        title = "Select the channels used for the filtering :"
        self.channels_selector_controller = multipleSelectorController(self.all_channels_names, title, box_checked=True)
        self.channels_selector_controller.set_listener(self.filter_listener)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: filterController
        """
        self.filter_listener = listener

    def set_channels_selected(self, channels_selected):
        """
        Set the channels selected in the multiple selector window.
        :param channels_selected: Channels selected.
        :type channels_selected: list of str
        """
        self.channels_selected = channels_selected
