#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main view
"""

from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QFileDialog

from mne.viz import plot_sensors

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class mainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.info_labels = ["Filename : ", "File Type : ", "Number of Channels : ", "Sampling Frequency (Hz) : ",
                            "Number of Events : ", "Number of Epochs : ", "Epoch start (sec) : ", "Epoch end (sec) : ",
                            "Number of Frames/Frames per Epoch : ", "Reference : ", "Channel Locations : ",
                            "ICA : ", "Dataset Size (Mb) : "]

        self.central_widget = QWidget()

        self.grid_layout = QGridLayout(self)
        self.central_widget.setLayout(self.grid_layout)

        for i, info in enumerate(self.info_labels):
            self.grid_layout.addWidget(QLabel(info), i, 0)
        for i in range(13):
            self.grid_layout.addWidget(QLabel("/"), i, 1)

        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("MNE Vision")

    def display_info(self, all_info):
        for i in range(13):
            label_item = self.grid_layout.itemAtPosition(i, 1).widget()
            label_item.setText(str(all_info[i]))

    """
    Plot
    """
    def plot_channel_locations(self, file_data):
        plot_sensors(file_data.info)
        # file_data.plot_sensors(show_names=True)

    def plot_data(self, file_data, file_type):
        if file_type == "Raw":
            file_data.plot(scalings="auto", n_channels=10)
        else:
            file_data.plot(scalings="auto", n_epochs=5, n_channels=10)

    def plot_erps(self, file_data, channels_selected):
        erps = file_data.average()
        erps.plot_joint(picks=channels_selected)

    """
    Updates
    """
    def update_path_to_file(self, path_to_file):
        label_item = self.grid_layout.itemAtPosition(0, 1).widget()
        label_item.setText(path_to_file)

    def update_sampling_frequency(self, frequency):
        label_item = self.grid_layout.itemAtPosition(3, 1).widget()
        label_item.setText(str(frequency))

    def update_reference(self, references):
        label_item = self.grid_layout.itemAtPosition(9, 1).widget()
        label_item.setText(str(references))

    def update_ica_decomposition(self, ica_status):
        label_item = self.grid_layout.itemAtPosition(11, 1).widget()
        label_item.setText(str(ica_status))

    def update_dataset_size(self, dataset_size):
        label_item = self.grid_layout.itemAtPosition(12, 1).widget()
        label_item.setText(str(dataset_size))

    """
    Getters
    """
    def get_path_to_file(self):
        path_to_file = QFileDialog().getSaveFileName(self, "Save file as")
        return path_to_file[0]
