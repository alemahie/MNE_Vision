#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main model
"""

import numpy as np

from os.path import getsize, splitext
from copy import copy, deepcopy

from mne import read_events, find_events, events_from_annotations

from PyQt5.QtCore import QThreadPool

from runnables.tools_runnable import filterRunnable, icaRunnable, sourceEstimationRunnable, resamplingRunnable, \
    reReferencingRunnable, extractEpochsRunnable, signalToNoiseRatioRunnable
from runnables.files_runnable import openCntFileRunnable, openSetFileRunnable, openFifFileRunnable, \
    findEventsFromChannelRunnable, loadDataInfoRunnable, exportDataCSVRunnable, exportDataSETRunnable, \
    exportEventsTXTRunnable
from runnables.plots_runnable import timeFrequencyRunnable
from runnables.connectivity_runnable import envelopeCorrelationRunnable, sourceSpaceConnectivityRunnable, \
    sensorSpaceConnectivityRunnable
from runnables.classification_runnable import classifyRunnable
from runnables.statistics_runnable import statisticsSnrRunnable, statisticsErspItcRunnable, \
    statisticsConnectivityRunnable

from exceptions.exceptions import EventFileError

from utils.file_path_search import get_directory_path_from_file_path
from utils.view.error_window import errorWindow
from utils.model.study_model import studyModel

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

        # Datasets info
        self.current_dataset_index = -1     # -1, means no dataset.
        self.file_data = []
        self.file_type = []
        self.file_path_name = []
        self.dataset_name = []

        self.channels_locations = []    # {}
        self.ica_decomposition = []     # "No"
        self.references = []            # "Unknown"
        self.read_events = []           # None     # Events info read from file or channel, used to transform raw to epochs
        self.read_event_ids = []        # None  # Event ids

        # Study
        self.study = None
        self.study_selected = False
        self.study_index = None

        # The 3 tmp variables are used when loading a dataset, prevents the case that if a new dataset is loaded and an
        # error occurs, the old data won't be overwritten if there was a dataset loaded before.
        self.file_data_tmp = None
        self.file_type_tmp = None
        self.file_path_name_tmp = None
        self.dataset_name_tmp = None

        # Runnables
        self.open_fif_file_runnable = None
        self.open_cnt_file_runnable = None
        self.open_set_file_runnable = None
        self.load_data_info_runnable = None
        self.find_events_from_channel_runnable = None
        self.export_data_csv_runnable = None
        self.export_data_set_runnable = None
        self.export_events_txt_runnable = None

        self.filter_runnable = None
        self.resampling_runnable = None
        self.re_referencing_runnable = None
        self.ica_data_decomposition_runnable = None
        self.extract_epochs_runnable = None
        self.snr_runnable = None
        self.source_estimation_runnable = None

        self.power_spectral_density_runnable = None
        self.time_frequency_runnable = None

        self.envelope_correlation_runnable = None
        self.source_space_connectivity_runnable = None
        self.sensor_space_connectivity_runnable = None

        self.classify_runnable = None

        self.statistics_snr_runnable = None
        self.statistics_ersp_itc_runnable = None
        self.statistics_connectivity_runnable = None

        # Others
        self.fig_psd = None     # PSD figure, to plot them in the main thread to avoid matplotlib errors.
        self.fig_topo = None

        self.statistics_fig_psd_one = None
        self.statistics_fig_topo_one = None
        self.statistics_fig_psd_two = None
        self.statistics_fig_topo_two = None

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
        self.open_fif_file_runnable.signals.error.connect(self.open_fif_file_computation_error)

    def open_fif_file_computation_finished(self):
        """
        Retrieves the data from the runnable when the FIF file has been opened.
        Notifies the main controller that the reading is done.
        """
        self.file_data_tmp = self.open_fif_file_runnable.get_file_data()
        self.file_type_tmp = self.open_fif_file_runnable.get_file_type()
        self.file_path_name_tmp = self.open_fif_file_runnable.get_path_to_file()
        self.main_listener.open_fif_file_computation_finished()

    def open_fif_file_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.open_fif_file_computation_error()

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
        self.open_cnt_file_runnable.signals.error.connect(self.open_cnt_file_computation_error)

    def open_cnt_file_computation_finished(self):
        """
        Retrieves the data from the runnable when the CNT file has been opened.
        Notifies the main controller that the reading is done.
        """
        self.file_data_tmp = self.open_cnt_file_runnable.get_file_data()
        self.file_type_tmp = self.open_cnt_file_runnable.get_file_type()
        self.file_path_name_tmp = self.open_cnt_file_runnable.get_path_to_file()
        self.main_listener.open_cnt_file_computation_finished()

    def open_cnt_file_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.open_cnt_file_computation_error()

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
        self.open_set_file_runnable.signals.error.connect(self.open_set_file_computation_error)

    def open_set_file_computation_finished(self):
        """
        Retrieves the data from the runnable when the SET file has been opened.
        Notifies the main controller that the reading is done.
        """
        self.file_data_tmp = self.open_set_file_runnable.get_file_data()
        self.file_type_tmp = self.open_set_file_runnable.get_file_type()
        self.file_path_name_tmp = self.open_set_file_runnable.get_path_to_file()
        self.main_listener.open_set_file_computation_finished()

    def open_set_file_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.open_set_file_computation_error()

    # Data Info
    def load_data_info(self, montage, channels_selected, tmin, tmax, dataset_name):
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
        :param dataset_name: The name of the loaded dataset.
        :type dataset_name: str
        """
        self.dataset_name_tmp = dataset_name

        pool = QThreadPool.globalInstance()
        self.load_data_info_runnable = loadDataInfoRunnable(self.file_data_tmp, montage, channels_selected, tmin, tmax)
        pool.start(self.load_data_info_runnable)
        self.load_data_info_runnable.signals.finished.connect(self.load_data_info_computation_finished)

    def load_data_info_computation_finished(self):
        """
        Retrieves the data from the runnable when the last information have been updated.
        Notifies the main controller that the reading is done.
        """
        self.file_data.append(self.load_data_info_runnable.get_file_data())
        self.file_type.append(self.file_type_tmp)
        self.file_path_name.append(self.file_path_name_tmp)
        self.dataset_name.append(self.dataset_name_tmp)

        self.channels_locations.append({})
        self.ica_decomposition.append("No")
        self.references.append("Unknown")
        self.read_events.append(None)     # Events info read from file or channel, used to transform raw to epochs
        self.read_event_ids.append(None)

        self.current_dataset_index = len(self.file_data)-1

        self.reset_tmp_attributes()

        self.create_channels_locations()
        file_type = self.file_type[self.current_dataset_index]
        if file_type == "Raw":
            self.try_finding_events()

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
                self.read_events[self.current_dataset_index] = events
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
        file_data = self.file_data[self.current_dataset_index]

        pool = QThreadPool.globalInstance()
        self.find_events_from_channel_runnable = findEventsFromChannelRunnable(file_data, stim_channel)
        pool.start(self.find_events_from_channel_runnable)
        self.find_events_from_channel_runnable.signals.finished.connect(self.find_events_from_channel_computation_finished)
        self.find_events_from_channel_runnable.signals.error.connect(self.find_events_from_channel_computation_error)

    def find_events_from_channel_computation_finished(self):
        """
        Retrieves the data from the runnable when the events are found from the provided channel.
        Notifies the main controller that the computation is done.
        """
        self.read_events[self.current_dataset_index] = self.find_events_from_channel_runnable.get_read_events()
        self.read_event_ids[self.current_dataset_index] = self.find_events_from_channel_runnable.get_read_event_ids()
        if self.read_events[self.current_dataset_index] is not None:
            if len(self.read_events[self.current_dataset_index]) == 0:
                error_message = "It seems that the number of events found is 0, please check the channel used or use " \
                                "another method."
                error_window = errorWindow(error_message)
                error_window.show()
        self.main_listener.find_events_from_channel_computation_finished()

    def find_events_from_channel_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.find_events_from_channel_computation_error()

    # Export CSV
    def export_data_to_csv_file_clicked(self, path_to_file):
        """
        Check if the path to the file is correct.
        Export the data to a CSV file.
        :param path_to_file: Path to the file.
        :type path_to_file: str
        """
        file_data = self.file_data[self.current_dataset_index]

        pool = QThreadPool.globalInstance()
        self.export_data_csv_runnable = exportDataCSVRunnable(file_data, path_to_file)
        pool.start(self.export_data_csv_runnable)
        self.export_data_csv_runnable.signals.finished.connect(self.export_data_csv_computation_finished)
        self.export_data_csv_runnable.signals.error.connect(self.export_data_csv_computation_error)

    def export_data_csv_computation_finished(self):
        """
        Retrieves the data from the runnable when the data are exported into a CSV file.
        Notifies the main controller that the computation is done.
        """
        self.main_listener.export_data_csv_computation_finished()

    def export_data_csv_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.export_data_csv_computation_error()

    # Export SET
    def export_data_to_set_file_clicked(self, path_to_file):
        """
        Check if the path to the file is correct.
        Export the data to a SET file.
        :param path_to_file: Path to the file.
        :type path_to_file: str
        """
        file_data = self.file_data[self.current_dataset_index]

        pool = QThreadPool.globalInstance()
        self.export_data_set_runnable = exportDataSETRunnable(file_data, path_to_file)
        pool.start(self.export_data_set_runnable)
        self.export_data_set_runnable.signals.finished.connect(self.export_data_set_computation_finished)
        self.export_data_set_runnable.signals.error.connect(self.export_data_set_computation_error)

    def export_data_set_computation_finished(self):
        """
        Retrieves the data from the runnable when the data are exported into a SET file.
        Notifies the main controller that the computation is done.
        """
        self.main_listener.export_data_set_computation_finished()

    def export_data_set_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.export_data_set_computation_error()

    # Export events
    def export_events_to_file_clicked(self, path_to_file):
        """
        Check if the path to the file is correct.
        Export the events to a TXT file.
        :param path_to_file: Path to the file.
        :type path_to_file: str
        """
        file_data = self.file_data[self.current_dataset_index]

        pool = QThreadPool.globalInstance()
        self.export_events_txt_runnable = exportEventsTXTRunnable(file_data, path_to_file)
        pool.start(self.export_events_txt_runnable)
        self.export_events_txt_runnable.signals.finished.connect(self.export_events_txt_computation_finished)
        self.export_events_txt_runnable.signals.error.connect(self.export_events_txt_computation_error)

    def export_events_txt_computation_finished(self):
        """
        Retrieves the data from the runnable when the events are exported into a TXT file.
        Notifies the main controller that the computation is done.
        """
        self.main_listener.export_events_txt_computation_finished()

    def export_events_txt_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.export_events_txt_computation_error()

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
            self.file_data[self.current_dataset_index].save(path_to_file, overwrite=True)
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
            file_path_name = path_to_file + "-raw.fif"
        else:
            file_path_name = path_to_file + "-epo.fif"
        self.file_path_name[self.current_dataset_index] = file_path_name
        self.file_data[self.current_dataset_index].save(file_path_name)

    # Clear dataset
    def clear_current_dataset(self):
        """
        Clear the data of the removed dataset.
        """
        del self.file_data[self.current_dataset_index]
        del self.file_type[self.current_dataset_index]
        del self.file_path_name[self.current_dataset_index]
        del self.dataset_name[self.current_dataset_index]

        del self.channels_locations[self.current_dataset_index]
        del self.ica_decomposition[self.current_dataset_index]
        del self.references[self.current_dataset_index]
        del self.read_events[self.current_dataset_index]
        del self.read_event_ids[self.current_dataset_index]

        self.current_dataset_index = len(self.file_data) - 1

    def create_study(self, study_name, task_name, dataset_names, dataset_indexes, subjects, sessions, runs, conditions, groups):
        """
        Create the study with the given information.
        :param study_name: The name of the study
        :type study_name: str
        :param task_name: The name of the task linked to the study
        :type task_name: str
        :param dataset_names: The name of the datasets linked to the study
        :type dataset_names: list of str
        :param dataset_indexes: The indexes of the datasets selected to be in the study
        :type dataset_indexes: list of int
        :param subjects: The subjects assigned to each dataset in the study
        :type subjects: list of str
        :param sessions: The sessions assigned to each dataset in the study
        :type sessions: list of str
        :param runs: The runs assigned to each dataset in the study
        :type runs: list of str
        :param conditions: The conditions assigned to each dataset in the study
        :type conditions: list of str
        :param groups: The groups assigned to each dataset in the study
        :type groups: list of str
        """
        self.study = studyModel(study_name, task_name, dataset_names, dataset_indexes, subjects, sessions, runs, conditions, groups)
        self.study.set_listener(self)
        self.study_selected = True

    def clear_study(self):
        """
        Clear the current study.
        """
        self.study = None
        self.study_selected = False

    """
    Tools menu
    """
    # Filtering
    def filter(self, low_frequency, high_frequency, channels_selected, filter_method, index=None):
        """
        Creates the parallel runnable for filtering the dataset.
        :param low_frequency: Lowest frequency from where the data will be filtered.
        :type low_frequency: float
        :param high_frequency: Highest frequency from where the data will be filtered.
        :type high_frequency: float
        :param channels_selected: Channels on which the filtering will be performed.
        :type channels_selected: list of str
        :param filter_method: Method used for the filtering, either FIR or IIR.
        :type filter_method: str
        :param index: The index of the dataset of the study.
        :type index: int
        """
        if self.study_selected:
            self.study_index = index
            file_data = self.file_data[index]
        else:
            file_data = self.file_data[self.current_dataset_index]

        pool = QThreadPool.globalInstance()
        self.filter_runnable = filterRunnable(low_frequency, high_frequency, channels_selected, file_data, filter_method)
        pool.start(self.filter_runnable)
        self.filter_runnable.signals.finished.connect(self.filter_computation_finished)
        self.filter_runnable.signals.error.connect(self.filter_computation_error)

    def filter_computation_finished(self):
        """
        Retrieves the data from the runnable when the filtering is computed.
        Notifies the main controller that the computation is done.
        """
        if self.study_selected:
            self.file_data[self.study_index] = self.filter_runnable.get_file_data()
            low_frequency = self.filter_runnable.get_low_frequency()
            high_frequency = self.filter_runnable.get_high_frequency()
            channels_selected = self.filter_runnable.get_channels_selected()
            filter_method = self.filter_runnable.get_filter_method()
            self.main_listener.filter_computation_finished(low_frequency, high_frequency, channels_selected, filter_method)
        else:
            self.file_data[self.current_dataset_index] = self.filter_runnable.get_file_data()
            self.main_listener.filter_computation_finished()

    def filter_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.filter_computation_error()

    # Resampling
    def resampling(self, new_frequency, index=None):
        """
        Creates the parallel runnable for performing a resampling.
        :param new_frequency: The new frequency at which the data will be resampled.
        :type new_frequency: int
        :param index: The index of the dataset of the study.
        :type index: int
        """
        if self.study_selected:
            self.study_index = index
            file_data = self.file_data[index]
            events = self.get_event_values(index)
        else:
            file_data = self.file_data[self.current_dataset_index]
            events = self.get_event_values()

        pool = QThreadPool.globalInstance()
        self.resampling_runnable = resamplingRunnable(new_frequency, file_data, events)
        pool.start(self.resampling_runnable)
        self.resampling_runnable.signals.finished.connect(self.resampling_computation_finished)
        self.resampling_runnable.signals.error.connect(self.resampling_computation_error)

    def resampling_computation_finished(self):
        """
        Retrieves the data from the runnable when the resampling is computed.
        Notifies the main controller that the computation is done.
        """
        if self.study_selected:
            self.file_data[self.study_index] = self.resampling_runnable.get_file_data()
            self.set_event_values(self.resampling_runnable.get_events(), index=self.study_index)

            frequency = self.resampling_runnable.get_frequency()
            self.main_listener.resampling_computation_finished(frequency)
        else:
            self.file_data[self.current_dataset_index] = self.resampling_runnable.get_file_data()
            self.set_event_values(self.resampling_runnable.get_events())
            self.main_listener.resampling_computation_finished()

    def resampling_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.resampling_computation_error()

    # Re-referencing
    def re_referencing(self, references, save_data, load_data, n_jobs, index=None):
        """
        Creates the parallel runnable for performing a re-referencing.
        :param references: References from which the data will be re-referenced. Can be a single or multiple channels;
        Can be an average of all channels; Can be a "point to infinity".
        :type references: list of str; str
        :param save_data: Boolean telling if the data computed must be saved into files.
        :type save_data: bool
        :param load_data: Boolean telling if the data used for the computation can be read from computer files.
        :type load_data: bool
        :param n_jobs: Number of parallel processes used to compute the re-referencing
        :type n_jobs: int
        :param index: The index of the dataset of the study.
        :type index: int
        """
        if self.study_selected:
            self.study_index = index
            file_data = self.file_data[index]
            file_path_name_without_extension = self.get_file_path_name_without_extension(index)
        else:
            file_data = self.file_data[self.current_dataset_index]
            file_path_name_without_extension = self.get_file_path_name_without_extension()

        pool = QThreadPool.globalInstance()
        self.re_referencing_runnable = reReferencingRunnable(references, file_data, file_path_name_without_extension,
                                                             save_data, load_data, n_jobs)
        pool.start(self.re_referencing_runnable)
        self.re_referencing_runnable.signals.finished.connect(self.re_referencing_computation_finished)
        self.re_referencing_runnable.signals.error.connect(self.re_referencing_computation_error)

    def re_referencing_computation_finished(self):
        """
        Retrieves the data from the runnable when the re-referencing is computed.
        Notifies the main controller that the computation is done.
        """
        if self.study_selected:
            self.file_data[self.study_index] = self.re_referencing_runnable.get_file_data()
            self.references[self.study_index] = self.re_referencing_runnable.get_references()

            save_data = self.re_referencing_runnable.get_save_data()
            load_data = self.re_referencing_runnable.get_load_data()
            n_jobs = self.re_referencing_runnable.get_n_jobs()
            self.main_listener.re_referencing_computation_finished(self.references[self.study_index], save_data, load_data,
                                                                   n_jobs)
        else:
            self.file_data[self.current_dataset_index] = self.re_referencing_runnable.get_file_data()
            self.references[self.current_dataset_index] = self.re_referencing_runnable.get_references()
            self.main_listener.re_referencing_computation_finished()

    def re_referencing_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.re_referencing_computation_error()

    # ICA decomposition
    def ica_data_decomposition(self, ica_method, index=None):
        """
        Creates the parallel runnable for performing the ICA decomposition of the dataset.
        :param ica_method: Method used for performing the ICA decomposition
        :type ica_method: str
        :param index: The index of the dataset of the study.
        :type index: int
        """
        if self.study_selected:
            self.study_index = index
            file_data = self.file_data[index]
        else:
            file_data = self.file_data[self.current_dataset_index]

        pool = QThreadPool.globalInstance()
        self.ica_data_decomposition_runnable = icaRunnable(ica_method, file_data)
        pool.start(self.ica_data_decomposition_runnable)
        self.ica_data_decomposition_runnable.signals.finished.connect(self.ica_data_decomposition_computation_finished)
        self.ica_data_decomposition_runnable.signals.error.connect(self.ica_data_decomposition_computation_error)

    def ica_data_decomposition_computation_finished(self):
        """
        Retrieves the data from the runnable when the ICA decomposition is computed.
        Notifies the main controller that the computation is done.
        """
        if self.study_selected:
            self.file_data[self.study_index] = self.ica_data_decomposition_runnable.get_file_data()
            self.ica_decomposition[self.study_index] = "Yes"

            ica_method = self.ica_data_decomposition_runnable.get_ica_method()
            self.main_listener.ica_data_decomposition_computation_finished(ica_method)
        else:
            self.file_data[self.current_dataset_index] = self.ica_data_decomposition_runnable.get_file_data()
            self.ica_decomposition[self.current_dataset_index] = "Yes"
            self.main_listener.ica_data_decomposition_computation_finished()

    def ica_data_decomposition_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.ica_data_decomposition_computation_error()

    # Extract Epochs
    def extract_epochs(self, tmin, tmax, trials_selected):
        """
        Creates the parallel runnable for extracting the epochs of a dataset based on the events provided/or found beforehand.
        :param tmin: Start time of the epoch to keep
        :type tmin: float
        :param tmax: End time of the epoch to keep
        :type tmax: float
        :param trials_selected: The indexes of the trials selected for the computation
        :type trials_selected: list of int
        """
        file_data = self.file_data[self.current_dataset_index]
        read_events = self.read_events[self.current_dataset_index]
        read_event_ids = self.read_event_ids[self.current_dataset_index]

        pool = QThreadPool.globalInstance()
        self.extract_epochs_runnable = extractEpochsRunnable(file_data, read_events, read_event_ids, tmin, tmax,
                                                             trials_selected)
        pool.start(self.extract_epochs_runnable)
        self.extract_epochs_runnable.signals.finished.connect(self.extract_epochs_computation_finished)
        self.extract_epochs_runnable.signals.error.connect(self.extract_epochs_computation_error)

    def extract_epochs_computation_finished(self):
        """
        Retrieves the data from the runnable when the epochs are extracted from the available events.
        Notifies the main controller that the computation is done.
        """
        self.file_type[self.current_dataset_index] = "Epochs"
        self.file_data[self.current_dataset_index] = self.extract_epochs_runnable.get_file_data()
        self.main_listener.extract_epochs_computation_finished()

    def extract_epochs_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.extract_epochs_computation_error()

    # SNR
    def signal_to_noise_ratio(self, snr_methods, source_method, read, write, picks, trials_selected):
        """
        Creates the parallel runnable for computation of the SNR of a dataset.
        """
        file_data = self.file_data[self.current_dataset_index]
        file_path_name_without_extension = self.get_file_path_name_without_extension()

        pool = QThreadPool.globalInstance()
        self.snr_runnable = signalToNoiseRatioRunnable(file_data, snr_methods, source_method, file_path_name_without_extension,
                                                       read, write, picks, trials_selected)
        pool.start(self.snr_runnable)
        self.snr_runnable.signals.finished.connect(self.snr_computation_finished)
        self.snr_runnable.signals.error.connect(self.snr_computation_error)

    def snr_computation_finished(self):
        """
        Retrieves the data from the runnable when the SNR is computed.
        Notifies the main controller that the computation is done.
        """
        self.main_listener.snr_computation_finished()

    def snr_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.snr_computation_error()

    # Source Estimation
    def source_estimation(self, source_estimation_method, save_data, load_data, epochs_method, trials_selected, tmin, tmax,
                          n_jobs, export_path):
        """
        Creates the parallel runnable for computing the source estimation of the data.
        :param source_estimation_method: The method used to compute the source estimation
        :type source_estimation_method: str
        :param save_data: Boolean telling if the data computed must be saved into files.
        :type save_data: bool
        :param load_data: Boolean telling if the data used for the computation can be read from computer files.
        :type load_data: bool
        :param epochs_method: On what data the source estimation will be computed. Can be three values :
        - "single trial" : Compute the source estimation on a single trial that is precised.
        - "evoked" : Compute the source estimation on the average of all the signals.
        - "averaged" : Compute the source estimation on every trial, and then compute the average of them.
        :type: str
        :param trials_selected: The indexes of the trials selected for the computation
        :type trials_selected: list of int
        :param tmin: Start time of the epoch or raw file
        :type tmin: float
        :param tmax: End time of the epoch or raw file
        :type tmax: float
        :param n_jobs: Number of processes used to compute the source estimation
        :type n_jobs: int
        :param export_path: Path where the source estimation data will be stored.
        :type export_path: str
        """
        file_data = self.file_data[self.current_dataset_index]
        file_path_name_without_extension = self.get_file_path_name_without_extension()

        pool = QThreadPool.globalInstance()
        self.source_estimation_runnable = sourceEstimationRunnable(source_estimation_method, file_data,
                                                                   file_path_name_without_extension,
                                                                   save_data, load_data, epochs_method, trials_selected,
                                                                   tmin, tmax, n_jobs, export_path)
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
    # PSD
    def power_spectral_density(self, minimum_frequency, maximum_frequency, minimum_time, maximum_time, topo_time_points):
        """
        Creates the parallel runnable for computing the power spectral density.
        :param minimum_frequency: Minimum frequency from which the power spectral density will be computed.
        :type minimum_frequency: float
        :param maximum_frequency: Maximum frequency from which the power spectral density will be computed.
        :type maximum_frequency: float
        :param minimum_time: Minimum time of the epochs from which the power spectral density will be computed.
        :type minimum_time: float
        :param maximum_time: Maximum time of the epochs from which the power spectral density will be computed.
        :type maximum_time: float
        :param topo_time_points: The time points for the topomaps.
        :type topo_time_points: list of float
        """
        file_data = self.file_data[self.current_dataset_index]
        try:
            bandwidth = 1.0/(maximum_time-minimum_time)     # To counter bandwidth normalization
            self.fig_psd = file_data.plot_psd(fmin=minimum_frequency, fmax=maximum_frequency, tmin=minimum_time,
                                              tmax=maximum_time, estimate="power", bandwidth=bandwidth,
                                              average=False, show=False)
            bands = []
            for time in topo_time_points:
                bands.append((time, str(time) + " Hz"))
            self.fig_topo = file_data.plot_psd_topomap(bands=bands, tmin=minimum_time, tmax=maximum_time, show=False)
            self.power_spectral_density_computation_finished()
        except Exception as error:
            error_message = "An error has occurred during the computation of the PSD"
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.power_spectral_density_computation_error()

        """
        pool = QThreadPool.globalInstance()
        self.power_spectral_density_runnable = powerSpectralDensityRunnable(self.file_data, minimum_frequency, maximum_frequency,
                                                                            minimum_time, maximum_time, topo_time_points)
        pool.start(self.power_spectral_density_runnable)
        self.power_spectral_density_runnable.signals.finished.connect(self.power_spectral_density_computation_finished)
        self.power_spectral_density_runnable.signals.error.connect(self.power_spectral_density_computation_error)
        """

    def power_spectral_density_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.main_listener.plot_spectra_maps_computation_finished()

    def power_spectral_density_computation_error(self):
        """
        Notifies the main controller that an error has occurred during the computation
        """
        self.main_listener.plot_spectra_maps_computation_error()

    # Time frequency
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
        file_data = self.file_data[self.current_dataset_index]

        pool = QThreadPool.globalInstance()
        self.time_frequency_runnable = timeFrequencyRunnable(file_data, method_tfr, channel_selected,
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
    # Envelope correlation
    def envelope_correlation(self, psi, fmin, fmax, connectivity_method, n_jobs, export_path):
        """
        Creates the parallel runnable for computing the envelope correlation between the channels of the dataset.
        :param psi: Check if the computation of the Phase Slope Index must be done. The PSI give an indication to the
        directionality of the connectivity.
        :type psi: bool
        :param fmin: Minimum frequency from which the envelope correlation will be computed.
        :type fmin: float
        :param fmax: Maximum frequency from which the envelope correlation will be computed.
        :type fmax: float
        :param connectivity_method: Method used for computing the source space connectivity.
        :type connectivity_method: str
        :param n_jobs: Number of processes used to compute the source estimation
        :type n_jobs: int
        :param export_path: Path where the envelope correlation data will be stored.
        :type export_path: str
        """
        file_data = self.file_data[self.current_dataset_index]

        pool = QThreadPool.globalInstance()
        self.envelope_correlation_runnable = envelopeCorrelationRunnable(file_data, psi, fmin, fmax, connectivity_method,
                                                                         n_jobs, export_path)
        pool.start(self.envelope_correlation_runnable)
        self.envelope_correlation_runnable.signals.finished.connect(self.envelope_correlation_computation_finished)
        self.envelope_correlation_runnable.signals.error.connect(self.envelope_correlation_computation_error)

    def envelope_correlation_computation_finished(self):
        """
        Notifies the main controller that the computation of the envelope correlation is done.
        """
        self.main_listener.envelope_correlation_computation_finished()

    def envelope_correlation_computation_error(self):
        """
        Notifies the main controller that an error has occurred during the computation
        """
        self.main_listener.envelope_correlation_computation_error()

    # Source space connectivity
    def source_space_connectivity(self, connectivity_method, spectrum_estimation_method, source_estimation_method, save_data,
                                  load_data, n_jobs, export_path, psi, fmin, fmax):
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
        :param export_path: Path where the source space connectivity data will be stored.
        :type export_path: str
        :param psi: Check if the computation of the Phase Slope Index must be done. The PSI give an indication to the
        directionality of the connectivity.
        :type psi: bool
        :param fmin: Minimum frequency from which the envelope correlation will be computed.
        :type fmin: float
        :param fmax: Maximum frequency from which the envelope correlation will be computed.
        :type fmax: float
        """
        file_data = self.file_data[self.current_dataset_index]
        file_path_name_without_extension = self.get_file_path_name_without_extension()

        pool = QThreadPool.globalInstance()
        self.source_space_connectivity_runnable = sourceSpaceConnectivityRunnable(file_data, file_path_name_without_extension,
                                                                                  connectivity_method, spectrum_estimation_method,
                                                                                  source_estimation_method, save_data, load_data,
                                                                                  n_jobs, export_path, psi, fmin, fmax)
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

    # Sensor space connectivity
    def sensor_space_connectivity(self, export_path):
        """
        Creates the parallel runnable for computing the connectivity of the sensor space of the dataset.
        :param export_path: Path where the sensor space connectivity data will be stored.
        :type export_path: str
        """
        file_data = self.file_data[self.current_dataset_index]

        pool = QThreadPool.globalInstance()
        self.sensor_space_connectivity_runnable = sensorSpaceConnectivityRunnable(file_data, export_path)
        pool.start(self.sensor_space_connectivity_runnable)
        self.sensor_space_connectivity_runnable.signals.finished.connect(self.sensor_space_connectivity_computation_finished)
        self.sensor_space_connectivity_runnable.signals.error.connect(self.sensor_space_connectivity_computation_error)

    def sensor_space_connectivity_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.main_listener.sensor_space_connectivity_computation_finished()

    def sensor_space_connectivity_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.sensor_space_connectivity_computation_error()

    """
    Classification menu
    """
    def classify(self, pipeline_selected, feature_selection, number_of_channels_to_select, hyper_tuning, cross_val_number,
                 trials_selected):
        """
        Creates the parallel runnable for computing the classification with pipeline(s) of artificial intelligence of
        the dataset.
        :param pipeline_selected: The pipeline(s) used for the classification of the dataset.
        :type pipeline_selected: list of str
        :param feature_selection: Boolean telling if the computation of some feature selection techniques must be performed
        on the dataset.
        :type feature_selection: boolean
        :param number_of_channels_to_select: Number of channels to select for the feature selection.
        :type number_of_channels_to_select: int
        :param hyper_tuning: Boolean telling if the computation of the tuning of the hyper-parameters of the pipelines must
        be performed on the dataset.
        :type hyper_tuning: boolean
        :param cross_val_number: Number of cross-validation fold used by the pipelines on the dataset.
        :type cross_val_number: int
        :param trials_selected: The indexes of the trials selected for the computation
        :type trials_selected: list of int
        """
        file_data = self.file_data[self.current_dataset_index]
        directory_path = self.get_directory_path_from_file_path()

        pool = QThreadPool.globalInstance()
        self.classify_runnable = classifyRunnable(file_data, directory_path, pipeline_selected, feature_selection,
                                                  number_of_channels_to_select, hyper_tuning, cross_val_number, trials_selected)
        pool.start(self.classify_runnable)
        self.classify_runnable.signals.finished.connect(self.classify_computation_finished)
        self.classify_runnable.signals.error.connect(self.classify_computation_error)

    def classify_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.main_listener.classify_computation_finished()

    def classify_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.classify_computation_error()

    """
    Statistics Menu
    """
    # SNR
    def statistics_snr(self, snr_methods, source_method, read, write, picks, stats_first_variable, stats_second_variable):
        """
        Creates the parallel runnable for computing the SNR and statistics on it.
        :param snr_methods: The methods used for computing the SNR
        :type snr_methods: list of str
        :param source_method: The method used for computing the source estimation
        :type source_method: str
        :param read: Boolean telling if the data used for the computation can be read from computer files.
        :type read: bool
        :param write: Boolean telling if the data computed must be saved into files.
        :type write: bool
        :param picks: The list of channels selected used for the computation
        :type picks: list of str
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        file_data = self.file_data[self.current_dataset_index]
        file_path_name_without_extension = self.get_file_path_name_without_extension()

        pool = QThreadPool.globalInstance()
        self.statistics_snr_runnable = statisticsSnrRunnable(file_data, snr_methods, source_method, file_path_name_without_extension,
                                                             read, write, picks, stats_first_variable, stats_second_variable)
        pool.start(self.statistics_snr_runnable)
        self.statistics_snr_runnable.signals.finished.connect(self.statistics_snr_computation_finished)
        self.statistics_snr_runnable.signals.error.connect(self.statistics_snr_computation_error)

    def statistics_snr_computation_finished(self):
        """
        Retrieves the data from the runnable when the SNR and the statistics is computed.
        Notifies the main controller that the computation is done.
        """
        self.main_listener.statistics_snr_computation_finished()

    def statistics_snr_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.statistics_snr_computation_error()

    # PSD
    def statistics_psd(self, minimum_frequency, maximum_frequency, minimum_time, maximum_time, topo_time_points,
                       channel_selected, stats_first_variable, stats_second_variable):
        """
        Creates the parallel runnable for computing the power spectral density.
        :param minimum_frequency: Minimum frequency from which the power spectral density will be computed.
        :type minimum_frequency: float
        :param maximum_frequency: Maximum frequency from which the power spectral density will be computed.
        :type maximum_frequency: float
        :param minimum_time: Minimum time of the epochs from which the power spectral density will be computed.
        :type minimum_time: float
        :param maximum_time: Maximum time of the epochs from which the power spectral density will be computed.
        :type maximum_time: float
        :param topo_time_points: The time points for the topomaps.
        :type topo_time_points: list of float
        :param channel_selected: Channel selected for the ERP.
        :type channel_selected: str
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        file_data = self.file_data[self.current_dataset_index]
        try:
            # Initialize variables
            bandwidth = 1.0 / (maximum_time - minimum_time)  # To counter bandwidth normalization
            bands = []
            for time in topo_time_points:
                bands.append((time, str(time) + " Hz"))
            # First variable
            file_data_one = deepcopy(file_data)
            mask = self.create_mask_from_variable_to_keep(file_data_one, stats_first_variable)
            file_data_one = file_data_one.drop(mask)
            self.statistics_fig_psd_one = file_data_one.plot_psd(fmin=minimum_frequency, fmax=maximum_frequency, tmin=minimum_time,
                                                                 tmax=maximum_time, estimate="power", bandwidth=bandwidth,
                                                                 average=False, show=False, picks=channel_selected)
            self.statistics_fig_topo_one = file_data_one.plot_psd_topomap(bands=bands, tmin=minimum_time, tmax=maximum_time,
                                                                          show=False)
            # Second variable
            file_data_two = deepcopy(file_data)
            mask = self.create_mask_from_variable_to_keep(file_data_two, stats_second_variable)
            file_data_two = file_data_two.drop(mask)
            self.statistics_fig_psd_two = file_data_two.plot_psd(fmin=minimum_frequency, fmax=maximum_frequency, tmin=minimum_time,
                                                                 tmax=maximum_time, estimate="power", bandwidth=bandwidth,
                                                                 average=False, show=False, picks=channel_selected)
            self.statistics_fig_topo_two = file_data_two.plot_psd_topomap(bands=bands, tmin=minimum_time, tmax=maximum_time,
                                                                          show=False)
            self.statistics_psd_computation_finished()
        except Exception as error:
            error_message = "An error has occurred during the computation of the PSD"
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.statistics_psd_computation_error()

    def statistics_psd_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.main_listener.statistics_psd_computation_finished()

    def statistics_psd_computation_error(self):
        """
        Notifies the main controller that an error has occurred during the computation
        """
        self.main_listener.statistics_psd_computation_error()

    # ERSP-ITC
    def statistics_ersp_itc(self, method_tfr, channel_selected, min_frequency, max_frequency, n_cycles, stats_first_variable,
                            stats_second_variable):
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
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        file_data = self.file_data[self.current_dataset_index]

        pool = QThreadPool.globalInstance()
        self.statistics_ersp_itc_runnable = statisticsErspItcRunnable(file_data, method_tfr, channel_selected, min_frequency,
                                                                      max_frequency, n_cycles, stats_first_variable,
                                                                      stats_second_variable)
        pool.start(self.statistics_ersp_itc_runnable)
        self.statistics_ersp_itc_runnable.signals.finished.connect(self.statistics_ersp_itc_computation_finished)
        self.statistics_ersp_itc_runnable.signals.error.connect(self.statistics_ersp_itc_computation_error)

    def statistics_ersp_itc_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.main_listener.statistics_ersp_itc_computation_finished()

    def statistics_ersp_itc_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.main_listener.statistics_ersp_itc_computation_error()

    # Connectivity
    def statistics_connectivity(self, psi, fmin, fmax, connectivity_method, n_jobs, export_path, stats_first_variable,
                                stats_second_variable):
        """
        Creates the parallel runnable for computing the envelope correlation between the channels of the dataset.
        :param psi: Check if the computation of the Phase Slope Index must be done. The PSI give an indication to the
        directionality of the connectivity.
        :type psi: bool
        :param fmin: Minimum frequency from which the envelope correlation will be computed.
        :type fmin: float
        :param fmax: Maximum frequency from which the envelope correlation will be computed.
        :type fmax: float
        :param connectivity_method: Method used for computing the source space connectivity.
        :type connectivity_method: str
        :param n_jobs: Number of processes used to compute the source estimation
        :type n_jobs: int
        :param export_path: Path where the envelope correlation data will be stored.
        :type export_path: str
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        file_data = self.file_data[self.current_dataset_index]

        pool = QThreadPool.globalInstance()
        self.statistics_connectivity_runnable = statisticsConnectivityRunnable(file_data, psi, fmin, fmax, connectivity_method,
                                                                               n_jobs, export_path, stats_first_variable,
                                                                               stats_second_variable)
        pool.start(self.statistics_connectivity_runnable)
        self.statistics_connectivity_runnable.signals.finished.connect(self.statistics_connectivity_computation_finished)
        self.statistics_connectivity_runnable.signals.error.connect(self.statistics_connectivity_computation_error)

    def statistics_connectivity_computation_finished(self):
        """
        Notifies the main controller that the computation of the envelope correlation is done.
        """
        self.main_listener.statistics_connectivity_computation_finished()

    def statistics_connectivity_computation_error(self):
        """
        Notifies the main controller that an error has occurred during the computation
        """
        self.main_listener.statistics_connectivity_computation_error()

    """
    Study Menu
    """
    def edit_study_information(self, study_name, task_name, subjects, sessions, runs, conditions, groups):
        """
        Send the information to the study to be edited.
        :param study_name: The name of the study
        :type study_name: str
        :param task_name: The name of the task linked to the study
        :type task_name: str
        :param subjects: The subjects assigned to each dataset in the study
        :type subjects: list of str
        :param sessions: The sessions assigned to each dataset in the study
        :type sessions: list of str
        :param runs: The runs assigned to each dataset in the study
        :type runs: list of str
        :param conditions: The conditions assigned to each dataset in the study
        :type conditions: list of str
        :param groups: The groups assigned to each dataset in the study
        :type groups: list of str
        """
        self.study.set_study_name(study_name)
        self.study.set_task_name(task_name)
        self.study.set_subjects(subjects)
        self.study.set_sessions(sessions)
        self.study.set_runs(runs)
        self.study.set_conditions(conditions)
        self.study.set_groups(groups)

    """
    Others
    """
    def is_fif_file(self):
        """
        Check if the dataset loaded is loaded from a FIF file.
        :return: True if the file used is a FIF file, False otherwise.
        :rtype: boolean
        """
        file_path_name = self.file_path_name[self.current_dataset_index]
        return file_path_name[-3:] == "fif"

    def create_channels_locations(self):
        """
        Retrieves the location of all channels from the MNE "Epochs" or "Raw" object for an easier use.
        Store the information inside the "self.channels_locations" attribute.
        """
        file_data = self.file_data[self.current_dataset_index]
        channels_locations = self.channels_locations[self.current_dataset_index]

        channels_info = file_data.info.get("chs")
        for channel in channels_info:
            channels_locations[channel["ch_name"]] = channel["loc"][:3]

        self.channels_locations[self.current_dataset_index] = channels_locations

    def try_finding_events(self):
        """
        Try to find the events if a raw file as been loaded.
        """
        file_data = self.file_data[self.current_dataset_index]

        read_ok = False
        try:
            read_events = find_events(file_data)
            self.read_events[self.current_dataset_index] = read_events
            read_ok = True
        except Exception as e:
            print(e)
            print(type(e))
        if not read_ok:
            try:
                read_events, read_event_ids = events_from_annotations(file_data)
                self.read_events[self.current_dataset_index] = read_events
                self.read_event_ids[self.current_dataset_index] = read_event_ids
            except Exception as e:
                print(e)
                print(type(e))

    @staticmethod
    def create_mask_from_variable_to_keep(file_data, stats_variable):
        """
        Create a mask to know which trial to keep and which one to remove for the computation.
        :return mask: Mask of trials to remove. True means remove, and False means keep.
        :rtype mask: list of boolean
        """
        mask = [True for _ in range(len(file_data.events))]
        event_ids = file_data.event_id
        event_id_to_keep = event_ids[stats_variable]
        for i, event in enumerate(file_data.events):
            if event[2] == event_id_to_keep:        # 2 is the event id in the events
                mask[i] = False
        return mask

    def reset_tmp_attributes(self):
        """
        Resets the temporary variable when a new dataset is completely loaded.
        """
        self.file_data_tmp = None
        self.file_type_tmp = None
        self.file_path_name_tmp = None
        self.dataset_name_tmp = None

    """
    Getters
    """
    def get_all_displayed_info(self):
        """
        Gets all the information of the dataset that will be displayed on the main window.
        :return: A list of all the displayed information.
        :rtype: list of str/float/int
        """
        all_info = [self.get_dataset_name(), self.get_file_path_name(), self.get_file_type(), self.get_number_of_channels(),
                    self.get_sampling_frequency(), self.get_number_of_events(), self.get_number_of_epochs(),
                    self.get_epochs_start(), self.get_epochs_end(), self.get_number_of_frames(),
                    self.get_reference(), self.get_channels_locations_status(), self.get_ica(), self.get_dataset_size()]
        return all_info

    def get_dataset_name(self):
        """
        Gets the dataset name of the dataset.
        :return: The dataset name
        :rtype: str
        """
        dataset_name = self.dataset_name[self.current_dataset_index]
        return dataset_name

    def get_all_dataset_names(self):
        """
        Gets the dataset name of all the datasets.
        :return: The dataset names
        :rtype: list of str
        """
        return self.dataset_name

    def get_file_path_name(self):
        """
        Gets the file path of the dataset.
        :return: The file path of the dataset
        :rtype: str
        """
        file_path_name = self.file_path_name[self.current_dataset_index]
        return file_path_name

    def get_all_file_path_name(self):
        """
        Gets the file path of all the datasets.
        :return: The file path of all the datasets
        :rtype: list of str
        """
        return self.file_path_name

    def get_file_path_name_without_extension(self, index=None):
        """
        Gets the file path of the dataset without the extension of the file.
        :param index: The index of the dataset to get the event from. If None, the current dataset index will be taken.
        :type index: int
        :return: The file path of the dataset without the extension.
        :rtype: str
        """
        if index is None:
            index = self.current_dataset_index
        file_path_name = self.file_path_name[index]
        return splitext(file_path_name)[0]

    def get_directory_path_from_file_path(self):
        """
        Gets the directory path of the dataset.
        :return: The directory path of the dataset.
        :rtype: str
        """
        file_path_name = self.file_path_name[self.current_dataset_index]
        return get_directory_path_from_file_path(file_path_name)

    def get_file_type(self):
        """
        Gets the type of the file.
        :return: The type of the file.
        :rtype: str
        """
        file_type = self.file_type[self.current_dataset_index]
        return file_type

    def get_all_file_type(self):
        """
        Gets the type of all the files.
        :return: The type of all the files.
        :rtype: list of str
        """
        return self.file_type

    def get_number_of_channels(self):
        """
        Gets the number of channels that are present in the dataset.
        :return: The number of channels
        :rtype: int
        """
        file_data = self.file_data[self.current_dataset_index]
        return len(file_data.ch_names)

    def get_sampling_frequency(self):
        """
        Gets the sampling frequency of the dataset.
        :return: The sampling frequency.
        :rtype: float
        """
        file_data = self.file_data[self.current_dataset_index]
        return file_data.info.get("sfreq")

    def get_number_of_events(self):
        """
        Gets the number of events present in the dataset.
        :return: The number of events. None for "Raw" type of dataset.
        :rtype: int/None
        """
        file_data = self.file_data[self.current_dataset_index]
        file_type = self.file_type[self.current_dataset_index]
        read_events = self.read_events[self.current_dataset_index]

        if file_type == "Raw":
            if read_events is None:
                return read_events
            else:
                return len(read_events)
        else:
            return len(file_data.events)

    def get_event_values(self, index=None):
        """
        Gets the events' information present in the dataset.
        :param index: The index of the dataset to get the event from. If None, the current dataset index will be taken.
        :type index: int
        :return: The events' information. Each event is represented by a list of 3 elements: First the latency time of
        the event; Second a "0" for MNE backwards compatibility; Third the event id.
        :rtype: list of, list of int
        """
        if index is None:
            index = self.current_dataset_index
        file_data = self.file_data[index]
        file_type = self.file_type[index]
        read_events = self.read_events[index]

        if file_type == "Raw":
            return read_events
        elif file_type == "Epochs":
            return file_data.events

    def get_event_ids(self):
        """
        Gets the event ids present in the dataset.
        :return: The events' ids
        :rtype: dict
        """
        file_data = self.file_data[self.current_dataset_index]
        file_type = self.file_type[self.current_dataset_index]
        read_event_ids = self.read_event_ids[self.current_dataset_index]

        if file_type == "Raw":
            return read_event_ids
        elif file_type == "Epochs":
            return file_data.event_id

    def get_number_of_epochs(self):
        """
        Gets the number of epochs present in the dataset.
        :return: The number of epochs. 1 for "Raw" type of dataset.
        :rtype: int
        """
        file_data = self.file_data[self.current_dataset_index]
        file_type = self.file_type[self.current_dataset_index]

        if file_type == "Raw":
            return 1
        else:
            return len(file_data)

    def get_epochs_start(self):
        """
        Gets the start time of the epochs of the dataset.
        :return: The start time of the epochs.
        :rtype: float
        """
        file_data = self.file_data[self.current_dataset_index]
        return round(file_data.times[0], 3)

    def get_epochs_end(self):
        """
        Gets the end time of the epochs of the dataset.
        :return: The end time of the epochs.
        :rtype: float
        """
        file_data = self.file_data[self.current_dataset_index]
        return round(file_data.times[-1], 3)

    def get_number_of_frames(self):
        """
        Gets the number of frames of the dataset. The number of frames depend from the start and end times of the epochs
        and the sampling frequency.
        :return: The number of frames.
        :rtype: int
        """
        file_data = self.file_data[self.current_dataset_index]
        return len(file_data.times)

    def get_reference(self):
        """
        Gets the references from which the dataset is based.
        :return: The references.
        :rtype: list of str/str
        """
        references = self.references[self.current_dataset_index]
        return references

    def get_channels_locations_status(self):
        """
        Gets the status of the channels' locations of the dataset.
        :return: "Unknown" if the channels' locations dict is empty. "Available" otherwise.
        :rtype: str
        """
        channels_locations = self.channels_locations[self.current_dataset_index]
        if not channels_locations:     # channels_locations dictionary is empty.
            return "Unknown"
        else:
            return "Available"

    def get_channels_locations(self):
        """
        Gets the channels' locations of the dataset.
        :return: The channels' locations.
        :rtype: dict
        """
        channels_locations = self.channels_locations[self.current_dataset_index]
        return channels_locations

    def get_ica(self):
        """
        Gets the status of the ICA decomposition of the dataset.
        :return: "Yes" if it is known by the software that the ICA decomposition has been performed. "No" otherwise.
        :rtype: str
        """
        ica_decomposition = self.ica_decomposition[self.current_dataset_index]
        return ica_decomposition

    def get_all_ica(self):
        """
        Gets the status of the ICA decomposition of all the datasets.
        :return: "Yes" if it is known by the software that the ICA decomposition has been performed. "No" otherwise.
        :rtype: list of str
        """
        return self.ica_decomposition

    def get_dataset_size(self):
        """
        Gets the size in megabits of the dataset.
        :return: The size of the dataset.
        :rtype: float
        """
        file_path_name = self.file_path_name[self.current_dataset_index]
        try:
            return round(getsize(file_path_name[:-3] + "fdt") / (1024 ** 2), 3)
        except:
            return round(getsize(file_path_name) / (1024 ** 2), 3)

    def get_all_channels_names(self):
        """
        Gets all the channels' names of the dataset.
        :return: The channels' names.
        :rtype: list of str
        """
        file_data = self.file_data[self.current_dataset_index]
        return file_data.ch_names

    def get_file_data(self):
        """
        Gets the MNE "Epochs" or "Raw" data of the dataset.
        :return: The MNE "Epochs" or "Raw" object.
        :rtype: Epochs/Raw
        """
        file_data = self.file_data[self.current_dataset_index]
        return file_data

    def get_all_file_data(self):
        """
        Gets the MNE "Epochs" or "Raw" data of all the datasets.
        :return: The MNE "Epochs" or "Raw" objects.
        :rtype: list of Epochs/Raw
        """
        return self.file_data

    def get_read_events(self):
        """
        Gets the read events obtained after the epochs' importation.
        :return: The read events.
        :rtype: list of int
        """
        read_events = self.read_events[self.current_dataset_index]
        return read_events

    def get_current_dataset_index(self):
        """
        Gets the current dataset index.
        :return: The current dataset index.
        :rtype: int
        """
        return self.current_dataset_index

    def get_all_study_displayed_info(self):
        """
        Gets all the information of the study that will be displayed on the main window.
        :return: A list of all the displayed information.
        :rtype: list of str/float/int
        """
        return self.study.get_displayed_info()

    def get_study(self):
        """
        Gets the study of the datasets selected.
        :return: The current study
        :rtype: studyModel
        """
        return self.study

    def get_study_selected(self):
        """
        Gets the state of the study
        :return: True if the study is selected, False otherwise.
        :rtype: bool
        """
        return self.study_selected

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
    def get_SNRs(self):
        """
        Get the SNR values computed over the data.
        :return: SNR
        :rtype: list of, list of float
        """
        return self.snr_runnable.get_SNRs()

    def get_SNR_methods(self):
        """
        Get the SNR methods used for the computation.
        :return: SNR methods
        :rtype: list of str
        """
        return self.snr_runnable.get_SNR_methods()

    def get_source_estimation_data(self):
        """
        Gets the data of the source estimation computation performed on the dataset.
        :return: The source estimation's data.
        :rtype: MNE.SourceEstimation
        """
        return self.source_estimation_runnable.get_source_estimation_data()

    def get_psd_fig(self):
        """
        Get the power spectral density's figure
        :return: The figure of the actual power spectral density's data computed
        :rtype: matplotlib.Figure
        """
        return self.fig_topo
        # return self.power_spectral_density_runnable.get_psd_fig()

    def get_psd_topo_fig(self):
        """
        Get the power spectral density's figure fo the topographies
        :return: The figure of the topographies of the actual power spectral density's data computed
        :rtype: matplotlib.Figure
        """
        return self.fig_psd
        # return self.power_spectral_density_runnable.get_topo_fig()

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

    def get_psi_data_envelope_correlation(self):
        """
        Get the psi's data for the envelope correlation.
        :return: The psi's data. Or nothing if the psi's data has not been computed.
        :rtype: list of, list of float
        """
        return self.envelope_correlation_runnable.get_psi_data()

    def get_source_space_connectivity_data(self):
        """
        Gets the data of the source space connectivity computation performed on the dataset.
        :return: The source space's data.
        :rtype: list of, list of float
        """
        return self.source_space_connectivity_runnable.get_source_space_connectivity_data()

    def get_psi_data_source_space(self):
        """
        Get the psi's data for the source space connectivity.
        :return: The psi's data. Or nothing if the psi's data has not been computed.
        :rtype: list of, list of float
        """
        return self.source_space_connectivity_runnable.get_psi_data()

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

    # Statistics SNR
    def get_statistics_first_SNRs(self):
        """
        Get the SNRs computed over the first independent variable.
        :return: The SNRs computed over the first independent variable.
        :rtype: list of, list of float
        """
        return self.statistics_snr_runnable.get_first_SNRs()

    def get_statistics_second_SNRs(self):
        """
        Get the SNRs computed over the second independent variable.
        :return: The SNRs computed over the second independent variable.
        :rtype: list of, list of float
        """
        return self.statistics_snr_runnable.get_second_SNRs()

    def get_statistics_SNR_t_values(self):
        """
        Get the T-values computed over the SNRs of the two independent variables.
        :return: T-values computed over the SNRs of the two independent variables.
        :rtype: list of float
        """
        return self.statistics_snr_runnable.get_t_values()

    def get_statistics_SNR_methods(self):
        """
        Get the SNR methods used for the computation.
        :return: SNR methods
        :rtype: list of str
        """
        return self.statistics_snr_runnable.get_SNR_methods()

    # Statistics PSD
    def get_statistics_psd_fig_one(self):
        """
        Get the power spectral density's figure of the first independent variable
        :return: The figure of the actual power spectral density's data computed
        :rtype: matplotlib.Figure
        """
        return self.statistics_fig_psd_one

    def get_statistics_psd_topo_fig_one(self):
        """
        Get the power spectral density's figure of the topographies of the first independent variable
        :return: The figure of the topographies of the actual power spectral density's data computed
        :rtype: matplotlib.Figure
        """
        return self.statistics_fig_topo_one

    def get_statistics_psd_fig_two(self):
        """
        Get the power spectral density's figure of the second independent variable
        :return: The figure of the actual power spectral density's data computed
        :rtype: matplotlib.Figure
        """
        return self.statistics_fig_psd_two

    def get_statistics_psd_topo_fig_two(self):
        """
        Get the power spectral density's figure of the topographies of the second independent variable
        :return: The figure of the topographies of the actual power spectral density's data computed
        :rtype: matplotlib.Figure
        """
        return self.statistics_fig_topo_two

    # Statistics ERSP ITC
    def get_statistics_ersp_itc_channel_selected(self):
        """
        Gets the channel used for the computation of the time-frequency analysis performed on the dataset.
        :return: The channel used for the time-frequency analysis computation.
        :rtype: list of str
        """
        return self.statistics_ersp_itc_runnable.get_channel_selected()

    def get_statistics_power_one(self):
        """
        Gets the "power" data of the time-frequency analysis computation performed on the dataset of the first independent variable.
        :return: "power" data of the time-frequency analysis computation.
        :rtype: MNE.AverageTFR
        """
        return self.statistics_ersp_itc_runnable.get_power_one()

    def get_statistics_itc_one(self):
        """
        Gets the "itc" data of the time-frequency analysis computation performed on the dataset of the first independent variable.
        :return: "itc" data of the time-frequency analysis computation.
        :rtype: MNE.AverageTFR
        """
        return self.statistics_ersp_itc_runnable.get_itc_one()

    def get_statistics_power_two(self):
        """
        Gets the "power" data of the time-frequency analysis computation performed on the dataset of the second independent variable.
        :return: "power" data of the time-frequency analysis computation.
        :rtype: MNE.AverageTFR
        """
        return self.statistics_ersp_itc_runnable.get_power_two()

    def get_statistics_itc_two(self):
        """
        Gets the "itc" data of the time-frequency analysis computation performed on the dataset of the second independent variable.
        :return: "itc" data of the time-frequency analysis computation.
        :rtype: MNE.AverageTFR
        """
        return self.statistics_ersp_itc_runnable.get_itc_two()

    # Statistics Connectivity
    def get_statistics_connectivity_data_one(self):
        """
        Gets the data of the envelope correlation computation performed on the dataset of the first independent variable.
        :return: The envelope correlation's data.
        :rtype: list of, list of float
        """
        return self.statistics_connectivity_runnable.get_connectivity_data_one()

    def get_statistics_connectivity_data_two(self):
        """
        Gets the data of the envelope correlation computation performed on the dataset of the second independent variable.
        :return: The envelope correlation's data.
        :rtype: list of, list of float
        """
        return self.statistics_connectivity_runnable.get_connectivity_data_two()

    def get_statistics_psi_data_one(self):
        """
        Get the psi's data for the envelope correlation of the first independent variable.
        :return: The psi's data. Or nothing if the psi's data has not been computed.
        :rtype: list of, list of float
        """
        return self.statistics_connectivity_runnable.get_psi_data_one()

    def get_statistics_psi_data_two(self):
        """
        Get the psi's data for the envelope correlation of the second independent variable.
        :return: The psi's data. Or nothing if the psi's data has not been computed.
        :rtype: list of, list of float
        """
        return self.statistics_connectivity_runnable.get_psi_data_two()

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

    def set_event_values(self, event_values, index=None):
        """
        Sets the values of the events for the dataset.
        :param event_values: The event values
        :type event_values: list of, list of int
        :param index: The index of the dataset to set the event. If None, the current dataset index will be taken.
        :type index: int
        """
        if index is None:
            index = self.current_dataset_index
        file_type = self.file_type[index]
        if file_type == "Raw":
            self.read_events[index] = np.copy(event_values)
        elif file_type == "Epochs":
            self.file_data[index].events = np.copy(event_values)

    def set_event_ids(self, event_ids):
        """
        Sets the events' ids for the dataset.
        :param event_ids: The events' ids.
        :type event_ids: dict
        """
        file_type = self.file_type[self.current_dataset_index]
        if file_type == "Raw":
            self.read_event_ids[self.current_dataset_index] = copy(event_ids)
        elif file_type == "Epochs":
            self.file_data[self.current_dataset_index].event_id = copy(event_ids)

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
        new_channels_locations = copy(channel_locations)
        channels_info = self.file_data[self.current_dataset_index].info.get("chs")
        for i, channel in enumerate(channels_info):
            channel_location = new_channels_locations[channel_names[i]]
            channel["loc"] = np.array([channel_location[0], channel_location[1], channel_location[2], 0.0, 0.0, 0.0,
                                       np.NAN, np.NAN, np.NAN, np.NAN, np.NAN, np.NAN])     # MNE Format
        self.channels_locations[self.current_dataset_index] = copy(new_channels_locations)

    def set_channel_names(self, channel_names):
        """
        Sets the channels' names inside the MNE "Epochs" or "Raw" object of the dataset.
        :param channel_names: The channels' names.
        :type channel_names: list of str
        """
        file_data = self.file_data[self.current_dataset_index]
        self.file_data[self.current_dataset_index] = file_data.pick_channels(channel_names)

    def set_reference(self, channels_selected):
        """
        Sets the reference of the dataset.
        :param channels_selected: The channels' names.
        :type channels_selected: list of str
        """
        if channels_selected[0] in ["average", "infinity"]:
            self.references[self.current_dataset_index] = channels_selected[0]
        else:
            self.references[self.current_dataset_index] = channels_selected

    def set_current_dataset_index(self, index_selected):
        """
        Sets the current dataset index of the currently selected dataset.
        :param index_selected: The index of the currently selected dataset.
        :type index_selected: int
        """
        self.current_dataset_index = index_selected

    def set_study_selected(self):
        """
        Sets the selection of the study to True.
        """
        self.study_selected = True
