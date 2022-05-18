#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main model
"""

import numpy as np

from os.path import getsize, splitext
from copy import copy

from PyQt6.QtCore import QThreadPool

from mne import read_events

from runnables.tools_runnable import filterRunnable, icaRunnable, sourceEstimationRunnable, resamplingRunnable, \
    reReferencingRunnable, extractEpochsRunnable
from runnables.files_runnable import openCntFileRunnable, openSetFileRunnable, openFifFileRunnable, \
    findEventsFromChannelRunnable, loadDataInfoRunnable
from runnables.plots_runnable import powerSpectralDensityRunnable, timeFrequencyRunnable
from runnables.connectivity_runnable import envelopeCorrelationRunnable, sourceSpaceConnectivityRunnable, \
    sensorSpaceConnectivityRunnable
from runnables.classification_runnable import classifyRunnable

from exceptions.exceptions import EventFileError

from utils.file_path_search import get_directory_path_from_file_path
from utils.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class mainModel:
    def __init__(self):
        """
        The main model is the main class where the computation are held.
        It contains the MNE "Epochs" or "Raw" object as well as additional information for the display or the computation.
        It is responsible for computing some simple information directly or calling the "Runnables".
        (Runnables are separate instances that will run in parallel to the main window so that it is not stuck.)
        It thus manages all the Runnables that will do the required computations.
        """
        self.main_listener = None

        self.file_data = None
        self.file_type = None
        self.file_path_name = None

        # The 3 tmp variables are used when loading a dataset, prevents the case that if a new dataset is loaded and an
        # error occurs, the old data won't be overwritten if there was a dataset loaded before.
        self.file_data_tmp = None
        self.file_type_tmp = None
        self.file_path_name_tmp = None

        self.channels_locations = {}
        self.ica_decomposition = "No"
        self.references = "Unknown"
        self.read_events = None     # Events info read from file or channel, used to transform raw to epochs

        # Runnable
        self.open_fif_file_runnable = None
        self.open_cnt_file_runnable = None
        self.open_set_file_runnable = None
        self.load_data_info_runnable = None
        self.find_events_from_channel_runnable = None

        self.filter_runnable = None
        self.resampling_runnable = None
        self.re_referencing_runnable = None
        self.ica_data_decomposition_runnable = None
        self.extract_epochs_runnable = None
        self.source_estimation_runnable = None

        self.power_spectral_density_runnable = None
        self.time_frequency_runnable = None

        self.envelope_correlation_runnable = None
        self.source_space_connectivity_runnable = None
        self.sensor_space_connectivity_runnable = None

        self.classify_runnable = None

    """
    File menu
    """
    # Open FIF File
    def open_fif_file(self, path_to_file):
        """
        Creates the parallel runnable for opening a FIF file.
        :param path_to_file: Path to the file
        :type path_to_file: str
        """
        pool = QThreadPool.globalInstance()
        self.open_fif_file_runnable = openFifFileRunnable(path_to_file)
        pool.start(self.open_fif_file_runnable)
        self.open_fif_file_runnable.signals.finished.connect(self.open_fif_file_computation_finished)

    def open_fif_file_computation_finished(self):
        """
        Retrieves the data from the runnable when the FIF file has been opened.
        Notifies the main controller that the reading is done.
        """
        self.file_data_tmp = self.open_fif_file_runnable.get_file_data()
        self.file_type_tmp = self.open_fif_file_runnable.get_file_type()
        self.file_path_name_tmp = self.open_fif_file_runnable.get_path_to_file()
        self.main_listener.open_fif_file_computation_finished()

    # Open CNT File
    def open_cnt_file(self, path_to_file):
        """
        Creates the parallel runnable for opening a CNT file.
        :param path_to_file: Path to the file
        :type path_to_file: str
        """
        pool = QThreadPool.globalInstance()
        self.open_cnt_file_runnable = openCntFileRunnable(path_to_file)
        pool.start(self.open_cnt_file_runnable)
        self.open_cnt_file_runnable.signals.finished.connect(self.open_cnt_file_computation_finished)

    def open_cnt_file_computation_finished(self):
        """
        Retrieves the data from the runnable when the CNT file has been opened.
        Notifies the main controller that the reading is done.
        """
        self.file_data_tmp = self.open_cnt_file_runnable.get_file_data()
        self.file_type_tmp = self.open_cnt_file_runnable.get_file_type()
        self.file_path_name_tmp = self.open_cnt_file_runnable.get_path_to_file()
        self.main_listener.open_cnt_file_computation_finished()

    # Open SET File
    def open_set_file(self, path_to_file):
        """
        Creates the parallel runnable for opening a SET file.
        :param path_to_file: Path to the file
        :type path_to_file: str
        """
        pool = QThreadPool.globalInstance()
        self.open_set_file_runnable = openSetFileRunnable(path_to_file)
        pool.start(self.open_set_file_runnable)
        self.open_set_file_runnable.signals.finished.connect(self.open_set_file_computation_finished)

    def open_set_file_computation_finished(self):
        """
        Retrieves the data from the runnable when the SET file has been opened.
        Notifies the main controller that the reading is done.
        """
        self.file_data_tmp = self.open_set_file_runnable.get_file_data()
        self.file_type_tmp = self.open_set_file_runnable.get_file_type()
        self.file_path_name_tmp = self.open_set_file_runnable.get_path_to_file()
        self.main_listener.open_set_file_computation_finished()

    # Data Info
    def load_data_info(self, montage, channels_selected, tmin, tmax):
        """
        Creates the parallel runnable for setting the additional information for the dataset.
        :param montage: Montage of the headset
        :type montage: str
        :param channels_selected: Channels selected
        :type channels_selected: list of str
        :param tmin: Start time of the epoch or raw file to keep
        :type tmin: float
        :param tmax: End time of the epoch or raw file to keep
        :type tmax: float
        """
        pool = QThreadPool.globalInstance()
        self.load_data_info_runnable = loadDataInfoRunnable(self.file_data_tmp, montage, channels_selected, tmin, tmax)
        pool.start(self.load_data_info_runnable)
        self.load_data_info_runnable.signals.finished.connect(self.load_data_info_computation_finished)

    def load_data_info_computation_finished(self):
        """
        Retrieves the data from the runnable when the last information have been updated.
        Notifies the main controller that the reading is done.
        """
        self.file_data = self.load_data_info_runnable.get_file_data()
        self.file_type = self.file_type_tmp
        self.file_path_name = self.file_path_name_tmp
        self.create_channels_locations()
        self.reset_tmp_attributes()
        self.main_listener.load_data_info_computation_finished()

    # Events
    def read_events_file(self, path_to_file):
        """
        Read an events file provided.
        This events file must be a FIF or a TXT file.
        The FIF files are provided when exporting an event file from MNE or MNE_Vision
        The TXT files are file where each line is of the form "
        :param path_to_file: Path to the file
        :type path_to_file: str
        """
        try:
            extension = path_to_file[-3:]
            if extension == "txt" or extension == "fif":
                events = read_events(path_to_file)
                self.read_events = events
            else:
                raise EventFileError()
        except EventFileError:
            error_message = "The event file extension must be '.txt' or '.fif'."
            error_window = errorWindow(error_message)
            error_window.show()
        except ValueError as error:
            error_message = "Could not read the file, please check your event file."
            detailed_message = str(error)
            error_window = errorWindow(error_message, detailed_message)
            error_window.show()
        except Exception as e:
            print(type(e))
            print(e)

    def find_events_from_channel(self, stim_channel):
        """
        Creates the parallel runnable for finding the events from a stimulation channel.
        :param stim_channel: Channel containing the stimulation/the events
        :type stim_channel: str
        """
        pool = QThreadPool.globalInstance()
        self.find_events_from_channel_runnable = findEventsFromChannelRunnable(self.file_data, stim_channel)
        pool.start(self.find_events_from_channel_runnable)
        self.find_events_from_channel_runnable.signals.finished.connect(self.find_events_from_channel_computation_finished)
        self.find_events_from_channel_runnable.signals.error.connect(self.find_events_from_channel_computation_error)

    def find_events_from_channel_computation_finished(self):
        """
        Retrieves the data from the runnable when the events are found from the provided channel.
        Notifies the main controller that the computation is done.
        """
        self.read_events = self.find_events_from_channel_runnable.get_read_events()
        self.main_listener.find_events_from_channel_computation_finished()

    def find_events_from_channel_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.find_events_from_channel_computation_error()

    # Save
    def save_file(self, path_to_file):
        """
        Saves the dataset into a FIF file, which is the extension of MNE.
        If the dataset is already a FIF file, overwrite it, otherwise create a new one.
        The name of the dataset will be the same as the previous one, but will have a FIF extension and will follow MNE
        conventions for file naming.
        :param path_to_file: Path to the file.
        :type path_to_file: str
        """
        if self.is_fif_file():
            self.file_data.save(path_to_file, overwrite=True)
        else:
            self.save_file_as(path_to_file)

    def save_file_as(self, path_to_file):
        """
        Saves the dataset into a FIF file, which is the extension of MNE.
        The name of the dataset will be the one provided by the user, but will have a FIF extension and will follow MNE
        conventions for file naming.
        :param path_to_file: Path to the file.
        :type path_to_file: str
        """
        if self.file_type == "Raw":
            self.file_path_name = path_to_file + "-raw.fif"
        else:
            self.file_path_name = path_to_file + "-epo.fif"
        self.file_data.save(self.file_path_name)

    """
    Tools menu
    """
    # Filtering
    def filter(self, low_frequency, high_frequency, channels_selected):
        """
        Creates the parallel runnable for filtering the dataset.
        :param low_frequency: Lowest frequency from where the data will be filtered.
        :type low_frequency: float
        :param high_frequency: Highest frequency from where the data will be filtered.
        :type high_frequency: float
        :param channels_selected: Channels on which the filtering will be performed.
        :type channels_selected: list of str
        """
        pool = QThreadPool.globalInstance()
        self.filter_runnable = filterRunnable(low_frequency, high_frequency, channels_selected, self.file_data)
        pool.start(self.filter_runnable)
        self.filter_runnable.signals.finished.connect(self.filter_computation_finished)

    def filter_computation_finished(self):
        """
        Retrieves the data from the runnable when the filtering is computed.
        Notifies the main controller that the computation is done.
        """
        self.file_data = self.filter_runnable.get_file_data()
        self.main_listener.filter_computation_finished()

    # Resampling
    def resampling(self, new_frequency):
        """
        Creates the parallel runnable for performing a resampling.
        :param new_frequency: The new frequency at which the data will be resampled.
        :type new_frequency: int
        """
        pool = QThreadPool.globalInstance()
        self.resampling_runnable = resamplingRunnable(new_frequency, self.file_data)
        pool.start(self.resampling_runnable)
        self.resampling_runnable.signals.finished.connect(self.resampling_computation_finished)

    def resampling_computation_finished(self):
        """
        Retrieves the data from the runnable when the resampling is computed.
        Notifies the main controller that the computation is done.
        """
        self.file_data = self.resampling_runnable.get_file_data()
        self.main_listener.resampling_computation_finished()

    # Re-referencing
    def re_referencing(self, references, n_jobs):
        """
        Creates the parallel runnable for performing a re-referencing.
        :param references: References from which the data will be re-referenced. Can be a single or multiple channels;
        Can be an average of all channels; Can be a "point to infinity".
        :type references: list of str; str
        :param n_jobs: Number of parallel processes used to compute the re-referencing
        :type n_jobs: int
        """
        pool = QThreadPool.globalInstance()
        self.re_referencing_runnable = reReferencingRunnable(references, self.file_data, n_jobs)
        pool.start(self.re_referencing_runnable)
        self.re_referencing_runnable.signals.finished.connect(self.re_referencing_computation_finished)

    def re_referencing_computation_finished(self):
        """
        Retrieves the data from the runnable when the re-referencing is computed.
        Notifies the main controller that the computation is done.
        """
        self.file_data = self.re_referencing_runnable.get_file_data()
        self.references = self.re_referencing_runnable.get_references()
        self.main_listener.re_referencing_computation_finished()

    # ICA decomposition
    def ica_data_decomposition(self, ica_method):
        """
        Creates the parallel runnable for performing the ICA decomposition of the dataset.
        :param ica_method: Method used for performing the ICA decomposition
        :type ica_method: str
        """
        pool = QThreadPool.globalInstance()
        self.ica_data_decomposition_runnable = icaRunnable(ica_method, self.file_data)
        pool.start(self.ica_data_decomposition_runnable)
        self.ica_data_decomposition_runnable.signals.finished.connect(self.ica_data_decomposition_computation_finished)

    def ica_data_decomposition_computation_finished(self):
        """
        Retrieves the data from the runnable when the ICA decomposition is computed.
        Notifies the main controller that the computation is done.
        """
        self.file_data = self.ica_data_decomposition_runnable.get_file_data()
        self.ica_decomposition = "Yes"
        self.main_listener.ica_decomposition_computation_finished()

    # Extract Epochs
    def extract_epochs(self, tmin, tmax):
        """
        Creates the parallel runnable for extracting the epochs of a dataset based on the events provided/or found beforehand.
        :param tmin: Start time of the epoch to keep
        :type tmin: float
        :param tmax: End time of the epoch to keep
        :type tmax: float
        """
        pool = QThreadPool.globalInstance()
        self.extract_epochs_runnable = extractEpochsRunnable(self.file_data, self.read_events, tmin, tmax)
        pool.start(self.extract_epochs_runnable)
        self.extract_epochs_runnable.signals.finished.connect(self.extract_epochs_computation_finished)

    def extract_epochs_computation_finished(self):
        """
        Retrieves the data from the runnable when the epochs are extracted from the available events.
        Notifies the main controller that the computation is done.
        """
        self.file_type = "Epochs"
        self.file_data = self.extract_epochs_runnable.get_file_data()
        self.main_listener.extract_epochs_computation_finished()

    # Source Estimation
    def source_estimation(self, source_estimation_method, save_data, load_data, n_jobs):
        """
        Creates the parallel runnable for computing the source estimation of the data.
        :param source_estimation_method: The method used to compute the source estimation
        :type source_estimation_method: str
        :param save_data: Boolean telling if the data computed must be saved into files.
        :type save_data: bool
        :param load_data: Boolean telling if the data used for the computation can be read from computer files.
        :type load_data: bool
        :param n_jobs: Number of processes used to computed the source estimation
        :type n_jobs: int
        """
        pool = QThreadPool.globalInstance()
        self.source_estimation_runnable = sourceEstimationRunnable(source_estimation_method, self.file_data,
                                                                   self.get_file_path_name_without_extension(),
                                                                   save_data, load_data, n_jobs)
        pool.start(self.source_estimation_runnable)
        self.source_estimation_runnable.signals.finished.connect(self.source_estimation_computation_finished)
        self.source_estimation_runnable.signals.error.connect(self.source_estimation_computation_error)

    def source_estimation_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.main_listener.source_estimation_computation_finished()

    def source_estimation_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.source_estimation_computation_error()

    """
    Plot menu
    """
    def power_spectral_density(self, method_psd, minimum_frequency, maximum_frequency, minimum_time, maximum_time):
        """
        Creates the parallel runnable for computing the power spectral density.
        :param method_psd: Method used to compute the power spectral density.
        :type method_psd: str
        :param minimum_frequency: Minimum frequency from which the power spectral density will be computed.
        :type minimum_frequency: float
        :param maximum_frequency: Maximum frequency from which the power spectral density will be computed.
        :type maximum_frequency: float
        :param minimum_time: Minimum time of the epochs from which the power spectral density will be computed.
        :type minimum_time: float
        :param maximum_time: Maximum time of the epochs from which the power spectral density will be computed.
        :type maximum_time: float
        """
        pool = QThreadPool.globalInstance()
        self.power_spectral_density_runnable = powerSpectralDensityRunnable(self.file_data, method_psd, minimum_frequency,
                                                                            maximum_frequency, minimum_time, maximum_time)
        pool.start(self.power_spectral_density_runnable)
        self.power_spectral_density_runnable.signals.finished.connect(self.power_spectral_density_computation_finished)

    def power_spectral_density_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.main_listener.plot_spectra_maps_computation_finished()

    def time_frequency(self, method_tfr, channel_selected, min_frequency, max_frequency, n_cycles):
        """
        Creates the parallel runnable for computing a time-frequency analysis of the data.
        :param method_tfr: Method used for computing the time-frequency analysis.
        :type method_tfr: str
        :param channel_selected: Channel on which the time-frequency analysis will be computed.
        :type channel_selected: str
        :param min_frequency: Minimum frequency from which the time-frequency analysis will be computed.
        :type min_frequency: float
        :param max_frequency: Maximum frequency from which the time-frequency analysis will be computed.
        :type max_frequency: float
        :param n_cycles: Number of cycles used by the time-frequency analysis for his computation.
        :type n_cycles: int
        """
        pool = QThreadPool.globalInstance()
        self.time_frequency_runnable = timeFrequencyRunnable(self.file_data, method_tfr, channel_selected,
                                                             min_frequency, max_frequency, n_cycles)
        pool.start(self.time_frequency_runnable)
        self.time_frequency_runnable.signals.finished.connect(self.time_frequency_computation_finished)
        self.time_frequency_runnable.signals.error.connect(self.time_frequency_computation_error)

    def time_frequency_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.main_listener.plot_time_frequency_computation_finished()

    def time_frequency_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.plot_time_frequency_computation_error()

    """
    Connectivity menu
    """
    def envelope_correlation(self):
        """
        Creates the parallel runnable for computing the envelope correlation between the channels of the dataset.
        """
        pool = QThreadPool.globalInstance()
        self.envelope_correlation_runnable = envelopeCorrelationRunnable(self.file_data)
        pool.start(self.envelope_correlation_runnable)
        self.envelope_correlation_runnable.signals.finished.connect(self.envelope_correlation_computation_finished)

    def envelope_correlation_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.main_listener.envelope_correlation_computation_finished()

    def source_space_connectivity(self, connectivity_method, spectrum_estimation_method, source_estimation_method, save_data,
                                  load_data, n_jobs):
        """
        Creates the parallel runnable for computing the connectivity inside the source space of the dataset.
        :param connectivity_method: Method used for computing the source space connectivity.
        :type connectivity_method: str
        :param spectrum_estimation_method: Method used for computing the spectrum estimation used inside the computation
        of the source space connectivity.
        :type spectrum_estimation_method: str
        :param source_estimation_method: Method used for computing the source estimation used inside the computation of
        the source space connectivity.
        :type source_estimation_method: str
        :param save_data: Boolean telling if the data computed must be saved into files.
        :type save_data: bool
        :param load_data: Boolean telling if the data used for the computation can be read from computer files.
        :type load_data: bool
        :param n_jobs: Number of processes used to computed the source estimation
        :type n_jobs: int
        """
        pool = QThreadPool.globalInstance()
        self.source_space_connectivity_runnable = sourceSpaceConnectivityRunnable(self.file_data, self.get_file_path_name_without_extension(),
                                                                                  connectivity_method, spectrum_estimation_method,
                                                                                  source_estimation_method, save_data, load_data,
                                                                                  n_jobs)
        pool.start(self.source_space_connectivity_runnable)
        self.source_space_connectivity_runnable.signals.finished.connect(self.source_space_connectivity_computation_finished)
        self.source_space_connectivity_runnable.signals.error.connect(self.source_space_connectivity_computation_error)

    def source_space_connectivity_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.main_listener.source_estimation_computation_finished()

    def source_space_connectivity_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.source_estimation_computation_error()

    def sensor_space_connectivity(self):
        """
        Creates the parallel runnable for computing the connectivity of the sensor space of the dataset.
        """
        pool = QThreadPool.globalInstance()
        self.sensor_space_connectivity_runnable = sensorSpaceConnectivityRunnable(self.file_data)
        pool.start(self.sensor_space_connectivity_runnable)
        self.sensor_space_connectivity_runnable.signals.finished.connect(self.sensor_space_connectivity_computation_finished)

    def sensor_space_connectivity_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.main_listener.sensor_space_connectivity_computation_finished()

    """
    Classification menu
    """
    def classify(self, pipeline_selected, feature_selection, hyper_tuning, cross_val_number):
        """
        Creates the parallel runnable for computing the classification with pipeline(s) of artificial intelligence of
        the dataset.
        :param pipeline_selected: The pipeline(s) used for the classification of the dataset.
        :type pipeline_selected: list of str
        :param feature_selection: Boolean telling if the computation of some feature selection techniques must be performed
        on the dataset.
        :type feature_selection: boolean
        :param hyper_tuning: Boolean telling if the computation of the tuning of the hyper-parameters of the pipelines must
        be performed on the dataset.
        :type hyper_tuning: boolean
        :param cross_val_number: Number of cross-validation fold used by the pipelines on the dataset.
        :type cross_val_number: int
        """
        pool = QThreadPool.globalInstance()
        self.classify_runnable = classifyRunnable(self.file_data, self.get_directory_path_from_file_path(),
                                                  pipeline_selected, feature_selection, hyper_tuning,
                                                  cross_val_number)
        pool.start(self.classify_runnable)
        self.classify_runnable.signals.finished.connect(self.classify_computation_finished)

    def classify_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.main_listener.classify_computation_finished()

    """
    Others
    """
    def is_fif_file(self):
        """
        Check if the dataset loaded is loaded from a FIF file.
        :return: True if the file used is a FIF file, False otherwise.
        :rtype: boolean
        """
        return self.file_path_name[-3:] == "fif"

    def create_channels_locations(self):
        """
        Retrieves the location of all channels from the MNE "Epochs" or "Raw" object for an easier use.
        Store the information inside the "self.channels_locations" attribute.
        """
        channels_info = self.file_data.info.get("chs")
        for channel in channels_info:
            self.channels_locations[channel["ch_name"]] = channel["loc"][:3]

    def reset_tmp_attributes(self):
        self.file_data_tmp = None
        self.file_type_tmp = None
        self.file_path_name_tmp = None

    """
    Getters
    """
    def get_all_displayed_info(self):
        """
        Gets all the information of the dataset that will be displayed on the main window.
        :return: A list of all the displayed information.
        :rtype: list of str/float/int
        """
        all_info = [self.get_file_path_name(), self.get_file_type(), self.get_number_of_channels(),
                    self.get_sampling_frequency(), self.get_number_of_events(), self.get_number_of_epochs(),
                    self.get_epochs_start(), self.get_epochs_end(), self.get_number_of_frames(),
                    self.get_reference(), self.get_channels_locations_status(), self.get_ica(), self.get_dataset_size()]
        return all_info

    def get_file_path_name(self):
        """
        Gets the file path of the dataset.
        :return: The file path of the dataset
        :rtype: str
        """
        return self.file_path_name

    def get_file_path_name_without_extension(self):
        """
        Gets the file path of the dataset without the extension of the file.
        :return: The file path of the dataset without the extension.
        :rtype: str
        """
        return splitext(self.file_path_name)[0]

    def get_directory_path_from_file_path(self):
        """
        Gets the directory path of the dataset.
        :return: The directory path of the dataset.
        :rtype: str
        """
        return get_directory_path_from_file_path(self.file_path_name)

    def get_file_type(self):
        """
        Gets the type of the file.
        :return: The type of the file.
        :rtype: str
        """
        return self.file_type

    def get_number_of_channels(self):
        """
        Gets the number of channels that are present in the dataset.
        :return: The number of channels
        :rtype: int
        """
        return len(self.file_data.ch_names)

    def get_sampling_frequency(self):
        """
        Gets the sampling frequency of the dataset.
        :return: The sampling frequency.
        :rtype: float
        """
        return self.file_data.info.get("sfreq")

    def get_number_of_events(self):
        """
        Gets the number of events present in the dataset.
        :return: The number of events. None for "Raw" type of dataset.
        :rtype: int/None
        """
        if self.file_type == "Raw":
            return None
        else:
            return len(self.file_data.events)

    def get_event_values(self):
        """
        Gets the events' information present in the dataset.
        :return: The events' information. Each event is represented by a list of 3 elements: First the latency time of
        the event; Second a "0" for MNE backwards compatibility; Third the event id.
        :rtype: list of, list of int
        """
        return self.file_data.events

    def get_event_ids(self):
        """
        Gets the events' ids present in the dataset.
        :return: The events' ids
        :rtype: dict
        """
        return self.file_data.event_id

    def get_number_of_epochs(self):
        """
        Gets the number of epochs present in the dataset.
        :return: The number of epochs. 1 for "Raw" type of dataset.
        :rtype: int
        """
        if self.file_type == "Raw":
            return 1
        else:
            return len(self.file_data)

    def get_epochs_start(self):
        """
        Gets the start time of the epochs of the dataset.
        :return: The start time of the epochs.
        :rtype: float
        """
        return round(self.file_data.times[0], 3)

    def get_epochs_end(self):
        """
        Gets the end time of the epochs of the dataset.
        :return: The end time of the epochs.
        :rtype: float
        """
        return round(self.file_data.times[-1], 3)

    def get_number_of_frames(self):
        """
        Gets the number of frames of the dataset. The number of frames depend from the start and end times of the epochs
        and the sampling frequency.
        :return: The number of frames.
        :rtype: int
        """
        return len(self.file_data.times)

    def get_reference(self):
        """
        Gets the references from which the dataset is based.
        :return: The references.
        :rtype: list of str/str
        """
        return self.references

    def get_channels_locations_status(self):
        """
        Gets the status of the channels' locations of the dataset.
        :return: "Unknown" if the channels' locations dict is empty. "Available" otherwise.
        :rtype: str
        """
        if not self.channels_locations:     # channels_locations dictionary is empty.
            return "Unknown"
        else:
            return "Available"

    def get_channels_locations(self):
        """
        Gets the channels' locations of the dataset.
        :return: The channels' locations.
        :rtype: dict
        """
        return self.channels_locations

    def get_ica(self):
        """
        Gets the status of the ICA decomposition of the dataset.
        :return: True if it is known by the software that the ICA decomposition has been performed. False otherwise.
        :rtype: boolean
        """
        return self.ica_decomposition

    def get_dataset_size(self):
        """
        Gets the size in megabits of the dataset.
        :return: The size of the dataset.
        :rtype: float
        """
        if self.file_path_name[-3:] == "set":
            return round(getsize(self.file_path_name[:-3] + "fdt") / (1024 ** 2), 3)
        else:
            return round(getsize(self.file_path_name) / (1024 ** 2), 3)

    def get_all_channels_names(self):
        """
        Gets all the channels' names of the dataset.
        :return: The channels' names.
        :rtype: list of str
        """
        return self.file_data.ch_names

    def get_file_data(self):
        """
        Gets the MNE "Epochs" or "Raw" data of the dataset.
        :return: The MNE "Epochs" or "Raw" object.
        :rtype: Epochs/Raw
        """
        return self.file_data

    """
    Temporaries
    """
    def get_all_tmp_channels_names(self):
        """
        Gets all the channels' names of the dataset being loaded.
        :return: The channels' names.
        :rtype: list of str
        """
        return self.file_data_tmp.ch_names

    def get_tmp_epochs_start(self):
        """
        Gets the start time of the epochs of the dataset being loaded.
        :return: The start time of the epochs.
        :rtype: float
        """
        return round(self.file_data_tmp.times[0], 3)

    def get_tmp_epochs_end(self):
        """
        Gets the end time of the epochs of the dataset being loaded.
        :return: The end time of the epochs.
        :rtype: float
        """
        return round(self.file_data_tmp.times[-1], 3)

    """
    Runnable getters
    """
    def get_source_estimation_data(self):
        """
        Gets the data of the source estimation computation performed on the dataset.
        :return: The source estimation's data.
        :rtype: MNE.SourceEstimation
        """
        return self.source_estimation_runnable.get_source_estimation_data()

    def get_psds(self):
        """
        Gets the "psds" data of the power spectral density computation performed on the dataset.
        :return: The actual power spectral density data computed
        :rtype: list of, list of, list of float
        """
        return self.power_spectral_density_runnable.get_psds()

    def get_freqs(self):
        """
        Gets the "freqs" data of the power spectral density computation performed on the dataset.
        :return: The frequencies at which the power spectral density is computed.
        :rtype: list of float
        """
        return self.power_spectral_density_runnable.get_freqs()

    def get_tfr_channel_selected(self):
        """
        Gets the channel used for the computation of the time-frequency analysis performed on the dataset.
        :return: The channel used for the time-frequency analysis computation.
        :rtype: list of str
        """
        return self.time_frequency_runnable.get_channel_selected()

    def get_power(self):
        """
        Gets the "power" data of the time-frequency analysis computation performed on the dataset.
        :return: "power" data of the time-frequency analysis computation.
        :rtype: MNE.AverageTFR
        """
        return self.time_frequency_runnable.get_power()

    def get_itc(self):
        """
        Gets the "itc" data of the time-frequency analysis computation performed on the dataset.
        :return: "itc" data of the time-frequency analysis computation.
        :rtype: MNE.AverageTFR
        """
        return self.time_frequency_runnable.get_itc()

    def get_envelope_correlation_data(self):
        """
        Gets the data of the envelope correlation computation performed on the dataset.
        :return: The envelope correlation's data.
        :rtype: list of, list of float
        """
        return self.envelope_correlation_runnable.get_envelope_correlation_data()

    def get_source_space_connectivity_data(self):
        """
        Gets the data of the source space connectivity computation performed on the dataset.
        :return: The source space's data.
        :rtype: list of, list of float
        """
        return self.source_space_connectivity_runnable.get_source_space_connectivity_data()

    def get_sensor_space_connectivity_data(self):
        """
        Gets the data of the sensor space connectivity computation performed on the dataset.
        :return: The sensor space's data.
        :rtype: list of, list of float
        """
        return self.sensor_space_connectivity_runnable.get_sensor_space_connectivity_data()

    def get_classifier(self):
        """
        Gets the classifier object obtained after the computation performed on the dataset.
        :return: The classifiers
        :rtype: ApplePyClassifier
        """
        return self.classify_runnable.get_classifier()

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Sets the main listener for the class that will be used for communications and send data.
        :param listener: The main listener
        :type listener: MainController
        """
        self.main_listener = listener

    def set_event_values(self, event_values):
        """
        Sets the values of the events for the dataset.
        :param event_values: The event values
        :type event_values: list of, list of int
        """
        self.file_data.events = np.copy(event_values)

    def set_event_ids(self, event_ids):
        """
        Sets the events' ids for the dataset.
        :param event_ids: The events' ids.
        :type event_ids: dict
        """
        self.file_data.event_id = copy(event_ids)

    def set_channel_locations(self, channel_locations, channel_names):
        """
        Sets the channels' locations inside the MNE "Epochs" or "Raw" object of the dataset.
        From the simpler format present in the "self.channels_location" attribute, creates a list of the form of the one
        used by MNE.
        :param channel_locations: The channels' locations.
        :type channel_locations: dict
        :param channel_names: The channels' names
        :type channel_names: list of str
        """
        self.channels_locations = copy(channel_locations)
        channels_info = self.file_data.info.get("chs")
        for i, channel in enumerate(channels_info):
            channel_location = self.channels_locations[channel_names[i]]
            channel["loc"] = np.array([channel_location[0], channel_location[1], channel_location[2], 0.0, 0.0, 0.0,
                                       np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN])

    def set_channel_names(self, channel_names):
        """
        Sets the channels' names inside the MNE "Epochs" or "Raw" object of the dataset.
        :param channel_names: The channels' names.
        :type channel_names: list of str
        """
        self.file_data.info.update({"ch_names": copy(channel_names)})
