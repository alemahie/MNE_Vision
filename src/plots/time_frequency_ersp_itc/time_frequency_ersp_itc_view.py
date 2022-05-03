#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Time frequency (ERSP/ITC) view
"""

from mne.viz import tight_layout

from matplotlib import pyplot as plt

from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QPushButton, QWidget, QGridLayout, QComboBox, QLabel, QLineEdit

from utils.elements_selector.elements_selector_controller import multipleSelectorController
from utils.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class timeFrequencyErspItcView(QWidget):
    def __init__(self, all_channels_names):
        super().__init__()
        self.time_frequency_ersp_itc_listener = None
        self.all_channels_names = all_channels_names
        self.channels_selector_controller = None
        self.channels_selected = None
        self.channels_selection_opened = False

        self.setWindowTitle("Time Frequency Analysis")

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.channels_selection_button = QPushButton("&Channels ...", self)
        self.channels_selection_button.clicked.connect(self.channels_selection_trigger)

        self.method_box = QComboBox()
        self.method_box.addItems(["Morlet", "Multitaper", "Stockwell"])

        self.low_frequency_line = QLineEdit("6")
        self.low_frequency_line.setValidator(QDoubleValidator())
        self.high_frequency_line = QLineEdit("35")
        self.high_frequency_line.setValidator(QDoubleValidator())
        self.n_cycles_line = QLineEdit("5.0")
        self.n_cycles_line.setValidator(QDoubleValidator())

        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_time_frequency_ersp_itc_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_time_frequency_ersp_itc_trigger)

        self.grid_layout.addWidget(QLabel("Channels : "), 0, 0)
        self.grid_layout.addWidget(self.channels_selection_button, 0, 1)
        self.grid_layout.addWidget(QLabel("Method for Time-frequency computation : "), 1, 0)
        self.grid_layout.addWidget(self.method_box, 1, 1)
        self.grid_layout.addWidget(QLabel("Low Frequency (Hz) : "), 2, 0)
        self.grid_layout.addWidget(self.low_frequency_line, 2, 1)
        self.grid_layout.addWidget(QLabel("High Frequency (Hz) : "), 3, 0)
        self.grid_layout.addWidget(self.high_frequency_line, 3, 1)
        self.grid_layout.addWidget(QLabel("Number of cycles : "), 4, 0)
        self.grid_layout.addWidget(self.n_cycles_line, 4, 1)
        self.grid_layout.addWidget(self.cancel, 5, 0)
        self.grid_layout.addWidget(self.confirm, 5, 1)

    def plot_ersp_itc(self, channel_selected, power, itc):
        fig, axis = plt.subplots(1, 2)
        power.plot(axes=axis[0], show=False)
        axis[0].set_title("ERSP")
        itc.plot(axes=axis[1], show=False)
        axis[1].set_title("ITC")
        fig.suptitle(f"Channel : {channel_selected[0]}")
        tight_layout()
        plt.show()

    """
    Triggers
    """
    def cancel_time_frequency_ersp_itc_trigger(self):
        self.time_frequency_ersp_itc_listener.cancel_button_clicked()

    def confirm_time_frequency_ersp_itc_trigger(self):
        if self.channels_selection_opened:
            channel_selected = self.channels_selected
            method_tfr = self.method_box.currentText()
            min_frequency = self.low_frequency_line.text()
            min_frequency = float(min_frequency.replace(',', '.'))
            max_frequency = self.high_frequency_line.text()
            max_frequency = float(max_frequency.replace(',', '.'))
            n_cycles = self.n_cycles_line.text()
            n_cycles = float(n_cycles.replace(',', '.'))
            self.time_frequency_ersp_itc_listener.confirm_button_clicked(method_tfr, channel_selected, min_frequency,
                                                                         max_frequency, n_cycles)
        else:
            error_message = "Please select a channel in the 'channel selection' menu before starting the computation."
            error_window = errorWindow(error_message)
            error_window.show()

    def channels_selection_trigger(self):
        title = "Select the channel used for the Time-frequency computation :"
        self.channels_selector_controller = multipleSelectorController(self.all_channels_names, title,
                                                                       box_checked=False, unique_box=True)
        self.channels_selector_controller.set_listener(self.time_frequency_ersp_itc_listener)
        self.channels_selection_opened = True

    """
    Setters
    """
    def set_listener(self, listener):
        self.time_frequency_ersp_itc_listener = listener

    def set_channels_selected(self, channels_selected):
        self.channels_selected = channels_selected
