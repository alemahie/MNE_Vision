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
    File Menu
    """
    @abstractmethod
    def open_fif_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def open_fif_file_computation_finished(self):
        pass

    @abstractmethod
    def open_fif_file_finished(self):
        pass

    @abstractmethod
    def open_cnt_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def open_cnt_file_computation_finished(self):
        pass

    @abstractmethod
    def open_cnt_file_finished(self):
        pass

    @abstractmethod
    def open_set_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def open_set_file_computation_finished(self):
        pass

    @abstractmethod
    def open_set_file_finished(self):
        pass

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
    def dataset_info_finished(self, channel_locations, channel_names):
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
    def source_estimation_clicked(self):
        pass

    @abstractmethod
    def source_estimation_information(self, source_estimation_method, save_data, load_data, n_jobs):
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
    Classification Menu
    """
    @abstractmethod
    def classify_clicked(self):
        pass

    @abstractmethod
    def classify_information(self, pipeline_selected, feature_selection, hyper_tuning, cross_val_number):
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
