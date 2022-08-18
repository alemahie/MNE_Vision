#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Study Plots Controller
"""

from copy import copy

from mne import combine_evoked, concatenate_epochs

from plots.power_spectral_density.power_spectral_density_controller import powerSpectralDensityController
from plots.time_frequency_ersp_itc.time_frequency_ersp_itc_controller import timeFrequencyErspItcController
from study.study_plots.study_plots_listener import studyPlotsListener
from study.study_plots.study_plots_view import studyPlotsView

from utils.waiting_while_processing.waiting_while_processing_controller import waitingWhileProcessingController
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
        self.study.set_study_listener(self)
        self.channels_selected = None
        self.subjects_selected = None

        self.power_spectral_density_controller = None
        self.time_frequency_ersp_itc_controller = None
        self.waiting_while_processing_controller = None

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
    # ERPs
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

    # PSD
    def plot_psd_clicked(self, channels_selected, subjects_selected):
        """
        Call the study to plot the psd on the given data.
        :param channels_selected: Channels selected
        :type channels_selected: str/list of str
        :param subjects_selected: Subjects selected
        :type subjects_selected: str/list of str
        """
        self.channels_selected = channels_selected
        self.subjects_selected = subjects_selected

        try:
            all_file_data = self.study.get_selected_file_data()
            minimum_time = round(all_file_data[0].times[0], 3)     # Epoch start
            maximum_time = round(all_file_data[0].times[-1], 3)    # Epoch end
            self.power_spectral_density_controller = powerSpectralDensityController(minimum_time, maximum_time)
            self.power_spectral_density_controller.set_listener(self)
        except Exception as e:
            print(e)

    def plot_spectra_maps_information(self, minimum_frequency, maximum_frequency, minimum_time, maximum_time,
                                      topo_time_points):
        """
        Create the waiting window while the computation of the power spectral density is done on the dataset.
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
        processing_title = "PSD running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.plot_spectra_maps_finished)
        self.waiting_while_processing_controller.set_listener(self)
        self.study.plot_psd(self.channels_selected, self.subjects_selected, minimum_frequency, maximum_frequency,
                            minimum_time, maximum_time, topo_time_points)

    def plot_spectra_maps_computation_finished(self):
        """
        Close the waiting window when the computation of the power spectral density is done on the dataset.
        """
        processing_title_finished = "PSD finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def plot_spectra_maps_computation_error(self):
        """
        Close the waiting window when the computation of the power spectral density is done on the dataset.
        """
        processing_title_finished = "An error has occurred during the computation of the PSD"
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def plot_spectra_maps_finished(self):
        """
        The computation of the power spectral density is completely done, plot it.
        """
        psd_fig = self.study.get_psd_fig()
        topo_fig = self.study.get_psd_topo_fig()
        self.power_spectral_density_controller.plot_psd(psd_fig, topo_fig)

    # ERP image
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

    # ERSP ITC
    def plot_ersp_itc_clicked(self, channels_selected, subjects_selected):
        """
        Call the study to plot the ersp and itc on the given data.
        :param channels_selected: Channels selected
        :type channels_selected: str/list of str
        :param subjects_selected: Subjects selected
        :type subjects_selected: str/list of str
        """
        self.channels_selected = channels_selected
        self.subjects_selected = subjects_selected

        try:
            all_channels_names = self.study.get_channel_names()
            self.time_frequency_ersp_itc_controller = timeFrequencyErspItcController(all_channels_names, no_channels=True)
            self.time_frequency_ersp_itc_controller.set_listener(self)
        except Exception as e:
            print(e)

    def plot_time_frequency_information(self, method_tfr, min_frequency, max_frequency, n_cycles):
        """
        Create the waiting window while the computation of the time-frequency analysis is done on the dataset.
        :param method_tfr: Method used for computing the time-frequency analysis.
        :type method_tfr: str
        :param min_frequency: Minimum frequency from which the time-frequency analysis will be computed.
        :type min_frequency: float
        :param max_frequency: Maximum frequency from which the time-frequency analysis will be computed.
        :type max_frequency: float
        :param n_cycles: Number of cycles used by the time-frequency analysis for his computation.
        :type n_cycles: int
        """
        processing_title = "Time frequency analysis running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.plot_time_frequency_finished)
        self.waiting_while_processing_controller.set_listener(self)
        self.study.plot_ersp_itc(self.channels_selected, self.subjects_selected, method_tfr, min_frequency, max_frequency,
                                 n_cycles)

    def plot_time_frequency_computation_finished(self):
        """
        Close the waiting window when the computation of the time-frequency analysis is done on the dataset.
        """
        processing_title_finished = "Time frequency analysis finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def plot_time_frequency_computation_error(self):
        """
        Close the waiting window and display an error message because an error occurred during the computation.
        """
        processing_title_finished = "An error as occurred during the time frequency analysis, please try again."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def plot_time_frequency_finished(self):
        """
        The computation of the time-frequency analysis is completely done, plot it.
        """
        channel_selected = self.study.get_tfr_channel_selected()
        power = self.study.get_power()
        itc = self.study.get_itc()
        self.time_frequency_ersp_itc_controller.plot_ersp_itc(channel_selected, power, itc)

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
