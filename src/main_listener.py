#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main listener
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class mainListener(ABC):
    # File menu
    @abstractmethod
    def open_fif_file_clicked(self, path_to_file):
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

    # Edit menu
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

    # Tools menu
    @abstractmethod
    def filter_clicked(self):
        pass

    @abstractmethod
    def filter_information(self, low_frequency, high_frequency, channels_selected):
        pass

    @abstractmethod
    def resampling_clicked(self):
        pass

    @abstractmethod
    def resampling_information(self, frequency):
        pass

    @abstractmethod
    def re_referencing_clicked(self):
        pass

    @abstractmethod
    def re_referencing_information(self, references):
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

    # Plot menu
    @abstractmethod
    def plot_channel_locations_clicked(self):
        pass

    @abstractmethod
    def plot_data_clicked(self):
        pass

    @abstractmethod
    def plot_spectra_maps_clicked(self):
        pass

    @abstractmethod
    def plot_spectra_maps_information(self, method_psd, minimum_frequency, maximum_frequency):
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
    def plot_time_frequency_clicked(self):
        pass

    # Others
    @abstractmethod
    def waiting_while_processing_finished(self, finish_method):
        pass
