#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Envelope Correlation view
"""

import matplotlib.pyplot as plt

from multiprocessing import cpu_count
from copy import deepcopy

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QGridLayout, QCheckBox, \
    QLineEdit, QComboBox, QSlider, QScrollArea
from PyQt5.QtCore import Qt

from mne.viz import plot_topomap, iter_topography
from mne_connectivity.viz import plot_connectivity_circle

from utils.view.plot_connectivity_circle_arrows import plot_connectivity_circle_arrows
from utils.view.separator import create_layout_separator

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class envelopeCorrelationView(QWidget):
    def __init__(self, number_of_channels, file_data):
        """
        Window displaying the parameters for computing the connectivity.
        :param number_of_channels: The number of channels.
        :type number_of_channels: int
        :param file_data: The dataset data
        :type file_data: MNE.Info
        """
        super().__init__()
        self.envelope_correlation_listener = None
        self.number_strongest_connections = None
        self.mode = None

        self.number_of_channels = number_of_channels
        self.file_data = deepcopy(file_data)

        self.psi_arrows = False
        self.psi_values_plot = False
        self.psi_topographies = False

        self.psi_values_window = None
        self.psi_data_picks = None

        self.setWindowTitle("Envelope Correlation")
        self.vertical_layout = QVBoxLayout()

        # Connectivity method
        self.connectivity_method_widget = QWidget()
        self.connectivity_method_layout = QHBoxLayout()
        self.connectivity_method_box = QComboBox()
        self.connectivity_method_box.addItems(["envelope_correlation", "coh", "cohy", "imcoh", "plv", "ciplv", "ppc",
                                               "pli", "wpli", "wpli2_debiased"])
        self.connectivity_method_layout.addWidget(QLabel("Connectivity measure method : "))
        self.connectivity_method_layout.addWidget(self.connectivity_method_box)
        self.connectivity_method_widget.setLayout(self.connectivity_method_layout)

        # Lines
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

        # Directionality
        self.directionality_widget = QWidget()
        self.directionality_layout = QGridLayout()
        self.psi_check_box = QCheckBox()
        self.psi_arrows_check_box = QCheckBox()
        self.psi_values_plot_check_box = QCheckBox()
        self.psi_topographies_check_box = QCheckBox()
        self.directionality_layout.addWidget(QLabel("Compute the Phase Slope Index (directionality) : "), 0, 0)
        self.directionality_layout.addWidget(self.psi_check_box, 0, 1)
        self.directionality_layout.addWidget(QLabel("Plot directionality on top of the connectivity (with arrows) : "), 1, 0)
        self.directionality_layout.addWidget(self.psi_arrows_check_box, 1, 1)
        self.directionality_layout.addWidget(QLabel("Plot all directionality values : "), 2, 0)
        self.directionality_layout.addWidget(self.psi_values_plot_check_box, 2, 1)
        self.directionality_layout.addWidget(QLabel("Plot directionality topographies : "), 3, 0)
        self.directionality_layout.addWidget(self.psi_topographies_check_box, 3, 1)
        self.directionality_widget.setLayout(self.directionality_layout)

        # Frequencies
        self.frequency_lines_widget = QWidget()
        self.frequency_lines_layout = QGridLayout()
        self.minimum_frequency_line = QLineEdit("2,0")
        self.minimum_frequency_line.setValidator(QDoubleValidator())
        self.maximum_frequency_line = QLineEdit("25,0")
        self.maximum_frequency_line.setValidator(QDoubleValidator())
        self.frequency_lines_layout.addWidget(QLabel("Minimum frequency of interest (Hz) : "), 0, 0)
        self.frequency_lines_layout.addWidget(self.minimum_frequency_line, 0, 1)
        self.frequency_lines_layout.addWidget(QLabel("Maximum frequency of interest (Hz) : "), 1, 0)
        self.frequency_lines_layout.addWidget(self.maximum_frequency_line, 1, 1)
        self.frequency_lines_widget.setLayout(self.frequency_lines_layout)

        # Number jobs slider
        self.n_jobs_widget = QWidget()
        self.n_jobs_layout = QHBoxLayout()
        self.n_jobs_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.n_jobs_slider.setMinimum(1)
        self.n_jobs_slider.setMaximum(cpu_count())
        self.n_jobs_slider.setValue(1)
        self.n_jobs_slider.setSingleStep(1)
        self.n_jobs_slider.valueChanged.connect(self.slider_value_changed_trigger)
        self.n_jobs_label = QLabel("1")
        self.n_jobs_layout.addWidget(QLabel("Number of threads : "))
        self.n_jobs_layout.addWidget(self.n_jobs_slider)
        self.n_jobs_layout.addWidget(self.n_jobs_label)
        self.n_jobs_widget.setLayout(self.n_jobs_layout)

        # Exportation
        self.data_exportation_widget = QWidget()
        self.data_exportation_layout = QHBoxLayout()
        self.data_exportation_button = QPushButton("Data exportation")
        self.data_exportation_button.clicked.connect(self.data_exportation_trigger)
        self.data_exportation_layout.addWidget(self.data_exportation_button)
        self.data_exportation_widget.setLayout(self.data_exportation_layout)

        # Cancel Confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_envelope_correlation_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_envelope_correlation_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.connectivity_method_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.lines_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.directionality_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.frequency_lines_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.n_jobs_widget)
        self.vertical_layout.addWidget(self.data_exportation_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.cancel_confirm_widget)
        self.setLayout(self.vertical_layout)

    """
    Plots
    """
    def plot_envelope_correlation(self, envelope_correlation_data, psi, channel_names):
        """
        Plot the envelope correlation computed.
        :param envelope_correlation_data: The envelope correlation data to plot.
        :type envelope_correlation_data: list of, list of float
        :param psi: Values of the computation of the PSI, if None then the computation has not been done.
        The PSI give an indication to the directionality of the connectivity.
        :type psi: list of, list of float
        :param channel_names: Channels' names
        :type channel_names: list of str
        """
        if psi is None:
            plot_connectivity_circle(envelope_correlation_data, channel_names, n_lines=self.number_strongest_connections,
                                     title="Envelope Correlation")
        else:
            if self.psi_arrows:
                plot_connectivity_circle_arrows(envelope_correlation_data, channel_names, psi=psi,
                                                n_lines=self.number_strongest_connections, title="Envelope Correlation")
            else:
                plot_connectivity_circle(envelope_correlation_data, channel_names, n_lines=self.number_strongest_connections,
                                         title="Envelope Correlation")
            self.plot_psi(psi, channel_names)
            if self.psi_values_plot:
                self.plot_psi_values(psi, channel_names)
            if self.psi_topographies:
                self.plot_psi_topographies(psi, channel_names)

    @staticmethod
    def plot_psi(psi, channel_names):
        """
        Plot the Phase Slope Index computed.
        :param psi: Values of the computation of the PSI, if None then the computation has not been done.
        The PSI give an indication to the directionality of the connectivity.
        :type psi: list of, list of float
        :param channel_names: Channels' names
        :type channel_names: list of str
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.matshow(psi)
        fig.colorbar(cax)

        # PSI : Positive value means from the channel to the other (row to columns)
        # While negative means the opposite

        # Set ticks on both sides of axes on
        ax.tick_params(axis="x", bottom=True, top=False, labelbottom=True, labeltop=False)
        plt.locator_params(axis="x", nbins=len(channel_names))
        plt.locator_params(axis="y", nbins=len(channel_names))
        ax.set_xticklabels([''] + channel_names, rotation=90)
        ax.set_yticklabels([''] + channel_names)
        ax.set_xlabel("Receiver")
        ax.set_ylabel("Sender")
        ax.set_title("PSI Directionality")

        plt.show()

    def plot_psi_values(self, psi, channel_names):
        """
        Plot the values of the Phase Slope Index computed.
        :param psi: Values of the computation of the PSI, if None then the computation has not been done.
        The PSI give an indication to the directionality of the connectivity.
        :type psi: list of, list of float
        :param channel_names: Channels' names
        :type channel_names: list of str
        """
        self.psi_values_window = psiValuesWindow(psi, channel_names)
        self.psi_values_window.show()

    def plot_psi_topographies(self, psi, channel_names):
        """
        Plot the PSI values as topographies on predefined points of the headset.
        :param psi: Values of the computation of the PSI, if None then the computation has not been done.
        The PSI give an indication to the directionality of the connectivity.
        :type psi: list of, list of float
        :param channel_names: Channels' names
        :type channel_names: list of str
        """
        picks = ['Fp1', 'Fp2', 'F7', 'F3', 'Fz', 'F4', 'F8', 'T7', 'C3', 'Cz', 'C4', 'T8', 'P7', 'P3', 'Pz', 'P4', 'P8', 'O1', 'O2']
        self.file_data = self.file_data.pick(picks)
        self.psi_data_picks = self.keep_picks_PSI_data(psi, channel_names, picks)
        for ax, idx in iter_topography(self.file_data.info,
                                       fig_facecolor='white',
                                       axis_facecolor='white',
                                       axis_spinecolor='white',
                                       on_pick=self.plot_topographies_on_pick):
            plot_topomap(self.psi_data_picks[idx], self.file_data.info, show=False)
        plt.gcf().suptitle('PSI Topographies')
        plt.show()

    def plot_topographies_on_pick(self, ax, ch_idx):
        """
        This block of code is executed once you click on one of the channel axes
        in the plot. To work with the viz internals, this function should only take
        two parameters, the axis and the channel or data index.
        """
        plot_topomap(self.psi_data_picks[ch_idx], self.file_data.info, show=False)

    """
    Utils
    """
    @staticmethod
    def keep_picks_PSI_data(psi, channel_names, picks):
        """
        Keep the PSI data from the channels that are in the picks.
        :param psi: Values of the computation of the PSI, if None then the computation has not been done.
        The PSI give an indication to the directionality of the connectivity.
        :type psi: list of, list of float
        :param channel_names: Channels' names
        :type channel_names: list of str
        :param picks: The channels to keep
        :type picks: list of str
        :return: All the PSI data kept with the picks
        :rtype: list of, list of float
        """
        # First get the indexes of each channel that are picked.
        indexes_dict = {}
        for i, value in enumerate(channel_names):
            if value in picks:
                indexes_dict[value] = i
        indexes = indexes_dict.values()
        # Get the PSI data to keep.
        res = []
        for pick in picks:
            pick_res = []
            index = indexes_dict[pick]
            for i in indexes:
                if i <= index:  # Row of the psi data
                    pick_res.append(psi[index][i])
                else:  # i > index: column of the psi data
                    pick_res.append(psi[i][index])
            res.append(pick_res)
        return res

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
        psi = self.psi_check_box.isChecked()

        fmin = None
        fmax = None
        if self.minimum_frequency_line.hasAcceptableInput():
            fmin = float(self.minimum_frequency_line.text().replace(',', '.'))
        if self.maximum_frequency_line.hasAcceptableInput():
            fmax = float(self.maximum_frequency_line.text().replace(',', '.'))

        connectivity_method = self.connectivity_method_box.currentText()
        n_jobs = self.n_jobs_slider.value()

        self.psi_arrows = self.psi_arrows_check_box.isChecked()
        self.psi_values_plot = self.psi_values_plot_check_box.isChecked()
        self.psi_topographies = self.psi_topographies_check_box.isChecked()

        self.envelope_correlation_listener.confirm_button_clicked(psi, fmin, fmax, connectivity_method, n_jobs)

    def data_exportation_trigger(self):
        """
        Open a new window asking for the path for the exportation of the envelope correlation data
        """
        self.envelope_correlation_listener.additional_parameters_clicked()

    def slider_value_changed_trigger(self):
        """
        Change the value of the slider displayed on the window when the actual slider is moved.
        """
        slider_value = self.n_jobs_slider.value()
        self.n_jobs_label.setText(str(slider_value))

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


