#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source Space Connectivity View
"""

import numpy as np

from multiprocessing import cpu_count

from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QButtonGroup, QCheckBox, \
    QSlider, QGridLayout, QSpinBox
from PyQt6.QtCore import Qt

from mne.viz import circular_layout
from mne_connectivity.viz import plot_connectivity_circle

from utils.file_path_search import get_labels_from_subject, get_project_freesurfer_path

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sourceSpaceConnectivityView(QWidget):
    def __init__(self, number_of_channels):
        super().__init__()
        self.source_space_connectivity_listener = None

        self.number_of_channels = number_of_channels
        self.number_strongest_connections = None

        self.setWindowTitle("Source Space Connectivity")

        self.global_layout = QVBoxLayout()
        self.setLayout(self.global_layout)

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

        self.method_widget = QWidget()
        self.method_layout = QHBoxLayout()
        self.method_box = QComboBox()
        self.method_box.addItems(["MNE", "dSPM", "sLORETA", "eLORETA"])
        self.method_layout.addWidget(QLabel("Source estimation method : "))
        self.method_layout.addWidget(self.method_box)
        self.method_widget.setLayout(self.method_layout)

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

        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_source_space_connectivity_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_source_space_connectivity_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.global_layout.addWidget(self.lines_widget)
        self.global_layout.addWidget(self.method_widget)
        self.global_layout.addWidget(self.save_load_widget)
        self.global_layout.addWidget(self.n_jobs_widget)
        self.global_layout.addWidget(self.cancel_confirm_widget)

    """
    Plots
    """
    def plot_source_space_connectivity(self, source_space_connectivity_data):
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
                                 node_angles=node_angles, node_colors=label_colors)

    """
    Triggers
    """
    def cancel_source_space_connectivity_trigger(self):
        self.source_space_connectivity_listener.cancel_button_clicked()

    def confirm_source_space_connectivity_trigger(self):
        if self.all_connections_check_box.isChecked():
            self.number_strongest_connections = self.number_of_channels * self.number_of_channels
        else:
            self.number_strongest_connections = int(self.number_strongest_connections_line.text())
        source_estimation_method = self.method_box.currentText()
        save_data, load_data = self.get_save_load_button_checked()
        n_jobs = self.n_jobs_slider.value()
        self.source_space_connectivity_listener.confirm_button_clicked(source_estimation_method, save_data, load_data, n_jobs)

    def slider_value_changed_trigger(self):
        slider_value = self.n_jobs_slider.value()
        self.n_jobs_label.setText(str(slider_value))

    """
    Setters
    """
    def set_listener(self, listener):
        self.source_space_connectivity_listener = listener

    """
    Getters
    """
    def get_save_load_button_checked(self):
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
