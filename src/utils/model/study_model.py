#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Study Model
"""

from copy import copy
from os.path import getsize

from PyQt5.QtCore import QThreadPool
from mne import concatenate_epochs

from runnables.study_runnable import studyTimeFrequencyRunnable
from utils.view.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class studyModel:
    def __init__(self, study_name, task_name, dataset_names, dataset_indexes, subjects, sessions, runs, conditions, groups):
        """
        Model for the study based on the dataset selected by the user
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
        self.main_listener = None
        self.study_listener = None

        self.study_name = study_name
        self.task_name = task_name
        self.dataset_names = dataset_names
        self.dataset_indexes = dataset_indexes
        self.subjects = subjects
        self.sessions = sessions
        self.runs = runs
        self.conditions = conditions
        self.groups = groups

        self.time_frequency_runnable = None

        self.fig_psd = None
        self.fig_topo = None

    """
    Plots
    """
    # PSD
    def plot_psd(self, channels_selected, subjects_selected, minimum_frequency, maximum_frequency, minimum_time,
                 maximum_time, topo_time_points):
        """
        Plot the PSD for the dataset of the study with the channels and subjects selected.
        :param channels_selected: Channels selected
        :type channels_selected: str/list of str
        :param subjects_selected: Subjects selected
        :type subjects_selected: str/list of str
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
        try:
            all_file_data = self.get_selected_file_data_with_subjects(subjects_selected)
            all_file_data = self.adapt_events(all_file_data)
            file_data = concatenate_epochs(all_file_data)
            file_data = file_data.pick(channels_selected)

            bandwidth = 1.0 / (maximum_time - minimum_time)  # To counter bandwidth normalization
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

    def power_spectral_density_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.study_listener.plot_spectra_maps_computation_finished()

    def power_spectral_density_computation_error(self):
        """
        Notifies the main controller that an error has occurred during the computation
        """
        self.study_listener.plot_spectra_maps_computation_error()

    # ERSP ITC
    def plot_ersp_itc(self, channels_selected, subjects_selected, method_tfr, min_frequency, max_frequency, n_cycles):
        """
        Plot the ERSP and ITC for the dataset of the study with the channels and subjects selected.
        :param channels_selected: Channels selected
        :type channels_selected: str/list of str
        :param subjects_selected: Subjects selected
        :type subjects_selected: str/list of str
        :param method_tfr: Method used for computing the time-frequency analysis.
        :type method_tfr: str
        :param min_frequency: Minimum frequency from which the time-frequency analysis will be computed.
        :type min_frequency: float
        :param max_frequency: Maximum frequency from which the time-frequency analysis will be computed.
        :type max_frequency: float
        :param n_cycles: Number of cycles used by the time-frequency analysis for his computation.
        :type n_cycles: int
        """
        try:
            all_file_data = self.get_selected_file_data_with_subjects(subjects_selected)
            all_file_data = self.adapt_events(all_file_data)
            file_data = concatenate_epochs(all_file_data)

            pool = QThreadPool.globalInstance()
            self.time_frequency_runnable = studyTimeFrequencyRunnable(file_data, method_tfr, channels_selected,
                                                                      min_frequency, max_frequency, n_cycles)
            pool.start(self.time_frequency_runnable)
            self.time_frequency_runnable.signals.finished.connect(self.time_frequency_computation_finished)
            self.time_frequency_runnable.signals.error.connect(self.time_frequency_computation_error)
        except Exception as error:
            error_message = "An error has occurred during the computation of the ERSP-ITC"
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.power_spectral_density_computation_error()

    def time_frequency_computation_finished(self):
        """
        Notifies the main controller that the computation is done.
        """
        self.study_listener.plot_time_frequency_computation_finished()

    def time_frequency_computation_error(self):
        """
        Notifies the main controller that the computation had an error.
        """
        self.study_listener.plot_time_frequency_computation_error()

    """
    Utils
    """
    @staticmethod
    def adapt_events(all_file_data):
        """
        Adapts the events on all the epochs so that they are all common and the epochs can thus be concatenated.
        :param all_file_data: The epochs on which the events must be adapted.
        :type all_file_data: list of MNE Epochs
        :return: The new epochs with the events adapted for concatenation
        :rtype: list of MNE Epochs
        """
        new_all_file_data = []
        all_event_ids = {}
        event_ids_counter = 1
        for file_data in all_file_data:     # Search
            event_ids = file_data.event_id
            for event_id in event_ids.keys():
                if event_id not in all_event_ids:
                    all_event_ids[event_id] = event_ids_counter
                    event_ids_counter += 1
        for file_data in all_file_data:     # Modify
            file_data.event_id = copy(all_event_ids)
            new_all_file_data.append(file_data)
        return new_all_file_data

    def check_file_type_all_epochs(self, all_file_type):
        """
        Check if all the file type in the study are epochs.
        :param all_file_type: All the file type of each dataset loaded.
        :type all_file_type: list of str
        :return: True if all datasets are epoched, False otherwise.
        :rtype: bool
        """
        for index in self.dataset_indexes:
            if all_file_type[index] == "Raw":
                return False
        return True     # All dataset are epochs if not raw, so ok.

    """
    Getters
    """
    def get_displayed_info(self):
        all_info = [self.study_name, "/", self.task_name, self.get_number_of_subjects(), self.get_number_of_conditions(),
                    self.get_number_of_sessions(), self.get_number_of_groups(), self.get_epochs_consistency(),
                    self.get_number_of_channels(), self.get_channel_locations(), self.get_status(), self.get_size()]
        return all_info

    def get_number_of_subjects(self):
        """
        Gets the number of different subjects in the study
        :return: The number of subjects
        :rtype: int
        """
        unique_subjects = []
        for subject in self.subjects:
            if subject not in unique_subjects:
                unique_subjects.append(subject)
        return len(unique_subjects)

    def get_number_of_conditions(self):
        """
        Gets the number of different conditions in the study
        :return: The number of conditions
        :rtype: int
        """
        unique_conditions = []
        for condition in self.conditions:
            if condition not in unique_conditions:
                unique_conditions.append(condition)
        return len(unique_conditions)

    def get_number_of_sessions(self):
        """
        Gets the number of different sessions in the study
        :return: The number of sessions
        :rtype: int
        """
        unique_sessions = []
        for session in self.sessions:
            if session not in unique_sessions:
                unique_sessions.append(session)
        return len(unique_sessions)

    def get_number_of_groups(self):
        """
        Gets the number of different groups in the study
        :return: The number of groups
        :rtype: int
        """
        unique_groups = []
        for group in self.groups:
            if group not in unique_groups:
                unique_groups.append(group)
        return len(unique_groups)

    def get_epochs_consistency(self):
        """
        Gets the epochs' consistency, if one of the dataset has different epochs times, the consistency will be false.
        :return: The epochs' consistency.
        :rtype: bool
        """
        epochs_consistency = True
        file_data = self.get_selected_file_data()

        epochs_start = round(file_data[0].times[0], 3)
        epochs_end = round(file_data[0].times[-1], 3)
        for i in range(1, len(file_data)):
            if epochs_start != round(file_data[i].times[0], 3):
                epochs_consistency = False
                break
            if epochs_end != round(file_data[i].times[-1], 3):
                epochs_consistency = False
                break
        return epochs_consistency

    def get_number_of_channels(self):
        """
        Gets the number of channels that are present in the study.
        :return: The number of channels
        :rtype: int
        """
        file_data = self.get_selected_file_data()
        return len(file_data[0].ch_names)

    def get_channel_locations(self):
        """
        Gets the channel location status that is present in the study.
        :return: The status of the channel location
        :rtype: str
        """
        file_data = self.get_selected_file_data()
        channel_location_available = "No"
        for i in range(len(file_data)):
            channel_location = file_data[i].ch_names
            if channel_location is not None:
                channel_location_available = "Yes"
                break
        return channel_location_available

    def get_status(self):
        """
        Gets the ICA status in the study.
        :return: The status of the ICA
        :rtype: str
        """
        all_ica = self.main_listener.get_all_ica()
        yes_counter = 0
        no_counter = 0
        for index in self.dataset_indexes:
            if all_ica[index] == "Yes":
                yes_counter += 1
            elif all_ica[index] == "No":
                no_counter += 1
        if yes_counter > 0 and no_counter == 0:
            return "ICA decomposition complete"
        elif yes_counter > 0 and no_counter > 0:
            return "Some ICA decomposition missing"
        elif yes_counter == 0 and no_counter > 0:
            return "ICA decomposition missing"

    def get_size(self):
        """
        Gets the size in megabits of the study.
        :return: The size of the study.
        :rtype: float
        """
        all_file_path_name = self.main_listener.get_all_file_path_name()
        selected_file_path_name = []
        for index in self.dataset_indexes:
            selected_file_path_name.append(all_file_path_name[index])

        total_size = 0
        for file_path_name in selected_file_path_name:
            try:
                total_size += round(getsize(file_path_name[:-3] + "fdt") / (1024 ** 2), 3)
            except:
                total_size += round(getsize(file_path_name) / (1024 ** 2), 3)
        return total_size

    # Getters utils
    def get_selected_file_data(self):
        """
        Gets the selected file data in the study
        :return: The selected file data.
        :rtype: list of MNE Epochs/Raw
        """
        all_file_data = self.main_listener.get_all_file_data()
        selected_file_data = []
        for index in self.dataset_indexes:
            selected_file_data.append(all_file_data[index])
        return selected_file_data

    def get_selected_file_data_with_subjects(self, subjects_selected):
        """
        Gets the selected file data in the study in function of the subjects selected.
        :return: The selected file data.
        :rtype: list of MNE Epochs/Raw
        """
        all_file_data = self.main_listener.get_all_file_data()
        selected_file_data = []
        for index in self.dataset_indexes:
            if self.subjects[index] in subjects_selected:       # If the dataset subject is in the subject selected, ok.
                selected_file_data.append(all_file_data[index])
        return selected_file_data

    def get_unique_subjects(self):
        """
        Gets only one copy of each subject.
        :return: The subjects assigned to each dataset in the study
        :rtype: list of str
        """
        subjects = []
        for subject in self.subjects:
            if subject not in subjects:
                subjects.append(subject)
        return subjects

    def get_study_name(self):
        """
        Gets the study name of the study.
        :return: The study name
        :rtype: str
        """
        return self.study_name

    def get_task_name(self):
        """
        Gets the task name of the study.
        :return: The task name
        :rtype: str
        """
        return self.task_name

    def get_dataset_names(self):
        """
        Gets the dataset names.
        :return: The dataset names
        :rtype: list of str
        """
        return self.dataset_names

    def get_dataset_indexes(self):
        """
        Gets the dataset indexes
        :return: The indexes of the datasets selected to be in the study
        :rtype: list of int
        """
        return self.dataset_indexes

    def get_subjects(self):
        """
        Gets the subjects
        :return: The subjects assigned to each dataset in the study
        :rtype: list of str
        """
        return self.subjects

    def get_sessions(self):
        """
        Gets the sessions
        :return: The sessions assigned to each dataset in the study
        :rtype: list of str
        """
        return self.sessions

    def get_runs(self):
        """
        Gets the runs
        :return: The runs assigned to each dataset in the study
        :rtype: list of str
        """
        return self.runs

    def get_conditions(self):
        """
        Gets the conditions
        :return: The conditions assigned to each dataset in the study
        :rtype: list of str
        """
        return self.conditions

    def get_groups(self):
        """
        Gets the groups
        :return: The groups assigned to each dataset in the study
        :rtype: list of str
        """
        return self.groups

    def get_channel_names(self):
        """
        Gets the channel names.
        :return: The channel names of the datasets in the study.
        :rtype: list of str
        """
        file_data = self.get_selected_file_data()
        return file_data[0].ch_names

    # Runnables
    def get_psd_fig(self):
        """
        Get the power spectral density's figure
        :return: The figure of the actual power spectral density's data computed
        :rtype: matplotlib.Figure
        """
        return self.fig_topo

    def get_psd_topo_fig(self):
        """
        Get the power spectral density's figure fo the topographies
        :return: The figure of the topographies of the actual power spectral density's data computed
        :rtype: matplotlib.Figure
        """
        return self.fig_psd

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

    """
    Setters
    """
    def set_study_name(self, study_name):
        """
        Sets the name of the study.
        :param study_name: The name of the study
        :type study_name: str
        """
        self.study_name = study_name

    def set_task_name(self, task_name):
        """
        Sets the task name.
        :param task_name: The name of the task linked to the study
        :type task_name: str
        """
        self.task_name = task_name

    def set_subjects(self, subjects):
        """
        Sets the subjects for each dataset.
        :param subjects: The subjects assigned to each dataset in the study
        :type subjects: list of str
        """
        self.subjects = subjects

    def set_sessions(self, sessions):
        """
        Sets the sessions for each dataset.
        :param sessions: The sessions assigned to each dataset in the study
        :type sessions: list of str
        """
        self.sessions = sessions

    def set_runs(self, runs):
        """
        Sets the runs for each dataset.
        :param runs: The runs assigned to each dataset in the study
        :type runs: list of str
        """
        self.runs = runs

    def set_conditions(self, conditions):
        """
        Sets the conditions for each dataset.
        :param conditions: The conditions assigned to each dataset in the study
        :type conditions: list of str
        """
        self.conditions = conditions

    def set_groups(self, groups):
        """
        Sets the groups for each dataset.
        :param groups: The groups assigned to each dataset in the study
        :type groups: list of str
        """
        self.groups = groups

    def set_listener(self, listener):
        """
        Set the main listener so that the controller is able to communicate with the main controller.
        :param listener: main listener
        :type listener: mainModel
        """
        self.main_listener = listener

    def set_study_listener(self, listener):
        """
        Set the study listener so that the model is able to communicate with the study controller.
        :param listener: study plot listener
        :type listener: studyPlotsListener
        """
        self.study_listener = listener
