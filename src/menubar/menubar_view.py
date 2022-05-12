#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar, QMenu, QFileDialog

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class menubarView(QMenuBar):
    def __init__(self):
        super().__init__()
        self.menubarListener = None

        # File menu
        self.file_menu = QMenu("File", self)
        self.addMenu(self.file_menu)
        self.open_menu = QMenu("Open", self)
        self.create_open_menu()
        self.file_menu.addMenu(self.open_menu)
        self.events_menu = QMenu("Import events info", self)
        self.create_events_menu()
        self.file_menu.addMenu(self.events_menu)
        self.events_menu.setEnabled(False)
        self.export_menu = QMenu("Export", self)
        self.create_export_menu()
        self.file_menu.addMenu(self.export_menu)
        self.export_menu.setEnabled(False)
        self.create_file_menu()

        # Edit menu
        self.edit_menu = QMenu("Edit", self)
        self.addMenu(self.edit_menu)
        self.create_edit_menu()
        self.edit_menu.setEnabled(False)

        # Tools menu
        self.tools_menu = QMenu("Tools", self)
        self.addMenu(self.tools_menu)
        self.create_tools_menu()
        self.tools_menu.setEnabled(False)

        # Plot menu
        self.plot_menu = QMenu("Plot", self)
        self.addMenu(self.plot_menu)
        self.create_plot_menu()
        self.plot_menu.setEnabled(False)

        # Connectivity menu
        self.connectivity_menu = QMenu("Connectivity", self)
        self.addMenu(self.connectivity_menu)
        self.create_connectivity_menu()
        self.connectivity_menu.setEnabled(False)

        # Classification menu
        self.classification_menu = QMenu("Classification", self)
        self.addMenu(self.classification_menu)
        self.create_classification_menu()
        self.classification_menu.setEnabled(False)

        # Help menu
        self.help_menu = QMenu("Help", self)
        self.addMenu(self.help_menu)
        self.create_help_menu()

    def create_open_menu(self):
        open_fif_file_action = QAction("FIF File", self)
        open_fif_file_action.triggered.connect(self.open_fif_file_trigger)
        self.open_menu.addAction(open_fif_file_action)
        self.open_menu.addSeparator()
        open_cnt_file_action = QAction("CNT File", self)
        open_cnt_file_action.triggered.connect(self.open_cnt_file_trigger)
        self.open_menu.addAction(open_cnt_file_action)
        open_set_file_action = QAction("SET File", self)
        open_set_file_action.triggered.connect(self.open_set_file_trigger)
        self.open_menu.addAction(open_set_file_action)

    def create_events_menu(self):
        read_events_file_action = QAction("Read events from file (.fif/.txt)", self)
        read_events_file_action.triggered.connect(self.read_events_file_trigger)
        self.events_menu.addAction(read_events_file_action)
        find_events_from_channel_action = QAction("Read events from channel data", self)
        find_events_from_channel_action.triggered.connect(self.find_events_from_channel_trigger)
        self.events_menu.addAction(find_events_from_channel_action)

    def create_export_menu(self):
        export_data_to_file_action = QAction("Export data to file", self)
        export_data_to_file_action.triggered.connect(self.export_data_to_file_trigger)
        self.export_menu.addAction(export_data_to_file_action)
        export_events_to_file_action = QAction("Export events to file", self)
        export_events_to_file_action.triggered.connect(self.export_events_to_file_trigger)
        self.export_menu.addAction(export_events_to_file_action)

    def create_file_menu(self):
        # Save
        self.file_menu.addSeparator()
        save_file_action = QAction("Save", self)
        save_file_action.triggered.connect(self.save_file_trigger)
        save_file_action.setEnabled(False)
        self.file_menu.addAction(save_file_action)
        save_file_as_action = QAction("Save As", self)
        save_file_as_action.triggered.connect(self.save_file_as_trigger)
        save_file_as_action.setEnabled(False)
        self.file_menu.addAction(save_file_as_action)
        # Other
        self.file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_program_trigger)
        self.file_menu.addAction(exit_action)

    def create_edit_menu(self):
        dataset_info_action = QAction("Dataset information", self)
        dataset_info_action.triggered.connect(self.dataset_info_trigger)
        self.edit_menu.addAction(dataset_info_action)
        event_values_action = QAction("Event values", self)
        event_values_action.triggered.connect(self.event_values_trigger)
        self.edit_menu.addAction(event_values_action)
        channel_location_action = QAction("Channel location", self)
        channel_location_action.triggered.connect(self.channel_location_trigger)
        self.edit_menu.addAction(channel_location_action)
        self.edit_menu.addSeparator()
        select_data_action = QAction("Select data", self)
        select_data_action.triggered.connect(self.select_data_trigger)
        select_data_action.setEnabled(False)
        self.edit_menu.addAction(select_data_action)
        select_data_events_action = QAction("Select data using events", self)
        select_data_events_action.triggered.connect(self.select_data_events_trigger)
        select_data_events_action.setEnabled(False)
        self.edit_menu.addAction(select_data_events_action)

    def create_tools_menu(self):
        filter_action = QAction("Filter", self)
        filter_action.triggered.connect(self.filter_trigger)
        self.tools_menu.addAction(filter_action)
        resampling_action = QAction("Resampling", self)
        resampling_action.triggered.connect(self.resampling_trigger)
        self.tools_menu.addAction(resampling_action)
        re_referencing_action = QAction("Re-Referencing", self)
        re_referencing_action.triggered.connect(self.re_referencing_trigger)
        self.tools_menu.addAction(re_referencing_action)
        self.tools_menu.addSeparator()
        inspect_reject_data_action = QAction("Inspect/Reject data by eyes", self)
        inspect_reject_data_action.triggered.connect(self.inspect_reject_data_trigger)
        inspect_reject_data_action.setEnabled(False)
        self.tools_menu.addAction(inspect_reject_data_action)
        self.tools_menu.addSeparator()
        decompose_ICA_action = QAction("Decompose data with ICA", self)
        decompose_ICA_action.triggered.connect(self.ica_decomposition_trigger)
        self.tools_menu.addAction(decompose_ICA_action)
        self.tools_menu.addSeparator()
        source_estimation_action = QAction("Source estimation", self)
        source_estimation_action.triggered.connect(self.source_estimation_trigger)
        self.tools_menu.addAction(source_estimation_action)

    def create_plot_menu(self):
        plot_channel_locations_action = QAction("Channel locations", self)
        plot_channel_locations_action.triggered.connect(self.plot_channel_locations)
        self.plot_menu.addAction(plot_channel_locations_action)
        self.plot_menu.addSeparator()
        plot_data_action = QAction("Channel data", self)
        plot_data_action.triggered.connect(self.plot_data_trigger)
        self.plot_menu.addAction(plot_data_action)
        plot_topographies_action = QAction("Channel topographies", self)
        plot_topographies_action.triggered.connect(self.plot_topographies_trigger)
        self.plot_menu.addAction(plot_topographies_action)
        plot_channel_spectra_maps_action = QAction("Channel spectra (PSD)", self)
        plot_channel_spectra_maps_action.triggered.connect(self.plot_spectra_maps_trigger)
        self.plot_menu.addAction(plot_channel_spectra_maps_action)
        plot_ERP_image_action = QAction("Channel ERP image", self)
        plot_ERP_image_action.triggered.connect(self.plot_ERP_image_trigger)
        self.plot_menu.addAction(plot_ERP_image_action)
        plot_ERPs_action = QAction("Channel ERPs", self)
        plot_ERPs_action.triggered.connect(self.plot_ERPs_trigger)
        self.plot_menu.addAction(plot_ERPs_action)
        plot_time_frequency_action = QAction("Channel time-frequency (ERSP/ITC)", self)
        plot_time_frequency_action.triggered.connect(self.plot_time_frequency_trigger)
        self.plot_menu.addAction(plot_time_frequency_action)

    def create_connectivity_menu(self):
        envelope_correlation_action = QAction("Envelope Correlation", self)
        envelope_correlation_action.triggered.connect(self.envelope_correlation_trigger)
        self.connectivity_menu.addAction(envelope_correlation_action)
        source_space_connectivity_action = QAction("Source Space Connectivity", self)
        source_space_connectivity_action.triggered.connect(self.source_space_connectivity_trigger)
        self.connectivity_menu.addAction(source_space_connectivity_action)
        sensor_space_connectivity_action = QAction("3D Sensor Space Connectivity", self)
        sensor_space_connectivity_action.triggered.connect(self.sensor_space_connectivity_trigger)
        self.connectivity_menu.addAction(sensor_space_connectivity_action)
        spectro_temporal_connectivity_action = QAction("Spectro-Temporal Connectivity", self)
        spectro_temporal_connectivity_action.triggered.connect(self.spectro_temporal_connectivity_trigger)
        spectro_temporal_connectivity_action.setEnabled(False)
        self.connectivity_menu.addAction(spectro_temporal_connectivity_action)

    def create_classification_menu(self):
        classify_action = QAction("Classify", self)
        classify_action.triggered.connect(self.classify_trigger)
        self.classification_menu.addAction(classify_action)

    def create_help_menu(self):
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.help_trigger)
        help_action.setEnabled(False)
        self.help_menu.addAction(help_action)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.about_trigger)
        about_action.setEnabled(False)
        self.help_menu.addAction(about_action)

    def enable_menu_when_file_loaded(self):
        menu_actions = self.file_menu.actions()
        self.events_menu.setEnabled(True)
        self.export_menu.setEnabled(True)
        for action in menu_actions:
            if action.text() == "Save" or action.text() == "Save As":
                action.setEnabled(True)
        self.edit_menu.setEnabled(True)
        self.tools_menu.setEnabled(True)
        self.plot_menu.setEnabled(True)
        self.connectivity_menu.setEnabled(True)
        self.classification_menu.setEnabled(True)

    """
    Triggers
    """
    # File menu triggers
    def open_fif_file_trigger(self):
        path_to_file = QFileDialog().getOpenFileName(self, "Open file", "*.fif")
        self.menubarListener.open_fif_file_clicked(path_to_file[0])

    def open_cnt_file_trigger(self):
        path_to_file = QFileDialog().getOpenFileName(self, "Open file", "*.cnt")
        self.menubarListener.open_cnt_file_clicked(path_to_file[0])

    def open_set_file_trigger(self):
        path_to_file = QFileDialog().getOpenFileName(self, "Open file", "*.set")
        self.menubarListener.open_set_file_clicked(path_to_file[0])

    def read_events_file_trigger(self):
        path_to_file = QFileDialog().getOpenFileName(self, "Open file")
        self.menubarListener.read_events_file_clicked(path_to_file[0])

    def find_events_from_channel_trigger(self):
        self.menubarListener.find_events_from_channel_clicked()

    def export_data_to_file_trigger(self):
        self.export_data_to_file_clicked()

    def export_events_to_file_trigger(self):
        self.export_events_to_file_clicked()

    def save_file_trigger(self):
        self.menubarListener.save_file_clicked()

    def save_file_as_trigger(self):
        self.menubarListener.save_file_as_clicked()

    def exit_program_trigger(self):
        self.menubarListener.exit_program_clicked()

    # Edit menu trigger
    def dataset_info_trigger(self):
        self.menubarListener.dataset_info_clicked()

    def event_values_trigger(self):
        self.menubarListener.event_values_clicked()

    def channel_location_trigger(self):
        self.menubarListener.channel_location_clicked()

    def select_data_trigger(self):
        self.menubarListener.select_data_clicked()

    def select_data_events_trigger(self):
        self.menubarListener.select_data_events_clicked()

    # Tools menu triggers
    def filter_trigger(self):
        self.menubarListener.filter_clicked()

    def resampling_trigger(self):
        self.menubarListener.resampling_clicked()

    def re_referencing_trigger(self):
        self.menubarListener.re_referencing_clicked()

    def inspect_reject_data_trigger(self):
        self.menubarListener.inspect_reject_data_clicked()

    def ica_decomposition_trigger(self):
        self.menubarListener.ica_decomposition_clicked()

    def source_estimation_trigger(self):
        self.menubarListener.source_estimation_clicked()

    # Plot menu triggers
    def plot_channel_locations(self):
        self.menubarListener.plot_channel_locations_clicked()

    def plot_data_trigger(self):
        self.menubarListener.plot_data_clicked()

    def plot_topographies_trigger(self):
        self.menubarListener.plot_topographies_clicked()

    def plot_spectra_maps_trigger(self):
        self.menubarListener.plot_spectra_maps_clicked()

    def plot_channel_properties_trigger(self):
        self.menubarListener.plot_channel_properties_clicked()

    def plot_ERP_image_trigger(self):
        self.menubarListener.plot_ERP_image_clicked()

    def plot_ERPs_trigger(self):
        self.menubarListener.plot_ERPs_clicked()

    def plot_time_frequency_trigger(self):
        self.menubarListener.plot_time_frequency_clicked()

    # Connectivity menu triggers
    def envelope_correlation_trigger(self):
        self.menubarListener.envelope_correlation_clicked()

    def source_space_connectivity_trigger(self):
        self.menubarListener.source_space_connectivity_clicked()

    def sensor_space_connectivity_trigger(self):
        self.menubarListener.sensor_space_connectivity_clicked()

    def spectro_temporal_connectivity_trigger(self):
        self.menubarListener.spectro_temporal_connectivity_clicked()

    # Classification menu triggers
    def classify_trigger(self):
        self.menubarListener.classify_clicked()

    # Help menu triggers
    def help_trigger(self):
        self.menubarListener.help_clicked()

    def about_trigger(self):
        self.menubarListener.about_clicked()

    """
    Setters
    """
    def set_listener(self, menubar_listener):
        self.menubarListener = menubar_listener
