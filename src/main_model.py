#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main model
"""

import numpy as np

from os.path import getsize, splitext
from copy import copy

from PyQt6.QtCore import QThreadPool

from runnables.tools_runnable import filterRunnable, icaRunnable, sourceEstimationRunnable, resamplingRunnable, \
    reReferencingRunnable
from runnables.files_runnable import openCntFileRunnable, openSetFileRunnable, openFifFileRunnable
from runnables.plots_runnable import powerSpectralDensityRunnable, timeFrequencyRunnable
from runnables.classification_runnable import classifyRunnable

from utils.file_path_search import get_directory_path_from_file_path

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
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

        self.open_fif_file_runnable = None
        self.open_cnt_file_runnable = None
        self.open_set_file_runnable = None

        self.filter_runnable = None
        self.resampling_runnable = None
        self.re_referencing_runnable = None
        self.ica_data_decomposition_runnable = None
        self.source_estimation_runnable = None

        self.power_spectral_density_runnable = None
        self.time_frequency_runnable = None

        self.classify_runnable = None

    """
    File menu
    """
    def open_fif_file(self, path_to_file):
        pool = QThreadPool.globalInstance()
        self.open_fif_file_runnable = openFifFileRunnable(path_to_file)
        pool.start(self.open_fif_file_runnable)
        self.open_fif_file_runnable.signals.finished.connect(self.open_fif_file_computation_finished)

    def open_fif_file_computation_finished(self):
        self.file_data = self.open_fif_file_runnable.get_file_data()
        self.file_type = self.open_fif_file_runnable.get_file_type()
        self.file_path_name = self.open_fif_file_runnable.get_path_to_file()
        self.create_channels_locations()
        self.main_listener.open_fif_file_computation_finished()

    def open_cnt_file(self, path_to_file):
        pool = QThreadPool.globalInstance()
        self.open_cnt_file_runnable = openCntFileRunnable(path_to_file)
        pool.start(self.open_cnt_file_runnable)
        self.open_cnt_file_runnable.signals.finished.connect(self.open_cnt_file_computation_finished)

    def open_cnt_file_computation_finished(self):
        self.file_data = self.open_cnt_file_runnable.get_file_data()
        self.file_type = self.open_cnt_file_runnable.get_file_type()
        self.file_path_name = self.open_cnt_file_runnable.get_path_to_file()
        self.create_channels_locations()
        self.main_listener.open_cnt_file_computation_finished()

    def open_set_file(self, path_to_file):
        pool = QThreadPool.globalInstance()
        self.open_set_file_runnable = openSetFileRunnable(path_to_file)
        pool.start(self.open_set_file_runnable)
        self.open_set_file_runnable.signals.finished.connect(self.open_set_file_computation_finished)

    def open_set_file_computation_finished(self):
        self.file_data = self.open_set_file_runnable.get_file_data()
        self.file_type = self.open_set_file_runnable.get_file_type()
        self.file_path_name = self.open_set_file_runnable.get_file_path_name()
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
        pool = QThreadPool.globalInstance()
        self.filter_runnable = filterRunnable(low_frequency, high_frequency, channels_selected, self.file_data)
        pool.start(self.filter_runnable)
        self.filter_runnable.signals.finished.connect(self.filter_computation_finished)

    def filter_computation_finished(self):
        self.file_data = self.filter_runnable.get_file_data()
        self.main_listener.filter_computation_finished()

    def resampling(self, new_frequency):
        pool = QThreadPool.globalInstance()
        self.resampling_runnable = resamplingRunnable(new_frequency, self.file_data)
        pool.start(self.resampling_runnable)
        self.resampling_runnable.signals.finished.connect(self.resampling_computation_finished)

    def resampling_computation_finished(self):
        self.file_data = self.resampling_runnable.get_file_data()
        self.main_listener.resampling_computation_finished()

    def re_referencing(self, references, n_jobs):
        pool = QThreadPool.globalInstance()
        self.re_referencing_runnable = reReferencingRunnable(references, self.file_data, n_jobs)
        pool.start(self.re_referencing_runnable)
        self.re_referencing_runnable.signals.finished.connect(self.re_referencing_computation_finished)

    def re_referencing_computation_finished(self):
        self.file_data = self.re_referencing_runnable.get_file_data()
        self.references = self.re_referencing_runnable.get_references()
        self.main_listener.re_referencing_computation_finished()

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
    def power_spectral_density(self, method_psd, minimum_frequency, maximum_frequency, minimum_time, maximum_time):
        pool = QThreadPool.globalInstance()
        self.power_spectral_density_runnable = powerSpectralDensityRunnable(self.file_data, method_psd, minimum_frequency,
                                                                            maximum_frequency, minimum_time, maximum_time)
        pool.start(self.power_spectral_density_runnable)
        self.power_spectral_density_runnable.signals.finished.connect(self.power_spectral_density_computation_finished)

    def power_spectral_density_computation_finished(self):
        self.main_listener.plot_spectra_maps_computation_finished()

    def time_frequency(self, method_tfr, channel_selected, min_frequency, max_frequency, n_cycles):
        pool = QThreadPool.globalInstance()
        self.time_frequency_runnable = timeFrequencyRunnable(self.file_data, method_tfr, channel_selected,
                                                             min_frequency, max_frequency, n_cycles)
        pool.start(self.time_frequency_runnable)
        self.time_frequency_runnable.signals.finished.connect(self.time_frequency_computation_finished)
        self.time_frequency_runnable.signals.error.connect(self.time_frequency_computation_error)

    def time_frequency_computation_finished(self):
        self.main_listener.plot_time_frequency_computation_finished()

    def time_frequency_computation_error(self):
        self.main_listener.plot_time_frequency_computation_error()

    """
    Classification menu
    """
    def classify(self, pipeline_selected, feature_selection, hyper_tuning, cross_val_number):
        pool = QThreadPool.globalInstance()
        self.classify_runnable = classifyRunnable(self.file_data, self.get_directory_path_from_file_path(),
                                                  pipeline_selected, feature_selection, hyper_tuning,
                                                  cross_val_number)
        pool.start(self.classify_runnable)
        self.classify_runnable.signals.finished.connect(self.classify_computation_finished)

    def classify_computation_finished(self):
        self.main_listener.classify_computation_finished()

    """
    Others
    """
    def is_fif_file(self):
        return self.file_path_name[-3:] == "fif"

    def create_channels_locations(self):
        channels_info = self.file_data.info.get("chs")
        for channel in channels_info:
            self.channels_locations[channel["ch_name"]] = channel["loc"][:3]

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

    def get_directory_path_from_file_path(self):
        return get_directory_path_from_file_path(self.file_path_name)

    def get_file_type(self):
        return self.file_type

    def get_number_of_channels(self):
        return len(self.file_data.ch_names)

    def get_sampling_frequency(self):
        return self.file_data.info.get("sfreq")

    def get_number_of_events(self):
        if self.file_type == "Raw":
            return None
        else:
            return len(self.file_data.events)

    def get_event_values(self):
        return self.file_data.events

    def get_event_ids(self):
        return self.file_data.event_id

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

    """
    Runnable getters
    """
    def get_source_estimation_data(self):
        return self.source_estimation_runnable.get_source_estimation_data()

    def get_psds(self):
        return self.power_spectral_density_runnable.get_psds()

    def get_freqs(self):
        return self.power_spectral_density_runnable.get_freqs()

    def get_tfr_channel_selected(self):
        return self.time_frequency_runnable.get_channel_selected()

    def get_power(self):
        return self.time_frequency_runnable.get_power()

    def get_itc(self):
        return self.time_frequency_runnable.get_itc()

    def get_classifier(self):
        return self.classify_runnable.get_classifier()

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener

    def set_event_values(self, event_values):
        self.file_data.events = np.copy(event_values)

    def set_event_ids(self, event_ids):
        self.file_data.event_id = copy(event_ids)

    def set_channel_locations(self, channel_locations, channel_names):
        self.channels_locations = copy(channel_locations)
        channels_info = self.file_data.info.get("chs")
        for i, channel in enumerate(channels_info):
            channel_location = self.channels_locations[channel_names[i]]
            channel["loc"] = np.array([channel_location[0], channel_location[1], channel_location[2], 0.0, 0.0, 0.0,
                                       np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN])

    def set_channel_names(self, channel_names):
        self.file_data.info.update({"ch_names": copy(channel_names)})
