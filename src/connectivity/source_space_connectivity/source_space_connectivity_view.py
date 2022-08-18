#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source Space Connectivity View
"""

import numpy as np

from multiprocessing import cpu_count

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QButtonGroup, QCheckBox, \
    QSlider, QGridLayout, QSpinBox, QLineEdit
from PyQt5.QtCore import Qt
from matplotlib import pyplot as plt

from mne.viz import circular_layout
from mne_connectivity.viz import plot_connectivity_circle

from utils.file_path_search import get_labels_from_subject, get_project_freesurfer_path
from utils.view.separator import create_layout_separator

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sourceSpaceConnectivityView(QWidget):
    def __init__(self, number_of_channels):
        """
        Window displaying the parameters for the computation of the source space connectivity on the dataset.
        :param number_of_channels: The number of channels.
        :type number_of_channels: int
        """
        super().__init__()
        self.source_space_connectivity_listener = None

        self.number_of_channels = number_of_channels
        self.number_strongest_connections = None

        self.setWindowTitle("Source Space Connectivity")

        self.global_layout = QVBoxLayout()
        self.setLayout(self.global_layout)

        # Connectivity method
        self.connectivity_method_widget = QWidget()
        self.connectivity_method_layout = QHBoxLayout()
        self.connectivity_method_box = QComboBox()
        self.connectivity_method_box.addItems(["coh", "cohy", "imcoh", "plv", "ciplv", "ppc", "pli", "wpli", "wpli2_debiased"])
        self.connectivity_method_layout.addWidget(QLabel("Connectivity measure method : "))
        self.connectivity_method_layout.addWidget(self.connectivity_method_box)
        self.connectivity_method_widget.setLayout(self.connectivity_method_layout)

        # Spectrum method
        self.spectrum_estimation_method_widget = QWidget()
        self.spectrum_estimation_method_layout = QHBoxLayout()
        self.spectrum_estimation_method_box = QComboBox()
        self.spectrum_estimation_method_box.addItems(["multitaper", "fourier", "cwt_morlet"])
        self.spectrum_estimation_method_layout.addWidget(QLabel("Spectrum estimation method : "))
        self.spectrum_estimation_method_layout.addWidget(self.spectrum_estimation_method_box)
        self.spectrum_estimation_method_widget.setLayout(self.spectrum_estimation_method_layout)

        # Method
        self.method_widget = QWidget()
        self.method_layout = QHBoxLayout()
        self.method_box = QComboBox()
        self.method_box.addItems(["MNE", "dSPM", "sLORETA", "eLORETA"])
        self.method_layout.addWidget(QLabel("Source space computation method : "))
        self.method_layout.addWidget(self.method_box)
        self.method_widget.setLayout(self.method_layout)

        # Save load
        self.save_load_widget = QWidget()
        self.check_box_layout = QVBoxLayout()
        self.save_load_buttons = QButtonGroup()
        self.check_box_compute_from_scratch = QCheckBox()
        self.check_box_compute_from_scratch.setText("Compute source space from scratch and don't save")
        self.check_box_compute_from_scratch.setChecked(True)
        self.save_load_buttons.addButton(self.check_box_compute_from_scratch, 0)  # Button with ID 0
        self.check_box_save = QCheckBox()
        self.check_box_save.setText("Save source space files")
        self.save_load_buttons.addButton(self.check_box_save, 1)  # Button with ID 1
        self.check_box_load = QCheckBox()
        self.check_box_load.setText("Load source space files")
        self.save_load_buttons.addButton(self.check_box_load, 2)  # Button with ID 2
        self.check_box_layout.addWidget(self.check_box_compute_from_scratch)
        self.check_box_layout.addWidget(self.check_box_save)
        self.check_box_layout.addWidget(self.check_box_load)
        self.save_load_widget.setLayout(self.check_box_layout)

        # Plot parameters
        self.lines_widget = QWidget()
        self.lines_layout = QGridLayout()
        self.number_strongest_connections_line = QSpinBox()
        self.number_strongest_connections_line.setMinimum(10)
        self.number_strongest_connections_line.setMaximum(number_of_channels*number_of_channels)
        self.number_strongest_connections_line.setValue(100)
        self.all_connections_check_box = QCheckBox()
        self.psi_check_box = QCheckBox()
        self.lines_layout.addWidget(QLabel("Number of strongest connections plotted : "), 0, 0)
        self.lines_layout.addWidget(self.number_strongest_connections_line, 0, 1)
        self.lines_layout.addWidget(QLabel("Plot all connections : "), 1, 0)
        self.lines_layout.addWidget(self.all_connections_check_box, 1, 1)
        self.lines_layout.addWidget(QLabel("Compute the Phase Slope Index (directionality) : "), 2, 0)
        self.lines_layout.addWidget(self.psi_check_box, 2, 1)
        self.lines_widget.setLayout(self.lines_layout)

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
        self.cancel.clicked.connect(self.cancel_source_space_connectivity_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_source_space_connectivity_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.global_layout.addWidget(self.connectivity_method_widget)
        # self.global_layout.addWidget(self.spectrum_estimation_method_widget)
        self.global_layout.addWidget(self.method_widget)
        self.global_layout.addWidget(self.save_load_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.lines_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.frequency_lines_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.n_jobs_widget)
        self.global_layout.addWidget(self.data_exportation_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.cancel_confirm_widget)

    """
    Plots
    """
    def plot_source_space_connectivity(self, source_space_connectivity_data, psi):
        """
        Plot the source space connectivity data.
        :param source_space_connectivity_data: The source space connectivity data.
        :type source_space_connectivity_data: list of, list of float
        :param psi: Check if the computation of the Phase Slope Index must be done. The PSI give an indication to the
        directionality of the connectivity.
        :type psi: bool
        """
        try:
            labels = get_labels_from_subject("fsaverage", get_project_freesurfer_path())
            label_colors = [label.color for label in labels]
            label_names = [label.name for label in labels]
            lh_labels = [name for name in label_names if name.endswith('lh')]

            label_ypos = list()     # Get the y-location of the label
            for name in lh_labels:
                idx = label_names.index(name)
                ypos = np.mean(labels[idx].pos[:, 1])
                label_ypos.append(ypos)

            # Reorder the labels based on their location
            lh_labels = [label for (yp, label) in sorted(zip(label_ypos, lh_labels))]
            rh_labels = [label[:-2] + 'rh' for label in lh_labels]  # For the right hemi

            node_order = list()     # Save the plot order and create a circular layout
            node_order.extend(lh_labels[::-1])  # reverse the order
            node_order.extend(rh_labels)
            node_angles = circular_layout(label_names, node_order, start_pos=90,
                                          group_boundaries=[0, len(label_names) / 2])

            plot_connectivity_circle(source_space_connectivity_data, label_names, n_lines=self.number_strongest_connections,
                                     node_angles=node_angles, node_colors=label_colors, title="Source Space Connectivity")

            if psi is not None:
                self.plot_psi(psi, label_names)
                # plot_connectivity_circle(psi, label_names, n_lines=self.number_strongest_connections, node_angles=node_angles,
                #                          node_colors=label_colors, title="PSI Directionality")
        except Exception as e:
            print(e)

    @staticmethod
    def plot_psi(psi, label_names):
        """
        Plot the Phase Slope Index computed.
        :param psi: Check if the computation of the Phase Slope Index must be done. The PSI give an indication to the
        directionality of the connectivity.
        :type psi: bool
        :param label_names: Labels' names
        :type label_names: list of str
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cax = ax.matshow(psi)
        fig.colorbar(cax)

        # PSI : Positive value means from the channel to the other (row to columns)
        # While negative means the opposite

        # Set ticks on both sides of axes on
        ax.tick_params(axis="x", bottom=True, top=False, labelbottom=True, labeltop=False)
        plt.locator_params(axis="x", nbins=len(label_names))
        plt.locator_params(axis="y", nbins=len(label_names))
        ax.set_xticklabels([''] + label_names, rotation=90)
        ax.set_yticklabels([''] + label_names)
        ax.set_xlabel("Receiver")
        ax.set_ylabel("Sender")
        ax.set_title("PSI Directionality")

        plt.show()

    """
    Triggers
    """
    def cancel_source_space_connectivity_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.source_space_connectivity_listener.cancel_button_clicked()

    def confirm_source_space_connectivity_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        connectivity_method = self.connectivity_method_box.currentText()
        spectrum_estimation_method = self.spectrum_estimation_method_box.currentText()
        if self.all_connections_check_box.isChecked():
            self.number_strongest_connections = self.number_of_channels * self.number_of_channels
        else:
            self.number_strongest_connections = int(self.number_strongest_connections_line.text())
        source_estimation_method = self.method_box.currentText()
        save_data, load_data = self.get_save_load_button_checked()
        n_jobs = self.n_jobs_slider.value()
        psi = self.psi_check_box.isChecked()

        fmin = None
        fmax = None
        if self.minimum_frequency_line.hasAcceptableInput():
            fmin = float(self.minimum_frequency_line.text().replace(',', '.'))
        if self.maximum_frequency_line.hasAcceptableInput():
            fmax = float(self.maximum_frequency_line.text().replace(',', '.'))

        self.source_space_connectivity_listener.confirm_button_clicked(connectivity_method, spectrum_estimation_method,
                                                                       source_estimation_method, save_data, load_data,
                                                                       n_jobs, psi, fmin, fmax)

    def data_exportation_trigger(self):
        """
        Open a new window asking for the path for the exportation of the source space connectivity data
        """
        self.source_space_connectivity_listener.additional_parameters_clicked()

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
        :type listener: sourceSpaceConnectivityController
        """
        self.source_space_connectivity_listener = listener

    """
    Getters
    """
    def get_save_load_button_checked(self):
        """
        Get the values of the save and load buttons.
        :return: save_data: True if the data must be saved. Otherwise, False.
        load_data: True if the data must be loaded. Otherwise, False.
        :rtype: boolean, boolean
        """
        checked_button = self.save_load_buttons.checkedButton()
        button_id = self.save_load_buttons.id(checked_button)
        save_data = None
        load_data = None
        if button_id == 0:
            save_data = False
            load_data = False
        elif button_id == 1:
            save_data = True
            load_data = False
        elif button_id == 2:
            save_data = False
            load_data = True
        return save_data, load_data
