#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Study Model
"""

from os.path import getsize

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
        Model for the study_creation based on the dataset selected by the user
        :param study_name: The name of the study_creation
        :type study_name: str
        :param task_name: The name of the task linked to the study_creation
        :type task_name: str
        :param dataset_names: The name of the datasets linked to the study_creation
        :type dataset_names: list of str
        :param dataset_indexes: The indexes of the datasets selected to be in the study_creation
        :type dataset_indexes: list of int
        :param subjects: The subjects assigned to each dataset in the study_creation
        :type subjects: list of str
        :param sessions: The sessions assigned to each dataset in the study_creation
        :type sessions: list of str
        :param runs: The runs assigned to each dataset in the study_creation
        :type runs: list of str
        :param conditions: The conditions assigned to each dataset in the study_creation
        :type conditions: list of str
        :param groups: The groups assigned to each dataset in the study_creation
        :type groups: list of str
        """
        self.main_listener = None

        self.study_name = study_name
        self.task_name = task_name
        self.dataset_names = dataset_names
        self.dataset_indexes = dataset_indexes
        self.subjects = subjects
        self.sessions = sessions
        self.runs = runs
        self.conditions = conditions
        self.groups = groups

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
        Gets the number of different subjects in the study_creation
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
        Gets the number of different conditions in the study_creation
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
        Gets the number of different sessions in the study_creation
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
        Gets the number of different groups in the study_creation
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
        Gets the number of channels that are present in the study_creation.
        :return: The number of channels
        :rtype: int
        """
        file_data = self.get_selected_file_data()
        return len(file_data[0].ch_names)

    def get_channel_locations(self):
        """
        Gets the channel location status that is present in the study_creation.
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
        Gets the ICA status in the study_creation.
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
        Gets the size in megabits of the study_creation.
        :return: The size of the study_creation.
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
        Gets the selected file data in the study_creation
        :return: The selected file data.
        :rtype: list of MNE Epochs/Raw
        """
        all_file_data = self.main_listener.get_all_file_data()
        selected_file_data = []
        for index in self.dataset_indexes:
            selected_file_data.append(all_file_data[index])
        return selected_file_data

    def get_study_name(self):
        """
        Gets the study_creation name of the study_creation.
        :return: The study_creation name
        :rtype: str
        """
        return self.study_name

    def get_task_name(self):
        """
        Gets the task name of the study_creation.
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
        :return: The indexes of the datasets selected to be in the study_creation
        :rtype: list of int
        """
        return self.dataset_indexes

    def get_subjects(self):
        """
        Gets the subjects
        :return: The subjects assigned to each dataset in the study_creation
        :rtype: list of str
        """
        return self.subjects

    def get_sessions(self):
        """
        Gets the sessions
        :return: The sessions assigned to each dataset in the study_creation
        :rtype: list of str
        """
        return self.sessions

    def get_runs(self):
        """
        Gets the runs
        :return: The runs assigned to each dataset in the study_creation
        :rtype: list of str
        """
        return self.runs

    def get_conditions(self):
        """
        Gets the conditions
        :return: The conditions assigned to each dataset in the study_creation
        :rtype: list of str
        """
        return self.conditions

    def get_groups(self):
        """
        Gets the groups
        :return: The groups assigned to each dataset in the study_creation
        :rtype: list of str
        """
        return self.groups

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
        :param task_name: The name of the task linked to the study_creation
        :type task_name: str
        """
        self.task_name = task_name

    def set_subjects(self, subjects):
        """
        Sets the subjects for each dataset.
        :param subjects: The subjects assigned to each dataset in the study_creation
        :type subjects: list of str
        """
        self.subjects = subjects

    def set_sessions(self, sessions):
        """
        Sets the sessions for each dataset.
        :param sessions: The sessions assigned to each dataset in the study_creation
        :type sessions: list of str
        """
        self.sessions = sessions

    def set_runs(self, runs):
        """
        Sets the runs for each dataset.
        :param runs: The runs assigned to each dataset in the study_creation
        :type runs: list of str
        """
        self.runs = runs

    def set_conditions(self, conditions):
        """
        Sets the conditions for each dataset.
        :param conditions: The conditions assigned to each dataset in the study_creation
        :type conditions: list of str
        """
        self.conditions = conditions

    def set_groups(self, groups):
        """
        Sets the groups for each dataset.
        :param groups: The groups assigned to each dataset in the study_creation
        :type groups: list of str
        """
        self.groups = groups

    def set_listener(self, listener):
        """
        Set the main listener so that the controller is able to communicate with the main controller.
        :param listener: main listener
        :type listener: downloadFsaverageMneDataController
        """
        self.main_listener = listener
