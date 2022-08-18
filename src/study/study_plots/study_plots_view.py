#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Study Plots View
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QScrollArea, QButtonGroup, QCheckBox

from utils.view.error_window import errorWindow
from utils.view.separator import create_layout_separator

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class studyPlotsView(QWidget):
    def __init__(self, study):
        """
        Window displaying the parameters for plotting study.
        :param study: The current study created on the datasets.
        :type study: studyModel
        """
        super().__init__()
        self.study_plots_listener = None

        self.select_unselect_channels_widget = None
        self.select_unselect_channels_layout = None
        self.select_all_channels = None
        self.unselect_all_channels = None

        self.select_unselect_subjects_widget = None
        self.select_unselect_subjects_layout = None
        self.select_all_subjects = None
        self.unselect_all_subjects = None

        self.study = study

        self.setWindowTitle("Study Plots")

        self.global_layout = QVBoxLayout()
        self.setLayout(self.global_layout)

        # Channels and subjects
        self.channels_subjects_widget = QWidget()
        self.channels_subjects_layout = QHBoxLayout()

        # Channels
        self.channels_widget = QWidget()
        self.channels_layout = QVBoxLayout()
        self.channels_button = QButtonGroup()
        self.create_select_unselect_channels_buttons()
        self.create_channels_check_boxes()
        self.channels_widget.setLayout(self.channels_layout)
        self.channels_scroll_area = QScrollArea()
        self.channels_scroll_area.setWidgetResizable(True)
        self.channels_scroll_area.setWidget(self.channels_widget)
        self.channels_subjects_layout.addWidget(self.channels_scroll_area)

        # Subjects
        self.subjects_widget = QWidget()
        self.subjects_layout = QVBoxLayout()
        self.subjects_button = QButtonGroup()
        self.create_select_unselect_subjects_buttons()
        self.create_subjects_check_boxes()
        self.subjects_widget.setLayout(self.subjects_layout)
        self.subjects_scroll_area = QScrollArea()
        self.subjects_scroll_area.setWidgetResizable(True)
        self.subjects_scroll_area.setWidget(self.subjects_widget)
        self.channels_subjects_layout.addWidget(self.subjects_scroll_area)

        self.channels_subjects_widget.setLayout(self.channels_subjects_layout)

        # Plot buttons
        self.plot_buttons_widget = QWidget()
        self.plot_buttons_layout = QVBoxLayout()
        self.erps_button = QPushButton("ERPs", self)
        self.erps_button.clicked.connect(self.erps_trigger)
        self.psd_button = QPushButton("PSD", self)
        self.psd_button.clicked.connect(self.psd_trigger)
        self.erp_image_button = QPushButton("ERP image", self)
        self.erp_image_button.clicked.connect(self.erp_image_trigger)
        self.ersp_itc_button = QPushButton("ERSP-ITC", self)
        self.ersp_itc_button.clicked.connect(self.ersp_itc_trigger)
        self.plot_buttons_layout.addWidget(self.erps_button)
        self.plot_buttons_layout.addWidget(self.psd_button)
        self.plot_buttons_layout.addWidget(self.erp_image_button)
        self.plot_buttons_layout.addWidget(self.ersp_itc_button)
        self.plot_buttons_widget.setLayout(self.plot_buttons_layout)

        # Cancel Confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_study_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_study_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        # Layout
        self.global_layout.addWidget(self.channels_subjects_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.plot_buttons_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.cancel_confirm_widget)

    def create_select_unselect_channels_buttons(self):
        self.select_unselect_channels_widget = QWidget()
        self.select_unselect_channels_layout = QHBoxLayout()
        self.select_all_channels = QPushButton("&Select All", self)
        self.select_all_channels.clicked.connect(self.select_all_channels_trigger)
        self.unselect_all_channels = QPushButton("&Unselect All", self)
        self.unselect_all_channels.clicked.connect(self.unselect_all_channels_trigger)
        self.select_unselect_channels_layout.addWidget(self.select_all_channels)
        self.select_unselect_channels_layout.addWidget(self.unselect_all_channels)
        self.select_unselect_channels_widget.setLayout(self.select_unselect_channels_layout)
        self.channels_layout.addWidget(self.select_unselect_channels_widget)

    def create_channels_check_boxes(self):
        channel_names = self.study.get_channel_names()
        self.channels_button.setExclusive(False)
        for i, channel in enumerate(channel_names):
            check_box = QCheckBox()
            check_box.setText(channel)
            check_box.setChecked(True)
            self.channels_layout.addWidget(check_box)
            self.channels_button.addButton(check_box, i)

    def create_select_unselect_subjects_buttons(self):
        self.select_unselect_subjects_widget = QWidget()
        self.select_unselect_subjects_layout = QHBoxLayout()
        self.select_all_subjects = QPushButton("&Select All", self)
        self.select_all_subjects.clicked.connect(self.select_all_subjects_trigger)
        self.unselect_all_subjects = QPushButton("&Unselect All", self)
        self.unselect_all_subjects.clicked.connect(self.unselect_all_subjects_trigger)
        self.select_unselect_subjects_layout.addWidget(self.select_all_subjects)
        self.select_unselect_subjects_layout.addWidget(self.unselect_all_subjects)
        self.select_unselect_subjects_widget.setLayout(self.select_unselect_subjects_layout)
        self.subjects_layout.addWidget(self.select_unselect_subjects_widget)

    def create_subjects_check_boxes(self):
        subjects = self.study.get_unique_subjects()
        self.subjects_button.setExclusive(False)
        for i, subject in enumerate(subjects):
            check_box = QCheckBox()
            check_box.setText(subject)
            check_box.setChecked(True)
            self.subjects_layout.addWidget(check_box)
            self.subjects_button.addButton(check_box, i)

    """
    Triggers
    """
    def cancel_study_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.study_plots_listener.cancel_button_clicked()

    def confirm_study_trigger(self):
        """
        Retrieve all the additional information and send the information to the controller.
        """
        self.study_plots_listener.confirm_button_clicked()

    def erps_trigger(self):
        """
        Retrieve all the information for plotting the erps.
        """
        channels_selected = self.get_all_channels_selected()
        subjects_selected = self.get_all_subjects_selected()
        if len(channels_selected) == 0:
            error_message = "Please select at least one channel to plot the ERPs."
            error_window = errorWindow(error_message)
            error_window.show()
        elif len(subjects_selected) == 0:
            error_message = "Please select at least one subject to plot the ERPs."
            error_window = errorWindow(error_message)
            error_window.show()
        else:
            self.study_plots_listener.plot_erps_clicked(channels_selected, subjects_selected)

    def psd_trigger(self):
        """
        Retrieve all the information for plotting the psd.
        """
        channels_selected = self.get_all_channels_selected()
        subjects_selected = self.get_all_subjects_selected()
        if len(channels_selected) < 1:
            error_message = "Please select at least two channels to plot the PSD."
            error_window = errorWindow(error_message)
            error_window.show()
        elif len(subjects_selected) == 0:
            error_message = "Please select at least one subject to plot the PSD."
            error_window = errorWindow(error_message)
            error_window.show()
        else:
            self.study_plots_listener.plot_psd_clicked(channels_selected, subjects_selected)

    def erp_image_trigger(self):
        """
        Retrieve all the information for plotting the erp image.
        """
        channels_selected = self.get_all_channels_selected()
        subjects_selected = self.get_all_subjects_selected()
        if len(channels_selected) != 1:
            error_message = "Please select exactly one channel to plot the ERP image."
            error_window = errorWindow(error_message)
            error_window.show()
        elif len(subjects_selected) == 0:
            error_message = "Please select at least one subject to plot the ERP image."
            error_window = errorWindow(error_message)
            error_window.show()
        else:
            self.study_plots_listener.plot_erp_image_clicked(channels_selected, subjects_selected)

    def ersp_itc_trigger(self):
        """
        Retrieve all the information for plotting the ersp and itc.
        """
        channels_selected = self.get_all_channels_selected()
        subjects_selected = self.get_all_subjects_selected()
        if len(channels_selected) != 1:
            error_message = "Please select exactly one channel to plot the ERSP-ITC."
            error_window = errorWindow(error_message)
            error_window.show()
        elif len(subjects_selected) == 0:
            error_message = "Please select at least one subject to plot the ERSP-ITC."
            error_window = errorWindow(error_message)
            error_window.show()
        else:
            self.study_plots_listener.plot_ersp_itc_clicked(channels_selected, subjects_selected)

    def select_all_channels_trigger(self):
        """
        Select all the channels of the window.
        """
        for i in range(1, self.channels_layout.count()):
            check_box = self.channels_layout.itemAt(i).widget()
            check_box.setChecked(True)

    def unselect_all_channels_trigger(self):
        """
        Unselect all the channels of the window.
        """
        for i in range(1, self.channels_layout.count()):
            check_box = self.channels_layout.itemAt(i).widget()
            check_box.setChecked(False)

    def select_all_subjects_trigger(self):
        """
        Select all the subjects of the window.
        """
        for i in range(1, self.subjects_layout.count()):
            check_box = self.subjects_layout.itemAt(i).widget()
            check_box.setChecked(True)

    def unselect_all_subjects_trigger(self):
        """
        Unselect all the subjects of the window.
        """
        for i in range(1, self.subjects_layout.count()):
            check_box = self.subjects_layout.itemAt(i).widget()
            check_box.setChecked(False)

    """
    Plots
    """
    def plot_erps(self, evoked):
        """
        Plot the ERPs for the evoked data provided by the study.
        :param evoked: The evoked data to plot
        :type evoked: MNE Evoked
        """
        evoked.plot_joint()

    def plot_erp_image(self, file_data, channel_selected):
        """
        Plot the ERP image for the data provided by the study.
        :param file_data: The data containing the ERP image to plot
        :type file_data: MNE Epochs
        :param channel_selected: The channels selected.
        :type channel_selected: str
        """
        file_data.plot_image(picks=channel_selected)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: loadDataInfoController
        """
        self.study_plots_listener = listener

    """
    Getters
    """
    def get_all_channels_selected(self):
        """
        Get the elements selected by the user.
        :return: Channels selected
        :rtype: str/list of str
        """
        all_channels = []
        start_idx = 1   # 1 Because we have the select and unselect buttons.
        for i in range(start_idx, self.channels_layout.count()):
            check_box = self.channels_layout.itemAt(i).widget()
            if check_box.isChecked():
                all_channels.append(check_box.text())
        return all_channels

    def get_all_subjects_selected(self):
        """
        Get the subjects selected by the user.
        :return: Subjects selected
        :rtype: str/list of str
        """
        all_subjects = []
        start_idx = 1   # 1 Because we have the select and unselect buttons.
        for i in range(start_idx, self.subjects_layout.count()):
            check_box = self.subjects_layout.itemAt(i).widget()
            if check_box.isChecked():
                all_subjects.append(check_box.text())
        return all_subjects