# PSI Values Window
class psiValuesWindow(QWidget):
    def __init__(self, psi, channel_names):
        """
        Plot the values of the Phase Slope Index computed.
        :param psi: Values of the computation of the PSI, if None then the computation has not been done.
        The PSI give an indication to the directionality of the connectivity.
        :type psi: list of, list of float
        :param channel_names: Channels' names
        :type channel_names: list of str
        """
        super().__init__()

        self.global_layout = QVBoxLayout()

        self.setWindowTitle("PSI Values")

        self.psi_values_widget = QWidget()
        self.psi_values_layout = QGridLayout()
        self.psi_values_layout.setSpacing(0)

        # Channel names
        for i in range(len(channel_names)):
            label_row = QLabel(channel_names[i])
            if i != 0:
                label_row.setObjectName("BoundariesGridLayoutRight")
            else:
                label_row.setObjectName("BoundariesGridLayoutLeft")
            self.psi_values_layout.addWidget(label_row, 0, i+1)
            label_col = QLabel(channel_names[i])
            if i != len(channel_names)-1:
                label_col.setObjectName("BoundariesGridLayoutLeft")
            else:
                label_col.setObjectName("BoundariesGridLayoutBottomLeft")
            self.psi_values_layout.addWidget(label_col, i+1, 0)
        # Values
        for i in range(len(psi)):
            for j in range(len(psi[i])):
                label = QLabel(str(round(psi[i][j], 3)))
                if i != len(channel_names)-1:
                    label.setObjectName("BoundariesGridLayoutRight")
                else:
                    label.setObjectName("BoundariesGridLayoutBottomRight")
                self.psi_values_layout.addWidget(label, i+1, j+1)

        self.psi_values_widget.setLayout(self.psi_values_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.psi_values_widget)

        self.global_layout.addWidget(self.scroll_area)
        self.setLayout(self.global_layout)
