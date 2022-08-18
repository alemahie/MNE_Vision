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
        """
        Controller for the menubar on top of the main window.
        Does the link between the main menus of the main window and the main controller.
        """
        self.main_listener = None
        self.menubar_view = menubarView()
        self.menubar_view.set_listener(self)

    def enable_menu(self):
        """
        Make the menus accessible when a dataset is loaded.
        """
        self.menubar_view.enable_menu()

    def disable_menu(self):
        """
        Make the menus disabled when no dataset is loaded.
        """
        self.menubar_view.disable_menu()

    def add_dataset(self, dataset_index, dataset_name, study_available):
        """
        Add a dataset in the dataset menu.
        :param dataset_index: The index of new dataset.
        :type dataset_index: int
        :param dataset_name: The name of the new dataset.
        :type dataset_name: str
        :param study_available: Enable the menu for selecting the study_creation if it is available.
        :type study_available: bool
        """
        self.menubar_view.add_dataset(dataset_index, dataset_name, study_available)

    def remove_dataset(self, dataset_index, study_available):
        """
        Remove a dataset from the dataset menu.
        :param dataset_index: The index of dataset to remove
        :type dataset_index: int
        :param study_available: Enable the menu for selecting the study_creation if it is available.
        :type study_available: bool
        """
        self.menubar_view.remove_dataset(dataset_index, study_available)

    def study_selection_activation(self):
        """
        Activate the menu for study_creation selection because a study_creation has been created.
        """
        self.menubar_view.study_selected_menu_activation()

    def study_selection_deactivation(self, study_exist):
        """
        Deactivate the menu for study_creation selection because a study_creation has been cleared.
        :param study_exist: True if the study exists, false otherwise
        :type study_exist: bool
        """
        self.menubar_view.dataset_selected_menu_activation(study_exist)

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

    def export_data_to_csv_file_clicked(self, path_to_file):
        self.main_listener.export_data_to_csv_file_clicked(path_to_file)

    def export_data_to_set_file_clicked(self, path_to_file):
        self.main_listener.export_data_to_set_file_clicked(path_to_file)

    def export_events_to_file_clicked(self):
        self.main_listener.export_events_to_file_clicked()

    def save_file_clicked(self):
        self.main_listener.save_file_clicked()

    def save_file_as_clicked(self):
        self.main_listener.save_file_as_clicked()

    def clear_dataset_clicked(self):
        self.main_listener.clear_dataset_clicked()

    def create_study_clicked(self):
        self.main_listener.create_study_clicked()

    def clear_study_clicked(self):
        self.main_listener.clear_study_clicked()

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

    def snr_clicked(self):
        self.main_listener.snr_clicked()

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

    # Statistics menu
    def statistics_snr_clicked(self):
        self.main_listener.statistics_snr_clicked()

    def statistics_erp_clicked(self):
        self.main_listener.statistics_erp_clicked()

    def statistics_psd_clicked(self):
        self.main_listener.statistics_psd_clicked()

    def statistics_ersp_itc_clicked(self):
        self.main_listener.statistics_ersp_itc_clicked()

    def statistics_connectivity_clicked(self):
        self.main_listener.statistics_connectivity_clicked()

    # Study menu
    def edit_study_clicked(self):
        self.main_listener.edit_study_clicked()

    def plot_study_clicked(self):
        self.main_listener.plot_study_clicked()

    # Dataset menu
    def change_dataset(self, index_selected):
        self.main_listener.change_dataset(index_selected)

    def study_selected(self):
        self.main_listener.study_selected()

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
