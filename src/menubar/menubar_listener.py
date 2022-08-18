#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class menubarListener(ABC):
    """
    Listener doing the connection between the controller and the view for displaying the menubar
    It retrieves the information from the view to send it to the controller.
    """

    """
    File menu
    """
    @abstractmethod
    def open_fif_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def open_cnt_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def open_set_file_clicked(self, path_to_file):
        pass

    # Events
    @abstractmethod
    def read_events_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def find_events_from_channel_clicked(self):
        pass

    # Export
    @abstractmethod
    def export_data_to_csv_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def export_data_to_set_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def export_events_to_file_clicked(self):
        pass

    # Save
    @abstractmethod
    def save_file_clicked(self):
        pass

    @abstractmethod
    def save_file_as_clicked(self):
        pass

    @abstractmethod
    def clear_dataset_clicked(self):
        pass

    # Study
    @abstractmethod
    def create_study_clicked(self):
        pass

    @abstractmethod
    def clear_study_clicked(self):
        pass

    # Other
    @abstractmethod
    def exit_program_clicked(self):
        pass

    """
    Edit Menu
    """
    @abstractmethod
    def dataset_info_clicked(self):
        pass

    @abstractmethod
    def event_values_clicked(self):
        pass

    @abstractmethod
    def channel_location_clicked(self):
        pass

    @abstractmethod
    def select_data_clicked(self):
        pass

    @abstractmethod
    def select_data_events_clicked(self):
        pass

    """
    Tools menu
    """
    @abstractmethod
    def filter_clicked(self):
        pass

    @abstractmethod
    def resampling_clicked(self):
        pass

    @abstractmethod
    def re_referencing_clicked(self):
        pass

    @abstractmethod
    def inspect_reject_data_clicked(self):
        pass

    @abstractmethod
    def ica_decomposition_clicked(self):
        pass

    @abstractmethod
    def extract_epochs_clicked(self):
        pass

    @abstractmethod
    def snr_clicked(self):
        pass

    @abstractmethod
    def source_estimation_clicked(self):
        pass

    """
    Plot menu
    """
    @abstractmethod
    def plot_channel_locations_clicked(self):
        pass

    @abstractmethod
    def plot_data_clicked(self):
        pass

    @abstractmethod
    def plot_topographies_clicked(self):
        pass

    @abstractmethod
    def plot_spectra_maps_clicked(self):
        pass

    @abstractmethod
    def plot_ERP_image_clicked(self):
        pass

    @abstractmethod
    def plot_ERPs_clicked(self):
        pass

    @abstractmethod
    def plot_time_frequency_clicked(self):
        pass

    """
    Connectivity menu
    """
    @abstractmethod
    def envelope_correlation_clicked(self):
        pass

    @abstractmethod
    def source_space_connectivity_clicked(self):
        pass

    @abstractmethod
    def sensor_space_connectivity_clicked(self):
        pass

    @abstractmethod
    def spectro_temporal_connectivity_clicked(self):
        pass

    """
    Classification menu
    """
    @abstractmethod
    def classify_clicked(self):
        pass

    """
    Statistics menu
    """
    @abstractmethod
    def statistics_snr_clicked(self):
        pass

    @abstractmethod
    def statistics_erp_clicked(self):
        pass

    @abstractmethod
    def statistics_psd_clicked(self):
        pass

    @abstractmethod
    def statistics_ersp_itc_clicked(self):
        pass

    @abstractmethod
    def statistics_connectivity_clicked(self):
        pass

    """
    Study menu
    """
    @abstractmethod
    def edit_study_clicked(self):
        pass

    @abstractmethod
    def plot_study_clicked(self):
        pass

    """
    Dataset menu
    """
    @abstractmethod
    def change_dataset(self, index_selected):
        pass

    @abstractmethod
    def study_selected(self):
        pass

    """
    Help menu
    """
    @abstractmethod
    def help_clicked(self):
        pass

    @abstractmethod
    def about_clicked(self):
        pass
