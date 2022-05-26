#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Envelope Correlation view
"""

from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QGridLayout, QCheckBox

from mne_connectivity.viz import plot_connectivity_circle

import matplotlib.pyplot as plt

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class envelopeCorrelationView(QWidget):
    def __init__(self, number_of_channels):
        """
        Window displaying the parameters for finding events from a stimulation channel.
        :param number_of_channels: The number of channels.
        :type number_of_channels: int
        """
        super().__init__()
        self.envelope_correlation_listener = None
        self.number_strongest_connections = None
        self.mode = None
        self.number_of_channels = number_of_channels

        self.setWindowTitle("Envelope Correlation")

        self.vertical_layout = QVBoxLayout()

        self.lines_widget = QWidget()
        self.lines_layout = QGridLayout()
        self.number_strongest_connections_line = QSpinBox()
        self.number_strongest_connections_line.setMinimum(10)
        self.number_strongest_connections_line.setMaximum(number_of_channels*number_of_channels)
        self.number_strongest_connections_line.setValue(100)
        self.all_connections_check_box = QCheckBox()
        self.lines_layout.addWidget(QLabel("Number of strongest connections plotted : "), 0, 0)
        self.lines_layout.addWidget(self.number_strongest_connections_line, 0, 1)
        self.lines_layout.addWidget(QLabel("Plot all connections : "), 1, 0)
        self.lines_layout.addWidget(self.all_connections_check_box, 1, 1)
        self.lines_widget.setLayout(self.lines_layout)

        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_envelope_correlation_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_envelope_correlation_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.lines_widget)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)
        self.setLayout(self.vertical_layout)

    def plot_envelope_correlation(self, envelope_correlation_data, channel_names):
        """
        Plot the envelope correlation computed.
        :param envelope_correlation_data: The envelope correlation data to plot.
        :type envelope_correlation_data: list of, list of float
        :param channel_names: Channels' names
        :type channel_names: list of str
        """
        plot_connectivity_circle(envelope_correlation_data, channel_names, n_lines=self.number_strongest_connections,
                                 title="Envelope Correlation")

        """
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.matshow(envelope_correlation_data)
        fig.colorbar(cax)

        # PSI : Positive value means from the channel to the other (row to columns)
        # While negative means the opposite

        # Set ticks on both sides of axes on
        ax.tick_params(axis="x", bottom=True, top=False, labelbottom=True, labeltop=False)
        plt.locator_params(axis="x", nbins=len(channel_names))
        plt.locator_params(axis="y", nbins=len(channel_names))
        ax.set_xticklabels([''] + channel_names, rotation=90)
        ax.set_yticklabels([''] + channel_names)

        plt.show()
        """

    """
    Triggers
    """
    def cancel_envelope_correlation_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.envelope_correlation_listener.cancel_button_clicked()

    def confirm_envelope_correlation_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        if self.all_connections_check_box.isChecked():
            self.number_strongest_connections = self.number_of_channels * self.number_of_channels
        else:
            self.number_strongest_connections = int(self.number_strongest_connections_line.text())
        self.envelope_correlation_listener.confirm_button_clicked()

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: envelopeCorrelationController
        """
        self.envelope_correlation_listener = listener
