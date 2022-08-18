#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Time frequency (ERSP/ITC) view
"""

from mne.viz import tight_layout

from matplotlib import pyplot as plt

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QComboBox, QLabel, QLineEdit

from utils.elements_selector.elements_selector_controller import multipleSelectorController
from utils.view.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class timeFrequencyErspItcView(QWidget):
    def __init__(self, all_channels_names, no_channels=False):
        """
        Window displaying the parameters for computing the ERPs on the dataset.
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        :param no_channels: Check if the channel selection must be done. Not necessary for the study plot.
        :type no_channels: bool
        """
        super().__init__()
        self.time_frequency_ersp_itc_listener = None

        self.all_channels_names = all_channels_names
        self.no_channels = no_channels

        self.channels_selector_controller = None
        self.channel_selected = None
        self.channels_selection_opened = False

        self.setWindowTitle("Time Frequency Analysis")

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        if not no_channels:
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

        if not no_channels:
            self.grid_layout.addWidget(QLabel("Channels : "), 0, 0)
            self.grid_layout.addWidget(self.channels_selection_button, 0, 1)
        self.grid_layout.addWidget(QLabel("Method for Time-frequency computation : "), 1, 0)
        self.grid_layout.addWidget(self.method_box, 1, 1)
        self.grid_layout.addWidget(QLabel("Minimum Frequency of interest (Hz) : "), 2, 0)
        self.grid_layout.addWidget(self.low_frequency_line, 2, 1)
        self.grid_layout.addWidget(QLabel("Maximum Frequency of interest (Hz) : "), 3, 0)
        self.grid_layout.addWidget(self.high_frequency_line, 3, 1)
        self.grid_layout.addWidget(QLabel("Number of cycles : "), 4, 0)
        self.grid_layout.addWidget(self.n_cycles_line, 4, 1)
        self.grid_layout.addWidget(self.cancel, 5, 0)
        self.grid_layout.addWidget(self.confirm, 5, 1)

    @staticmethod
    def plot_ersp_itc(channel_selected, power, itc):
        """
        Plot the time-frequency analysis.
        :param channel_selected: The channel selected for the time-frequency analysis.
        :type channel_selected: str
        :param power: "power" data of the time-frequency analysis computation.
        :type power: MNE.AverageTFR
        :param itc: "itc" data of the time-frequency analysis computation.
        :type itc: MNE.AverageTFR
        """
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
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.time_frequency_ersp_itc_listener.cancel_button_clicked()

    def confirm_time_frequency_ersp_itc_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        if self.channels_selection_opened or self.no_channels:      # Menu channel must have been opened if it exists.
            if not self.no_channels:
                channel_selected = self.channel_selected
            else:
                channel_selected = None
            method_tfr = self.method_box.currentText()
            min_frequency = self.low_frequency_line.text()
            min_frequency = float(min_frequency.replace(',', '.'))
            max_frequency = self.high_frequency_line.text()
            max_frequency = float(max_frequency.replace(',', '.'))
            n_cycles = self.n_cycles_line.text()
            n_cycles = float(n_cycles.replace(',', '.'))

            if not self.no_channels:
                self.time_frequency_ersp_itc_listener.confirm_button_clicked(method_tfr, channel_selected, min_frequency,
                                                                             max_frequency, n_cycles)
            else:
                self.time_frequency_ersp_itc_listener.confirm_button_clicked_from_study(method_tfr, min_frequency,
                                                                                        max_frequency, n_cycles)
        else:
            error_message = "Please select a channel in the 'channel selection' menu before starting the computation."
            error_window = errorWindow(error_message)
            error_window.show()

    def channels_selection_trigger(self):
        """
        Open the multiple selector window.
        The user can select a single channel.
        """
        title = "Select the channel used for the Time-frequency computation :"
        self.channels_selector_controller = multipleSelectorController(self.all_channels_names, title,
                                                                       box_checked=False, unique_box=True)
        self.channels_selector_controller.set_listener(self.time_frequency_ersp_itc_listener)
        self.channels_selection_opened = True

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: timeFrequencyErspItcController
        """
        self.time_frequency_ersp_itc_listener = listener

    def set_channels_selected(self, channel_selected):
        """
        Set the channel selected in the multiple selector window.
        :param channel_selected: The channel selected.
        :type channel_selected: str
        """
        self.channel_selected = channel_selected
