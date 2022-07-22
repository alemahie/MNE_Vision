#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Study Plots Controller
"""
from copy import copy

from mne import combine_evoked, concatenate_epochs

from study.study_plots.study_plots_listener import studyPlotsListener
from study.study_plots.study_plots_view import studyPlotsView

from utils.view.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class studyPlotsController(studyPlotsListener):
    def __init__(self, study):
        """
        Controller for plotting data of the study.
        Create a new window for displaying the information.
        :param study: The current study created on the datasets.
        :type study: studyModel
        """
        self.main_listener = None
        self.study_plots_view = studyPlotsView(study)
        self.study_plots_view.set_listener(self)

        self.study = study

        self.study_plots_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.study_plots_view.close()

    def confirm_button_clicked(self):
        """
        Close the window and send the information to the main controller
        """
        self.study_plots_view.close()
        self.main_listener.edit_plots_information()

    """
    Plots
    """
    def plot_erps_clicked(self, channels_selected, subjects_selected):
        """
        Call the study to plot the erps on the given data.
        :param channels_selected: Channels selected
        :type channels_selected: str/list of str
        :param subjects_selected: Subjects selected
        :type subjects_selected: str/list of str
        """
        try:
            all_file_data = self.study.get_selected_file_data_with_subjects(subjects_selected)
            all_evoked = []
            for file_data in all_file_data:
                all_evoked.append(file_data.average(picks=channels_selected))
            evoked = combine_evoked(all_evoked, weights="nave")
            self.study_plots_view.plot_erps(evoked)
        except Exception as error:
            error_message = "An error occurred during the computation of the ERPs, please try again."
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()

    def plot_psd_clicked(self, channels_selected, subjects_selected):
        """
        Call the study to plot the psd on the given data.
        :param channels_selected: Channels selected
        :type channels_selected: str/list of str
        :param subjects_selected: Subjects selected
        :type subjects_selected: str/list of str
        """
        self.study.plot_psd(channels_selected, subjects_selected)

    def plot_erp_image_clicked(self, channels_selected, subjects_selected):
        """
        Call the study to plot the erp image on the given data.
        :param channels_selected: Channels selected
        :type channels_selected: str/list of str
        :param subjects_selected: Subjects selected
        :type subjects_selected: str/list of str
        """
        try:
            all_file_data = self.study.get_selected_file_data_with_subjects(subjects_selected)
            all_file_data = self.adapt_events(all_file_data)
            file_data = concatenate_epochs(all_file_data)
            self.study_plots_view.plot_erp_image(file_data, channels_selected)
        except Exception as error:
            error_message = "An error occurred during the computation of the ERP image, please try again."
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()

    def plot_ersp_itc_clicked(self, channels_selected, subjects_selected):
        """
        Call the study to plot the ersp and itc on the given data.
        :param channels_selected: Channels selected
        :type channels_selected: str/list of str
        :param subjects_selected: Subjects selected
        :type subjects_selected: str/list of str
        """
        self.study.plot_ersp_itc(channels_selected, subjects_selected)

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

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the main listener so that the controller is able to communicate with the main controller.
        :param listener: main listener
        :type listener: mainController
        """
        self.main_listener = listener
