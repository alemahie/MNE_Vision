#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main listener
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class mainListener(ABC):
    """
    The main listener is the link between the main view and the main controller, but also between most of the controllers.
    When the controller wants to send the information back to the main controller (who created it) it passes through the
    main listener, that will send the information to the main controller.
    It is here to "listen" and send the information to the correct place.
    """

    """
    File Menu
    """
    # Open FIF
    @abstractmethod
    def open_fif_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def open_fif_file_computation_finished(self):
        pass

    @abstractmethod
    def open_fif_file_finished(self):
        pass

    # Open CNT
    @abstractmethod
    def open_cnt_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def open_cnt_file_computation_finished(self):
        pass

    @abstractmethod
    def open_cnt_file_finished(self):
        pass

    # Open SET
    @abstractmethod
    def open_set_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def open_set_file_computation_finished(self):
        pass

    @abstractmethod
    def open_set_file_finished(self):
        pass

    # Load Data Info
    @abstractmethod
    def load_data_info_information(self, montage, channels_selected, tmin, tmax):
        pass

    @abstractmethod
    def load_data_info_computation_finished(self):
        pass

    # Events
    @abstractmethod
    def read_events_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def find_events_from_channel_clicked(self):
        pass

    @abstractmethod
    def find_events_from_channel_information(self, stim_channel):
        pass

    @abstractmethod
    def find_events_from_channel_computation_finished(self):
        pass

    @abstractmethod
    def find_events_from_channel_computation_error(self):
        pass

    # Export
    @abstractmethod
    def export_data_to_csv_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def export_data_csv_computation_finished(self):
        pass

    @abstractmethod
    def export_data_to_set_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def export_data_set_computation_finished(self):
        pass

    @abstractmethod
    def export_events_to_file_clicked(self):
        pass

    @abstractmethod
    def export_events_txt_computation_finished(self):
        pass

    # Save
    @abstractmethod
    def save_file_clicked(self):
        pass

    @abstractmethod
    def save_file_as_clicked(self):
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
    def event_values_finished(self, event_values, event_ids):
        pass

    @abstractmethod
    def channel_location_clicked(self):
        pass

    @abstractmethod
    def channel_location_finished(self, channel_locations, channel_names):
        pass

    @abstractmethod
    def select_data_clicked(self):
        pass

    @abstractmethod
    def select_data_events_clicked(self):
        pass

    """ 
    Tools Menu
    """
    @abstractmethod
    def filter_clicked(self):
        pass

    @abstractmethod
    def filter_information(self, low_frequency, high_frequency, channels_selected):
        pass

    @abstractmethod
    def filter_computation_finished(self):
        pass

    @abstractmethod
    def filter_finished(self):
        pass

    @abstractmethod
    def resampling_clicked(self):
        pass

    @abstractmethod
    def resampling_information(self, frequency):
        pass

    @abstractmethod
    def resampling_computation_finished(self):
        pass

    @abstractmethod
    def resampling_finished(self):
        pass

    @abstractmethod
    def re_referencing_clicked(self):
        pass

    @abstractmethod
    def re_referencing_information(self, references, n_jobs):
        pass

    @abstractmethod
    def re_referencing_computation_finished(self):
        pass

    @abstractmethod
    def re_referencing_finished(self):
        pass

    @abstractmethod
    def inspect_reject_data_clicked(self):
        pass

    @abstractmethod
    def ica_decomposition_clicked(self):
        pass

    @abstractmethod
    def ica_decomposition_information(self, ica_method):
        pass

    @abstractmethod
    def ica_decomposition_computation_finished(self):
        pass

    @abstractmethod
    def ica_decomposition_finished(self):
        pass

    @abstractmethod
    def extract_epochs_clicked(self):
        pass

    @abstractmethod
    def extract_epochs_information(self, tmin, tmax):
        pass

    @abstractmethod
    def extract_epochs_computation_finished(self):
        pass

    @abstractmethod
    def extract_epochs_finished(self):
        pass

    @abstractmethod
    def snr_clicked(self):
        pass

    # Source Estimation
    @abstractmethod
    def source_estimation_clicked(self):
        pass

    @abstractmethod
    def source_estimation_information(self, source_estimation_method, save_data, load_data, epochs_method, trial_number,
                                      n_jobs):
        pass

    @abstractmethod
    def source_estimation_computation_finished(self):
        pass

    @abstractmethod
    def source_estimation_finished(self):
        pass

    """
    Plot Menu
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
    def plot_topographies_information(self, time_points, mode):
        pass

    @abstractmethod
    def plot_spectra_maps_clicked(self):
        pass

    @abstractmethod
    def plot_spectra_maps_information(self, method_psd, minimum_frequency, maximum_frequency, minimum_time, maximum_time):
        pass

    @abstractmethod
    def plot_spectra_maps_computation_finished(self):
        pass

    @abstractmethod
    def plot_spectra_maps_finished(self):
        pass

    @abstractmethod
    def plot_ERP_image_clicked(self):
        pass

    @abstractmethod
    def plot_ERP_image_information(self, channels_selected):
        pass

    @abstractmethod
    def plot_ERPs_clicked(self):
        pass

    @abstractmethod
    def plot_ERPs_information(self, channel_selected):
        pass

    @abstractmethod
    def plot_time_frequency_clicked(self):
        pass

    @abstractmethod
    def plot_time_frequency_information(self, method_tfr, channel_selected, min_frequency, max_frequency, n_cycles):
        pass

    @abstractmethod
    def plot_time_frequency_computation_finished(self):
        pass

    @abstractmethod
    def plot_time_frequency_computation_error(self):
        pass

    @abstractmethod
    def plot_time_frequency_finished(self):
        pass

    """
    Connectivity Menu
    """
    @abstractmethod
    def envelope_correlation_clicked(self):
        pass

    @abstractmethod
    def envelope_correlation_information(self):
        pass

    @abstractmethod
    def envelope_correlation_computation_finished(self):
        pass

    @abstractmethod
    def envelope_correlation_finished(self):
        pass

    @abstractmethod
    def source_space_connectivity_clicked(self):
        pass

    @abstractmethod
    def source_space_connectivity_information(self, connectivity_method, spectrum_estimation_method, source_estimation_method,
                                              save_data, load_data, n_jobs):
        pass

    @abstractmethod
    def source_space_connectivity_computation_finished(self):
        pass

    @abstractmethod
    def source_space_connectivity_finished(self):
        pass

    @abstractmethod
    def sensor_space_connectivity_clicked(self):
        pass

    @abstractmethod
    def sensor_space_connectivity_information(self):
        pass

    @abstractmethod
    def sensor_space_connectivity_computation_finished(self):
        pass

    @abstractmethod
    def sensor_space_connectivity_finished(self):
        pass

    @abstractmethod
    def spectro_temporal_connectivity_clicked(self):
        pass

    @abstractmethod
    def spectro_temporal_connectivity_information(self):
        pass

    """
    Classification Menu
    """
    @abstractmethod
    def classify_clicked(self):
        pass

    @abstractmethod
    def classify_information(self, pipeline_selected, feature_selection, number_of_channels_to_select, hyper_tuning, cross_val_number):
        pass

    @abstractmethod
    def classify_computation_finished(self):
        pass

    @abstractmethod
    def classify_finished(self):
        pass

    """
    Others 
    """
    @abstractmethod
    def waiting_while_processing_finished(self, finish_method):
        pass

    @abstractmethod
    def download_fsaverage_mne_data_information(self):
        pass

    @abstractmethod
    def download_fsaverage_mne_data_computation_finished(self):
        pass
