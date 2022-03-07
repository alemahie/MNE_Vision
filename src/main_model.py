#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main model
"""

from os.path import getsize, splitext

from PyQt6.QtCore import QThreadPool
from mne import read_epochs
from mne.io import read_raw_fif

from runnables.tools_runnable import icaRunnable, sourceEstimationRunnable
from runnables.files_runnable import openCntFileRunnable, openSetFileRunnable
from runnables.plots_runnable import powerSpectralDensityRunnable

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class mainModel:
    def __init__(self):
        self.main_listener = None

        self.file_path_name = None
        self.file_type = None
        self.file_data = None
        self.channels_locations = {}
        self.ica_decomposition = "No"
        self.references = "Unknown"

        self.open_cnt_file_runnable = None
        self.open_set_file_runnable = None
        self.ica_data_decomposition_runnable = None
        self.source_estimation_runnable = None
        self.power_spectral_density_runnable = None

    """
    Useful methods
    """
    def is_fif_file(self):
        return self.file_path_name[-3:] == "fif"

    def create_channels_locations(self):
        channels_info = self.file_data.info.get("chs")
        for channel in channels_info:
            self.channels_locations[channel["ch_name"]] = channel["loc"][:3]

    """
    File menu
    """
    def open_fif_file(self, path_to_file):
        if path_to_file[-7:-4] == "raw":
            self.file_type = "Raw"
            self.file_data = read_raw_fif(path_to_file, preload=True)
        else:
            self.file_type = "Epochs"
            self.file_data = read_epochs(path_to_file, preload=True)
        self.file_path_name = path_to_file
        self.create_channels_locations()

    def open_cnt_file(self, path_to_file):
        pool = QThreadPool.globalInstance()
        self.open_cnt_file_runnable = openCntFileRunnable(path_to_file)
        pool.start(self.open_cnt_file_runnable)
        self.open_cnt_file_runnable.signals.finished.connect(self.open_cnt_file_computation_finished)
        self.file_type = "Raw"
        self.file_path_name = path_to_file

    def open_cnt_file_computation_finished(self):
        self.file_data = self.open_cnt_file_runnable.get_file_data()
        self.create_channels_locations()
        self.main_listener.open_cnt_file_computation_finished()

    def open_set_file(self, path_to_file):
        pool = QThreadPool.globalInstance()
        self.open_set_file_runnable = openSetFileRunnable(path_to_file)
        pool.start(self.open_set_file_runnable)
        self.open_set_file_runnable.signals.finished.connect(self.open_set_file_computation_finished)
        self.file_path_name = path_to_file

    def open_set_file_computation_finished(self):
        self.file_data = self.open_set_file_runnable.get_file_data()
        self.file_type = self.open_set_file_runnable.get_file_type()
        self.create_channels_locations()
        self.main_listener.open_set_file_computation_finished()

    def save_file(self, path_to_file):
        if self.is_fif_file():
            self.file_data.save(path_to_file, overwrite=True)
        else:
            self.save_file_as(path_to_file)

    def save_file_as(self, path_to_file):
        if self.file_type == "Raw":
            self.file_path_name = path_to_file + "-raw.fif"
        else:
            self.file_path_name = path_to_file + "-epo.fif"
        self.file_data.save(self.file_path_name)

    """
    Tools menu
    """
    def filter(self, low_frequency, high_frequency, channels_selected):
        self.file_data.filter(l_freq=low_frequency, h_freq=high_frequency, picks=channels_selected)

    def resampling(self, new_frequency):
        self.file_data.resample(new_frequency)

    def re_referencing(self, references):
        self.file_data.set_eeg_reference(ref_channels=references)
        self.references = references

    def ica_data_decomposition(self, ica_method):
        pool = QThreadPool.globalInstance()
        self.ica_data_decomposition_runnable = icaRunnable(ica_method, self.file_data)
        pool.start(self.ica_data_decomposition_runnable)
        self.ica_data_decomposition_runnable.signals.finished.connect(self.ica_data_decomposition_computation_finished)

    def ica_data_decomposition_computation_finished(self):
        self.file_data = self.ica_data_decomposition_runnable.get_file_data()
        self.ica_decomposition = "Yes"
        self.main_listener.ica_decomposition_computation_finished()

    def source_estimation(self, source_estimation_method, save_data, load_data, n_jobs):
        pool = QThreadPool.globalInstance()
        self.source_estimation_runnable = sourceEstimationRunnable(source_estimation_method, self.file_data,
                                                                   self.get_file_path_name_without_extension(),
                                                                   save_data, load_data, n_jobs)
        pool.start(self.source_estimation_runnable)
        self.source_estimation_runnable.signals.finished.connect(self.source_estimation_computation_finished)

    def source_estimation_computation_finished(self):
        self.main_listener.source_estimation_computation_finished()

    """
    Plot menu
    """
    def power_spectral_density(self, method_psd, minimum_frequency, maximum_frequency):
        pool = QThreadPool.globalInstance()
        self.power_spectral_density_runnable = powerSpectralDensityRunnable(self.file_data, method_psd, minimum_frequency, maximum_frequency)
        pool.start(self.power_spectral_density_runnable)
        self.power_spectral_density_runnable.signals.finished.connect(self.power_spectral_density_computation_finished)

    def power_spectral_density_computation_finished(self):
        self.main_listener.plot_spectra_maps_computation_finished()

    """
    Getters
    """
    def get_all_displayed_info(self):
        all_info = [self.get_file_path_name(), self.get_file_type(), self.get_number_of_channels(),
                    self.get_sampling_frequency(), self.get_number_of_events(), self.get_number_of_epochs(),
                    self.get_epochs_start(), self.get_epochs_end(), self.get_number_of_frames(),
                    self.get_reference(), self.get_channels_locations_status(), self.get_ica(), self.get_dataset_size()]
        return all_info

    def get_file_path_name(self):
        return self.file_path_name

    def get_file_path_name_without_extension(self):
        return splitext(self.file_path_name)[0]

    def get_file_type(self):
        return self.file_type

    def get_number_of_channels(self):
        return len(self.file_data.ch_names)

    def get_sampling_frequency(self):
        return self.file_data.info.get("sfreq")

    def get_number_of_events(self):
        if self.file_type == "Raw":
            print("Raw")
        else:
            print("Epochs")

    def get_number_of_epochs(self):
        if self.file_type == "Raw":
            return 1
        else:
            return len(self.file_data)

    def get_epochs_start(self):
        return round(self.file_data.times[0], 3)

    def get_epochs_end(self):
        return round(self.file_data.times[-1], 3)

    def get_number_of_frames(self):
        return len(self.file_data.times)

    def get_reference(self):
        return self.references

    def get_channels_locations_status(self):
        if not self.channels_locations:     # channels_locations dictionary is empty.
            return "Unknown"
        else:
            return "Available"

    def get_channels_locations(self):
        return self.channels_locations

    def get_ica(self):
        return self.ica_decomposition

    def get_dataset_size(self):
        if self.file_path_name[-3:] == "set":
            return round(getsize(self.file_path_name[:-3] + "fdt") / (1024 ** 2), 3)
        else:
            return round(getsize(self.file_path_name) / (1024 ** 2), 3)

    def get_all_channels_names(self):
        return self.file_data.ch_names

    def get_file_data(self):
        return self.file_data

    def get_source_estimation_data(self):
        return self.source_estimation_runnable.get_source_estimation_data()

    def get_psds(self):
        return self.power_spectral_density_runnable.get_psds()

    def get_freqs(self):
        return self.power_spectral_density_runnable.get_freqs()

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
