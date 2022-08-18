#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main view
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from mne.viz import plot_sensors, set_3d_backend, set_browser_backend

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class mainView(QMainWindow):
    def __init__(self):
        """
        The main view is the main window were all the information are displayed and where the menus are available.
        Update the information when they change and call the correct methods when a specific menu is clicked.
        """
        super().__init__()

        self.info_labels = ["       No dataset loaded", "Filename : ", "File Type : ", "Number of Channels : ",
                            "Sampling Frequency (Hz) : ", "Number of Events : ", "Number of Epochs : ", "Epoch start (sec) : ",
                            "Epoch end (sec) : ", "Number of Frames/Frames per Epoch : ", "Reference : ", "Channel Locations : ",
                            "ICA : ", "Dataset Size (Mb) : "]
        self.study_info_labels = ["       No dataset loaded", "Study Filename : ", "Study task name : ", "Number of subjects : ",
                                  "Number of conditions : ", "Number of sessions : ", "Number of groups : ", "Epochs Consistency : ",
                                  "Channels per frame : ", "Channel locations : ", "ICA Status : ", "Study Size (Mb) : "]

        self.central_widget = None
        self.grid_layout = None

        self.create_display()

        self.setWindowTitle("MNE Vision")
        self.setup_mne_backends()

    @staticmethod
    def setup_mne_backends():
        """
        Set the 2D and 3D backends that will be used by MNE for the plots.
        """
        set_browser_backend("matplotlib")
        set_3d_backend("pyvistaqt")

    def create_display(self):
        """
        Create the display of the main window.
        """
        self.central_widget = QWidget()
        self.grid_layout = QGridLayout(self)

        self.grid_layout.setSpacing(0)
        for i, info in enumerate(self.info_labels):
            label = QLabel(info)
            if i == 0:
                dataset_name_font = QFont('', 15)
                dataset_name_font.setBold(True)
                label.setFont(dataset_name_font)
                label.setAlignment(Qt.AlignBottom)
            elif 0 < i < 13:
                label.setObjectName("BoundariesGridLayoutLeft")
            elif i == 13:
                label.setObjectName("BoundariesGridLayoutBottomLeft")
            self.grid_layout.addWidget(label, i, 0)
        for i in range(1, 14):
            label = QLabel("/")
            if i != 13:
                label.setObjectName("BoundariesGridLayoutRight")
            else:
                label.setObjectName("BoundariesGridLayoutBottomRight")
            self.grid_layout.addWidget(label, i, 1)
        self.central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.central_widget)

    def display_info(self, all_info):
        """
        Display the information on the main screen.
        :param all_info: All the information to display.
        :type all_info: list of str/int/float/list
        """
        for i in range(14):
            if i != 0:
                label_item = self.grid_layout.itemAtPosition(i, 1).widget()
            else:           # Dataset name
                label_item = self.grid_layout.itemAtPosition(i, 0).widget()
                all_info[i] = "        " + all_info[i]
            label_item.setText(str(all_info[i]))

    def clear_display(self):
        """
        Clear the display when no dataset is loaded.
        """
        for i in range(14):
            if i != 0:
                label_item = self.grid_layout.itemAtPosition(i, 1).widget()
                label_item.setText("/")
            else:
                label_item = self.grid_layout.itemAtPosition(i, 0).widget()
                label_item.setText("        No dataset loaded")

    def create_study_display(self):
        """
        Create the display of the study_creation on the main window.
        """
        self.central_widget = QWidget()
        self.grid_layout = QGridLayout(self)

        self.grid_layout.setSpacing(0)
        for i, info in enumerate(self.study_info_labels):
            label = QLabel(info)
            if i == 0:
                dataset_name_font = QFont('', 15)
                dataset_name_font.setBold(True)
                label.setFont(dataset_name_font)
                label.setAlignment(Qt.AlignBottom)
            elif 0 < i < 11:
                label.setObjectName("BoundariesGridLayoutLeft")
            elif i == 11:
                label.setObjectName("BoundariesGridLayoutBottomLeft")
            self.grid_layout.addWidget(label, i, 0)
        for i in range(1, 12):
            label = QLabel("/")
            if i != 11:
                label.setObjectName("BoundariesGridLayoutRight")
            else:
                label.setObjectName("BoundariesGridLayoutBottomRight")
            self.grid_layout.addWidget(label, i, 1)
        self.central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.central_widget)

    def display_study_info(self, all_info):
        """
        Display the information of the study_creation on the main screen.
        :param all_info: All the information to display.
        :type all_info: list of str/int/float/list
        """
        for i in range(12):
            if i != 0:
                label_item = self.grid_layout.itemAtPosition(i, 1).widget()
            else:           # Dataset name
                label_item = self.grid_layout.itemAtPosition(i, 0).widget()
                all_info[i] = "        " + all_info[i]
            label_item.setText(str(all_info[i]))

    """
    Plot
    """
    @staticmethod
    def plot_channel_locations(file_data):
        """
        Plot the channels' location.
        :param file_data: "Epochs" or "Raw" MNE file containing the information about the dataset.
        :type file_data: MNE_Epochs/MNE_Raw
        """
        plot_sensors(file_data.info, show_names=True)

    @staticmethod
    def plot_data(file_data, file_type, events=None, event_id=None):
        """
        plot the data of all channels.
        :param file_data: "Epochs" or "Raw" MNE file containing the information about the dataset.
        :type file_data: MNE_Epochs/MNE_Raw
        :param file_type: The type of the file, either "Epochs" or "Raw"
        :type file_type: str
        :param events: Event values
        :type events: list of, list of int
        :param event_id: Event ids
        :type event_id: dict
        """
        if file_type == "Raw":
            file_data.plot(scalings="auto", n_channels=10)
        else:
            file_data.plot(scalings="auto", n_epochs=5, n_channels=10, events=events, event_id=event_id)

    @staticmethod
    def plot_topographies(file_data, time_points, mode):
        """
        Plot the topographies.
        :param file_data: "Epochs" or "Raw" MNE file containing the information about the dataset.
        :type file_data: MNE_Epochs/MNE_Raw
        :param time_points: Time points at which the topographies will be plotted.
        :type time_points: list of float
        :param mode: Mode used for plotting the topographies.
        :type mode: str
        """
        evoked = file_data.average()
        if mode == "separated":
            evoked.plot_topomap(times=time_points)
        elif mode == "animated":
            evoked.animate_topomap(times=time_points, frame_rate=2)

    @staticmethod
    def plot_erp_image(file_data, channel_selected):
        """
        Plot the ERP image.
        :param file_data: "Epochs" or "Raw" MNE file containing the information about the dataset.
        :type file_data: MNE_Epochs/MNE_Raw
        :param channel_selected: Channel selected
        :type channel_selected: str
        """
        file_data.plot_image(picks=channel_selected)

    @staticmethod
    def plot_erps(file_data, channels_selected):
        """
        Plot the ERPs.
        :param file_data: "Epochs" or "Raw" MNE file containing the information about the dataset.
        :type file_data: MNE_Epochs/MNE_Raw
        :param channels_selected: Channels selected.
        :type channels_selected: list of str
        """
        erps = file_data.average()
        if len(channels_selected) == 1:
            erps.plot(picks=channels_selected)
        else:
            erps.plot_joint(picks=channels_selected)

    """
    Updates
    """
    def update_dataset_name(self, dataset_name):
        """
        Update the dataset name on the main window.
        :param dataset_name: The dataset name.
        :type dataset_name: str
        """
        label_item = self.grid_layout.itemAtPosition(0, 0).widget()
        label_item.setText(dataset_name)

    def update_path_to_file(self, path_to_file):
        """
        Update the path to the file on the main window.
        :param path_to_file: Path to the file
        :type path_to_file: str
        """
        label_item = self.grid_layout.itemAtPosition(1, 1).widget()
        label_item.setText(path_to_file)

    def update_file_type(self, file_type):
        """
        Update the file type on the main window.
        :param file_type: File type, either "Epochs" or "Raw".
        :type file_type: str
        """
        label_item = self.grid_layout.itemAtPosition(2, 1).widget()
        label_item.setText(file_type)

    def update_sampling_frequency(self, frequency):
        """
        Update the sampling frequency on the main window.
        :param frequency: The frequency
        :type frequency: float
        """
        label_item = self.grid_layout.itemAtPosition(4, 1).widget()
        label_item.setText(str(frequency))

    def update_number_of_events(self, number_of_events):
        """
        Update the number of events on the main window.
        :param number_of_events: The number of events.
        :type number_of_events: int
        """
        label_item = self.grid_layout.itemAtPosition(5, 1).widget()
        label_item.setText(str(number_of_events))

    def update_number_of_epochs(self, number_of_epochs):
        """
        Update the number of epochs on the main window.
        :param number_of_epochs: The number of epochs.
        :type number_of_epochs: int
        """
        label_item = self.grid_layout.itemAtPosition(6, 1).widget()
        label_item.setText(str(number_of_epochs))

    def update_epoch_start(self, epoch_start):
        """
        Update the epochs start time on the main window.
        :param epoch_start: The epochs start time.
        :type epoch_start: float
        """
        label_item = self.grid_layout.itemAtPosition(7, 1).widget()
        label_item.setText(str(epoch_start))

    def update_epoch_end(self, epoch_end):
        """
        Update the epochs end time on the main window.
        :param epoch_end: The epochs end time.
        :type epoch_end: float
        """
        label_item = self.grid_layout.itemAtPosition(8, 1).widget()
        label_item.setText(str(epoch_end))

    def update_number_of_frames(self, number_of_frames):
        """
        Update the number of frames on the main window.
        :param number_of_frames: The number of frames.
        :type number_of_frames: int
        """
        label_item = self.grid_layout.itemAtPosition(9, 1).widget()
        label_item.setText(str(number_of_frames))

    def update_reference(self, references):
        """
        Update the references on the main window.
        :param references: The references.
        :type references: str/list of str
        """
        label_item = self.grid_layout.itemAtPosition(10, 1).widget()
        label_item.setText(str(references))

    def update_ica_decomposition(self, ica_status):
        """
        Update the ICA decomposition status on the main window.
        :param ica_status: The ICA decomposition status.
        :type ica_status: str
        """
        label_item = self.grid_layout.itemAtPosition(12, 1).widget()
        label_item.setText(str(ica_status))

    def update_dataset_size(self, dataset_size):
        """
        Update the dataset size on the main window.
        :param dataset_size: The dataset size.
        :type dataset_size: float
        """
        label_item = self.grid_layout.itemAtPosition(13, 1).widget()
        label_item.setText(str(dataset_size))

    """
    Getters
    """
    def get_save_path(self):
        """
        Get the path to the file when wanting to save the dataset.
        :return: The path to the file.
        :rtype: str
        """
        path_to_file = QFileDialog().getSaveFileName(self, "Save file as")
        return path_to_file[0]

    def get_export_path(self):
        """
        Get the path to the file when wanting to export the events.
        :return: The path to the file.
        :rtype: str
        """
        path_to_file = QFileDialog().getSaveFileName(self, "Export events to TXT file")
        return path_to_file[0]
