#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

import sys

from menubar.menubar_listener import menubarListener
from menubar.menubar_view import menubarView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class menubarController(menubarListener):
    def __init__(self):
        self.main_listener = None
        self.menubar_view = menubarView()
        self.menubar_view.set_listener(self)

    def enable_menu_when_file_loaded(self):
        self.menubar_view.enable_menu_when_file_loaded()

    """
    Menu buttons clicked
    """
    # File menu
    def open_fif_file_clicked(self, path_to_file):
        self.main_listener.open_fif_file_clicked(path_to_file)

    def open_cnt_file_clicked(self, path_to_file):
        self.main_listener.open_cnt_file_clicked(path_to_file)

    def open_set_file_clicked(self, path_to_file):
        self.main_listener.open_set_file_clicked(path_to_file)

    def read_events_file_clicked(self, path_to_file):
        self.main_listener.read_events_file_clicked(path_to_file)

    def find_events_from_channel_clicked(self):
        self.main_listener.find_events_from_channel_clicked()

    def export_data_to_file_clicked(self):
        self.main_listener.export_data_to_file_clicked()

    def export_events_to_file_clicked(self):
        self.main_listener.export_events_to_file_clicked()

    def save_file_clicked(self):
        self.main_listener.save_file_clicked()

    def save_file_as_clicked(self):
        self.main_listener.save_file_as_clicked()

    def exit_program_clicked(self):
        sys.exit(0)

    # Edit menu
    def dataset_info_clicked(self):
        self.main_listener.dataset_info_clicked()

    def event_values_clicked(self):
        self.main_listener.event_values_clicked()

    def channel_location_clicked(self):
        self.main_listener.channel_location_clicked()

    def select_data_clicked(self):
        self.main_listener.select_data_clicked()

    def select_data_events_clicked(self):
        self.main_listener.select_data_events_clicked()

    # Tools menu
    def filter_clicked(self):
        self.main_listener.filter_clicked()

    def resampling_clicked(self):
        self.main_listener.resampling_clicked()

    def re_referencing_clicked(self):
        self.main_listener.re_referencing_clicked()

    def inspect_reject_data_clicked(self):
        self.main_listener.inspect_reject_data_clicked()

    def ica_decomposition_clicked(self):
        self.main_listener.ica_decomposition_clicked()

    def extract_epochs_clicked(self):
        self.main_listener.extract_epochs_clicked()

    def source_estimation_clicked(self):
        self.main_listener.source_estimation_clicked()

    # Plot menu
    def plot_channel_locations_clicked(self):
        self.main_listener.plot_channel_locations_clicked()

    def plot_data_clicked(self):
        self.main_listener.plot_data_clicked()

    def plot_topographies_clicked(self):
        self.main_listener.plot_topographies_clicked()

    def plot_spectra_maps_clicked(self):
        self.main_listener.plot_spectra_maps_clicked()

    def plot_ERP_image_clicked(self):
        self.main_listener.plot_ERP_image_clicked()

    def plot_ERPs_clicked(self):
        self.main_listener.plot_ERPs_clicked()

    def plot_time_frequency_clicked(self):
        self.main_listener.plot_time_frequency_clicked()

    # Connectivity menu
    def envelope_correlation_clicked(self):
        self.main_listener.envelope_correlation_clicked()

    def source_space_connectivity_clicked(self):
        self.main_listener.source_space_connectivity_clicked()

    def sensor_space_connectivity_clicked(self):
        self.main_listener.sensor_space_connectivity_clicked()

    def spectro_temporal_connectivity_clicked(self):
        self.main_listener.spectro_temporal_connectivity_clicked()

    # Classification menu
    def classify_clicked(self):
        self.main_listener.classify_clicked()

    # Help menu
    def help_clicked(self):
        print("Help")

    def about_clicked(self):
        print("About")

    """
    Setters
    """
    def set_listener(self, main_listener):
        self.main_listener = main_listener

    """
    Getters
    """
    def get_view(self):
        return self.menubar_view
