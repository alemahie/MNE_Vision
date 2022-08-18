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
    def open_fif_file_computation_error(self):
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
    def open_cnt_file_computation_error(self):
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
    def open_set_file_computation_error(self):
        pass

    @abstractmethod
    def open_set_file_finished(self):
        pass

    # Load Data Info
    @abstractmethod
    def load_data_info_information(self, montage, channels_selected, tmin, tmax, dataset_name):
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

    # Export CSV
    @abstractmethod
    def export_data_to_csv_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def export_data_csv_computation_finished(self):
        pass

    @abstractmethod
    def export_data_csv_computation_error(self):
        pass

    # Export SET
    @abstractmethod
    def export_data_to_set_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def export_data_set_computation_finished(self):
        pass

    @abstractmethod
    def export_data_set_computation_error(self):
        pass

    # Export events
    @abstractmethod
    def export_events_to_file_clicked(self):
        pass

    @abstractmethod
    def export_events_txt_computation_finished(self):
        pass

    @abstractmethod
    def export_events_txt_computation_error(self):
        pass

    # Save
    @abstractmethod
    def save_file_clicked(self):
        pass

    @abstractmethod
    def save_file_as_clicked(self):
        pass

    # Clear dataset
    @abstractmethod
    def clear_dataset_clicked(self):
        pass

    # Study
    @abstractmethod
    def create_study_clicked(self):
        pass

    @abstractmethod
    def create_study_information(self, study_name, task_name, dataset_names, dataset_indexes, subjects, sessions, runs,
                                 conditions, groups):
        pass

    @abstractmethod
    def clear_study_clicked(self):
        pass

    """
    Edit Menu
    """
    # Dataset info
    @abstractmethod
    def dataset_info_clicked(self):
        pass

    @abstractmethod
    def dataset_info_information(self, channels_selected):
        pass

    # Event values
    @abstractmethod
    def event_values_clicked(self):
        pass

    @abstractmethod
    def event_values_finished(self, event_values, event_ids):
        pass

    # Channel location
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
    # Filter
    @abstractmethod
    def filter_clicked(self):
        pass

    @abstractmethod
    def filter_information(self, low_frequency, high_frequency, channels_selected, filter_method):
        pass

    @abstractmethod
    def filter_computation_finished(self):
        pass

    @abstractmethod
    def filter_computation_error(self):
        pass

    @abstractmethod
    def filter_finished(self):
        pass

    # Resampling
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
    def resampling_computation_error(self):
        pass

    @abstractmethod
    def resampling_finished(self):
        pass

    # Re-referencing
    @abstractmethod
    def re_referencing_clicked(self):
        pass

    @abstractmethod
    def re_referencing_information(self, references, save_data, load_data, n_jobs):
        pass

    @abstractmethod
    def re_referencing_computation_finished(self):
        pass

    @abstractmethod
    def re_referencing_computation_error(self):
        pass

    @abstractmethod
    def re_referencing_finished(self):
        pass

    # Inspect data
    @abstractmethod
    def inspect_reject_data_clicked(self):
        pass

    # ICA decomposition
    @abstractmethod
    def ica_decomposition_clicked(self):
        pass

    @abstractmethod
    def ica_decomposition_information(self, ica_method):
        pass

    @abstractmethod
    def ica_data_decomposition_computation_finished(self):
        pass

    @abstractmethod
    def ica_data_decomposition_computation_error(self):
        pass

    @abstractmethod
    def ica_decomposition_finished(self):
        pass

    # Extract epochs
    @abstractmethod
    def extract_epochs_clicked(self):
        pass

    @abstractmethod
    def extract_epochs_information(self, tmin, tmax, trials_selected):
        pass

    @abstractmethod
    def extract_epochs_computation_finished(self):
        pass

    @abstractmethod
    def extract_epochs_computation_error(self):
        pass

    @abstractmethod
    def extract_epochs_finished(self):
        pass

    # SNR
    @abstractmethod
    def snr_clicked(self):
        pass

    @abstractmethod
    def snr_information(self, snr_methods, source_method, read, write, picks, trials_selected):
        pass

    @abstractmethod
    def snr_computation_finished(self):
        pass

    @abstractmethod
    def snr_computation_error(self):
        pass

    @abstractmethod
    def snr_finished(self):
        pass

    # Source Estimation
    @abstractmethod
    def source_estimation_clicked(self):
        pass

    @abstractmethod
    def source_estimation_information(self, source_estimation_method, save_data, load_data, epochs_method, trial_number,
                                      tmin, tmax, n_jobs, export_path):
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
    # Channel locations
    @abstractmethod
    def plot_channel_locations_clicked(self):
        pass

    @abstractmethod
    def plot_data_clicked(self):
        pass

    # Topographies
    @abstractmethod
    def plot_topographies_clicked(self):
        pass

    @abstractmethod
    def plot_topographies_information(self, time_points, mode):
        pass

    # Spectra maps
    @abstractmethod
    def plot_spectra_maps_clicked(self):
        pass

    @abstractmethod
    def plot_spectra_maps_information(self, minimum_frequency, maximum_frequency, minimum_time, maximum_time, topo_time_points):
        pass

    @abstractmethod
    def plot_spectra_maps_computation_finished(self):
        pass

    @abstractmethod
    def plot_spectra_maps_computation_error(self):
        pass

    @abstractmethod
    def plot_spectra_maps_finished(self):
        pass

    # ERP image
    @abstractmethod
    def plot_ERP_image_clicked(self):
        pass

    @abstractmethod
    def plot_ERP_image_information(self, channels_selected):
        pass

    # ERPs
    @abstractmethod
    def plot_ERPs_clicked(self):
        pass

    @abstractmethod
    def plot_ERPs_information(self, channel_selected):
        pass

    # Time frequency
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
    # Envelope correlation
    @abstractmethod
    def envelope_correlation_clicked(self):
        pass

    @abstractmethod
    def envelope_correlation_information(self, psi, fmin, fmax, connectivity_method, n_jobs, export_path):
        pass

    @abstractmethod
    def envelope_correlation_computation_finished(self):
        pass

    @abstractmethod
    def envelope_correlation_computation_error(self):
        pass

    @abstractmethod
    def envelope_correlation_finished(self):
        pass

    # Source space connectivity
    @abstractmethod
    def source_space_connectivity_clicked(self):
        pass

    @abstractmethod
    def source_space_connectivity_information(self, connectivity_method, spectrum_estimation_method, source_estimation_method,
                                              save_data, load_data, n_jobs, export_path, psi, fmin, fmax):
        pass

    @abstractmethod
    def source_space_connectivity_computation_finished(self):
        pass

    @abstractmethod
    def source_space_connectivity_finished(self):
        pass

    # Sensor space connectivity
    @abstractmethod
    def sensor_space_connectivity_clicked(self):
        pass

    @abstractmethod
    def sensor_space_connectivity_information(self, export_path):
        pass

    @abstractmethod
    def sensor_space_connectivity_computation_finished(self):
        pass

    @abstractmethod
    def sensor_space_connectivity_computation_error(self):
        pass

    @abstractmethod
    def sensor_space_connectivity_finished(self):
        pass

    # Spectro temporal connectivity
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
    def classify_information(self, pipeline_selected, feature_selection, number_of_channels_to_select, hyper_tuning,
                             cross_val_number, trials_selected):
        pass

    @abstractmethod
    def classify_computation_finished(self):
        pass

    @abstractmethod
    def classify_computation_error(self):
        pass

    @abstractmethod
    def classify_finished(self):
        pass

    """
    Statistics Menu
    """
    # SNR
    @abstractmethod
    def statistics_snr_clicked(self):
        pass

    @abstractmethod
    def statistics_snr_information(self, snr_methods, source_method, read, write, picks, stats_first_variable, stats_second_variable):
        pass

    # ERP
    @abstractmethod
    def statistics_erp_clicked(self):
        pass

    @abstractmethod
    def statistics_erp_information(self, channels_selected, stats_first_variable, stats_second_variable):
        pass

    # PSD
    @abstractmethod
    def statistics_psd_clicked(self):
        pass

    @abstractmethod
    def statistics_psd_information(self, minimum_frequency, maximum_frequency, minimum_time, maximum_time, topo_time_points,
                                   channel_selected, stats_first_variable, stats_second_variable):
        pass

    # ERSP ITC
    @abstractmethod
    def statistics_ersp_itc_clicked(self):
        pass

    @abstractmethod
    def statistics_ersp_itc_information(self, method_tfr, channel_selected, min_frequency, max_frequency, n_cycles,
                                        stats_first_variable, stats_second_variable):
        pass

    # Connectivity
    @abstractmethod
    def statistics_connectivity_clicked(self):
        pass

    @abstractmethod
    def statistics_connectivity_information(self, psi, fmin, fmax, connectivity_method, n_jobs, export_path,
                                            stats_first_variable, stats_second_variable):
        pass

    """
    Study Menu
    """
    @abstractmethod
    def edit_study_clicked(self):
        pass

    @abstractmethod
    def plot_study_clicked(self):
        pass

    """
    Dataset Menu
    """
    @abstractmethod
    def change_dataset(self, index_selected):
        pass

    @abstractmethod
    def study_selected(self):
        pass

    """
    Others 
    """
    @abstractmethod
    def download_fsaverage_mne_data_information(self):
        pass

    @abstractmethod
    def download_fsaverage_mne_data_computation_finished(self):
        pass
