#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filter view
"""

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QGridLayout, QLabel, QHBoxLayout, QVBoxLayout, QComboBox

from utils.elements_selector.elements_selector_controller import multipleSelectorController
from utils.view.separator import create_layout_separator

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

        self.global_layout = QVBoxLayout()

        # Channels
        self.method_channels_widget = QWidget()
        self.method_channels_layout = QGridLayout()
        self.method_box = QComboBox()
        self.method_box.addItems(["fir", "iir"])
        self.channels_selection_button = QPushButton("&Channels ...", self)
        self.channels_selection_button.clicked.connect(self.channels_selection_trigger)
        self.method_channels_layout.addWidget(QLabel("Filtering method :"), 0, 0)
        self.method_channels_layout.addWidget(self.method_box, 0, 1)
        self.method_channels_layout.addWidget(QLabel("Channels :"), 1, 0)
        self.method_channels_layout.addWidget(self.channels_selection_button, 1, 1)
        self.method_channels_widget.setLayout(self.method_channels_layout)

        # Lines
        self.lines_widget = QWidget()
        self.lines_layout = QGridLayout()
        self.low_frequency_line = QLineEdit("0,1")
        self.low_frequency_line.setValidator(QDoubleValidator())
        self.high_frequency_line = QLineEdit("45,0")
        self.high_frequency_line.setValidator(QDoubleValidator())
        self.lines_layout.addWidget(QLabel("Low Frequency (Hz) : "), 0, 0)
        self.lines_layout.addWidget(self.low_frequency_line, 0, 1)
        self.lines_layout.addWidget(QLabel("High Frequency (Hz) : "), 1, 0)
        self.lines_layout.addWidget(self.high_frequency_line, 1, 1)
        self.lines_widget.setLayout(self.lines_layout)

        # Cancel Confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_filtering_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_filtering_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        # Layout
        self.global_layout.addWidget(self.method_channels_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.lines_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.cancel_confirm_widget)
        self.setLayout(self.global_layout)

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
        filter_method = self.method_box.currentText()
        low_frequency = None
        high_frequency = None
        if self.low_frequency_line.hasAcceptableInput():
            low_frequency = self.low_frequency_line.text()
            low_frequency = float(low_frequency.replace(',', '.'))
        if self.high_frequency_line.hasAcceptableInput():
            high_frequency = self.high_frequency_line.text()
            high_frequency = float(high_frequency.replace(',', '.'))
        self.filter_listener.confirm_button_clicked(low_frequency, high_frequency, self.channels_selected, filter_method)

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
