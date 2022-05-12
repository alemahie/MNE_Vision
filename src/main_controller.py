#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

import sys

from PyQt6.QtWidgets import QApplication

from main_model import mainModel
from main_view import mainView
from main_listener import mainListener

from menubar.menubar_controller import menubarController

from file.find_events_from_channel.find_events_from_channel_controller import findEventsFromChannelController

from edit.dataset_info.dataset_info_controller import datasetInfoController
from edit.event_values.event_values_controller import eventValuesController
from edit.channel_location.channel_location_controller import channelLocationController

from tools.filter.filter_controller import filterController
from tools.resampling.resampling_controller import resamplingController
from tools.re_referencing.re_referencing_controller import reReferencingController
from tools.ICA_decomposition.ICA_decomposition_controller import icaDecompositionController
from tools.extract_epochs.extract_epochs_controller import extractEpochsController
from tools.source_estimation.source_estimation_controller import sourceEstimationController

from plots.power_spectral_density.power_spectral_density_controller import powerSpectralDensityController
from plots.topographies.topographies_controller import topographiesController
from plots.erp_image.erp_image_controller import erpImageController
from plots.erp.erp_controller import erpController
from plots.time_frequency_ersp_itc.time_frequency_ersp_itc_controller import timeFrequencyErspItcController

from connectivity.envelope_correlation.envelope_correlation_controller import envelopeCorrelationController
from connectivity.source_space_connectivity.source_space_connectivity_controller import sourceSpaceConnectivityController
from connectivity.sensor_space_connectivity.spectral_connectivity_controller import sensorSpaceConnectivityController
from connectivity.spectro_temporal_connectivity.spectro_temporal_connectivity_controller import \
    spectroTemporalConnectivityController

from classification.classify.classify_controller import classifyController

from utils.stylesheet import get_stylesheet
from utils.waiting_while_processing.waiting_while_processing_controller import waitingWhileProcessingController
from utils.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class mainController(mainListener):
    def __init__(self):
        self.main_model = mainModel()
        self.main_model.set_listener(self)

        self.app = QApplication(sys.argv)
        self.app.setStyleSheet(get_stylesheet())

        self.main_view = mainView()
        self.screen_size = self.get_screen_geometry()
        self.main_view.resize(0.8 * self.screen_size.width(), 0.8 * self.screen_size.height())

        self.menubar_controller = menubarController()
        self.menubar_controller.set_listener(self)
        self.menubar_view = self.menubar_controller.get_view()
        self.main_view.setMenuBar(self.menubar_view)

        self.find_events_from_channel_controller = None

        self.dataset_info_controller = None
        self.event_values_controller = None
        self.channel_location_controller = None

        self.filter_controller = None
        self.resampling_controller = None
        self.re_referencing_controller = None
        self.ica_decomposition_controller = None
        self.extract_epochs_controller = None
        self.source_estimation_controller = None

        self.power_spectral_density_controller = None
        self.topographies_controller = None
        self.erp_image_controller = None
        self.erp_controller = None
        self.time_frequency_ersp_itc_controller = None

        self.envelope_correlation_controller = None
        self.source_space_connectivity_controller = None
        self.sensor_space_connectivity_controller = None
        self.spectro_temporal_connectivity_controller = None

        self.classify_controller = None

        self.waiting_while_processing_controller = None

        self.main_view.show()

        sys.exit(self.app.exec())

    """
    File menu
    """
    # Open FIF File
    def open_fif_file_clicked(self, path_to_file):
        if path_to_file != '':
            processing_title = "FIF file reading running, please wait."
            finish_method = "open_fif_file"
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
            self.waiting_while_processing_controller.set_listener(self)
            self.main_model.open_fif_file(path_to_file)

    def open_fif_file_computation_finished(self):
        processing_title_finished = "FIF file reading finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def open_fif_file_finished(self):
        self.display_all_info()

    # Open CNT file
    def open_cnt_file_clicked(self, path_to_file):
        if path_to_file != '':
            processing_title = "CNT file reading running, please wait."
            finish_method = "open_cnt_file"
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
            self.waiting_while_processing_controller.set_listener(self)
            self.main_model.open_cnt_file(path_to_file)

    def open_cnt_file_computation_finished(self):
        processing_title_finished = "CNT file reading finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def open_cnt_file_finished(self):
        self.display_all_info()

    # Open SET file
    def open_set_file_clicked(self, path_to_file):
        if path_to_file != '':
            processing_title = "SET file reading running, please wait."
            finish_method = "open_set_file"
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
            self.waiting_while_processing_controller.set_listener(self)
            self.main_model.open_set_file(path_to_file)

    def open_set_file_computation_finished(self):
        processing_title_finished = "SET file reading finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def open_set_file_finished(self):
        self.display_all_info()

    # Read Events
    def read_events_file_clicked(self, path_to_file):
        if path_to_file != '':
            file_type = self.main_model.get_file_type()
            if file_type == "Raw":
                self.main_model.read_events_file(path_to_file)
            else:
                error_message = "You can only find events when processing a raw file."
                error_window = errorWindow(error_message)
                error_window.show()

    def find_events_from_channel_clicked(self):
        file_type = self.main_model.get_file_type()
        if file_type == "Raw":
            all_channels_names = self.main_model.get_all_channels_names()
            self.find_events_from_channel_controller = findEventsFromChannelController(all_channels_names)
            self.find_events_from_channel_controller.set_listener(self)
        else:
            error_message = "You can only find events when processing a raw file."
            error_window = errorWindow(error_message)
            error_window.show()

    def find_events_from_channel_information(self, stim_channel):
        processing_title = "Finding events from the channel, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.find_events_from_channel(stim_channel)

    def find_events_from_channel_computation_finished(self):
        processing_title_finished = "Finding events from the channel finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def find_events_from_channel_computation_error(self):
        processing_title_finished = "An error as occurred when trying to find events from the provided channel, please try again."
        self.waiting_while_processing_controller.set_finish_method("error")
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    # Export
    def export_data_to_file_clicked(self):
        print("export data")

    def export_events_to_file_clicked(self):
        print("export events")

    # Save
    def save_file_clicked(self):
        if self.main_model.is_fif_file():
            path_to_file = self.main_model.get_file_path_name()
        else:
            path_to_file = self.main_view.get_path_to_file()
        self.main_model.save_file(path_to_file)
        self.main_view.update_path_to_file(self.main_model.get_file_path_name())

    def save_file_as_clicked(self):
        path_to_file = self.main_view.get_path_to_file()
        self.main_model.save_file_as(path_to_file)
        self.main_view.update_path_to_file(self.main_model.get_file_path_name())

    """
    Edit menu
    """
    def dataset_info_clicked(self):
        sampling_rate = self.main_model.get_sampling_frequency()
        time_points_epochs = self.main_model.get_number_of_frames()
        start_time = self.main_model.get_epochs_start()
        self.dataset_info_controller = datasetInfoController(sampling_rate, time_points_epochs, start_time)
        self.dataset_info_controller.set_listener(self)

    def dataset_info_finished(self, channel_locations, channel_names):
        self.main_model.set_channel_locations(channel_locations, channel_names)
        self.main_model.set_channel_names(channel_names)

    def event_values_clicked(self):
        file_type = self.main_model.get_file_type()
        if file_type == "Epochs":
            event_values = self.main_model.get_event_values()
            event_ids = self.main_model.get_event_ids()
            number_of_epochs = self.main_model.get_number_of_epochs()
            number_of_frames = self.main_model.get_number_of_frames()
            self.event_values_controller = eventValuesController(event_values, event_ids, number_of_epochs,
                                                                 number_of_frames)
            self.event_values_controller.set_listener(self)
        else:
            error_message = "You must be working with an epoched file to edit the events."
            error_window_view = errorWindow(error_message)
            error_window_view.show()

    def event_values_finished(self, event_values, event_ids):
        self.main_model.set_event_values(event_values)
        self.main_model.set_event_ids(event_ids)
        number_of_events = self.main_model.get_number_of_events()
        self.main_view.update_number_of_events(number_of_events)

    def channel_location_clicked(self):
        channel_location = self.main_model.get_channels_locations()
        channel_names = self.main_model.get_all_channels_names()
        self.channel_location_controller = channelLocationController(channel_location, channel_names)
        self.channel_location_controller.set_listener(self)

    def select_data_clicked(self):
        pass

    def select_data_events_clicked(self):
        pass

    """
    Tools menu
    """
    # Filtering
    def filter_clicked(self):
        all_channels_names = self.main_model.get_all_channels_names()
        self.filter_controller = filterController(all_channels_names)
        self.filter_controller.set_listener(self)

    def filter_information(self, low_frequency, high_frequency, channels_selected):
        processing_title = "Filtering running, please wait."
        finish_method = "filtering"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.filter(low_frequency, high_frequency, channels_selected)

    def filter_computation_finished(self):
        processing_title_finished = "Filtering finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def filter_finished(self):
        dataset_size = self.main_model.get_dataset_size()
        self.main_view.update_dataset_size(dataset_size)

    # Resampling
    def resampling_clicked(self):
        frequency = self.main_model.get_sampling_frequency()
        self.resampling_controller = resamplingController(frequency)
        self.resampling_controller.set_listener(self)

    def resampling_information(self, frequency):
        processing_title = "Resampling running, please wait."
        finish_method = "resampling"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.resampling(frequency)

    def resampling_computation_finished(self):
        processing_title_finished = "Resampling finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def resampling_finished(self):
        frequency = self.main_model.get_sampling_frequency()
        number_of_frames = self.main_model.get_number_of_frames()
        dataset_size = self.main_model.get_dataset_size()
        self.main_view.update_sampling_frequency(frequency)
        self.main_view.update_number_of_frames(number_of_frames)
        self.main_view.update_dataset_size(dataset_size)

    # Re-referencing
    def re_referencing_clicked(self):
        reference = self.main_model.get_reference()
        all_channels_names = self.main_model.get_all_channels_names()
        self.re_referencing_controller = reReferencingController(reference, all_channels_names)
        self.re_referencing_controller.set_listener(self)

    def re_referencing_information(self, references, n_jobs):
        processing_title = "Re-referencing running, please wait."
        finish_method = "re-referencing"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.re_referencing(references, n_jobs)

    def re_referencing_computation_finished(self):
        processing_title_finished = "Re-referencing finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def re_referencing_finished(self):
        references = self.main_model.get_reference()
        self.main_view.update_reference(references)

    # Reject data
    def inspect_reject_data_clicked(self):
        pass

    # ICA decomposition
    def ica_decomposition_clicked(self):
        self.ica_decomposition_controller = icaDecompositionController()
        self.ica_decomposition_controller.set_listener(self)

    def ica_decomposition_information(self, ica_method):
        processing_title = "ICA decomposition running, please wait."
        finish_method = "ica_decomposition"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.ica_data_decomposition(ica_method)

    def ica_decomposition_computation_finished(self):
        processing_title_finished = "ICA decomposition finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def ica_decomposition_finished(self):
        ica_status = self.main_model.get_ica()
        self.main_view.update_ica_decomposition(ica_status)

    # Extract Epochs
    def extract_epochs_clicked(self):
        self.extract_epochs_controller = extractEpochsController()
        self.extract_epochs_controller.set_listener(self)

    def extract_epochs_information(self, tmin, tmax):
        processing_title = "Epochs extraction running, please wait."
        finish_method = "extract_epochs"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.extract_epochs(tmin, tmax)

    def extract_epochs_computation_finished(self):
        processing_title_finished = "Epochs extraction finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def extract_epochs_finished(self):
        try:
            file_type = self.main_model.get_file_type()
            number_events = self.main_model.get_number_of_events()
            number_epochs = self.main_model.get_number_of_epochs()
            epoch_start = self.main_model.get_epochs_start()
            epoch_end = self.main_model.get_epochs_end()
            number_of_frames = self.main_model.get_number_of_frames()
            self.main_view.update_file_type(file_type)
            self.main_view.update_number_of_events(number_events)
            self.main_view.update_number_of_epochs(number_epochs)
            self.main_view.update_epoch_start(epoch_start)
            self.main_view.update_epoch_end(epoch_end)
            self.main_view.update_number_of_frames(number_of_frames)
        except Exception as e:
            print("azetrruu")
            print(type(e))
            print(e)

    # Source Estimation
    def source_estimation_clicked(self):
        self.source_estimation_controller = sourceEstimationController()
        self.source_estimation_controller.set_listener(self)

    def source_estimation_information(self, source_estimation_method, save_data, load_data, n_jobs):
        processing_title = "Source estimation running, please wait."
        finish_method = "source_estimation"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.source_estimation(source_estimation_method, save_data, load_data, n_jobs)

    def source_estimation_computation_finished(self):
        processing_title_finished = "Source estimation finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def source_estimation_computation_error(self):
        processing_title_finished = "An error as occurred during the computation of the source estimation, please try again."
        self.waiting_while_processing_controller.set_finish_method("error")
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def source_estimation_finished(self):
        source_estimation_data = self.main_model.get_source_estimation_data()
        self.source_estimation_controller.plot_source_estimation(source_estimation_data)

    """
    Plot menu
    """
    def plot_channel_locations_clicked(self):
        file_data = self.main_model.get_file_data()
        self.main_view.plot_channel_locations(file_data)

    def plot_data_clicked(self):
        file_data = self.main_model.get_file_data()
        file_type = self.main_model.get_file_type()
        if file_type == "Raw":
            self.main_view.plot_data(file_data, file_type)
        else:
            event_values = self.main_model.get_event_values()
            event_ids = self.main_model.get_event_ids()
            self.main_view.plot_data(file_data, file_type, events=event_values, event_id=event_ids)

    def plot_topographies_clicked(self):
        self.topographies_controller = topographiesController()
        self.topographies_controller.set_listener(self)

    def plot_topographies_information(self, time_points, mode):
        file_data = self.main_model.get_file_data()
        self.main_view.plot_topographies(file_data, time_points, mode)

    # Spectra maps
    def plot_spectra_maps_clicked(self):
        minimum_time = self.main_model.get_epochs_start()
        maximum_time = self.main_model.get_epochs_end()
        self.power_spectral_density_controller = powerSpectralDensityController(minimum_time, maximum_time)
        self.power_spectral_density_controller.set_listener(self)

    def plot_spectra_maps_information(self, method_psd, minimum_frequency, maximum_frequency, minimum_time, maximum_time):
        processing_title = "PSD running, please wait."
        finish_method = "plot_spectra_maps"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.power_spectral_density(method_psd, minimum_frequency, maximum_frequency, minimum_time, maximum_time)

    def plot_spectra_maps_computation_finished(self):
        processing_title_finished = "PSD finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def plot_spectra_maps_finished(self):
        psds = self.main_model.get_psds()
        freqs = self.main_model.get_freqs()
        self.power_spectral_density_controller.plot_psd(psds, freqs)

    def plot_ERP_image_clicked(self):
        all_channels_names = self.main_model.get_all_channels_names()
        self.erp_image_controller = erpImageController(all_channels_names)
        self.erp_image_controller.set_listener(self)

    def plot_ERP_image_information(self, channel_selected):
        file_data = self.main_model.get_file_data()
        self.main_view.plot_erp_image(file_data, channel_selected)

    def plot_ERPs_clicked(self):
        all_channels_names = self.main_model.get_all_channels_names()
        self.erp_controller = erpController(all_channels_names)
        self.erp_controller.set_listener(self)

    def plot_ERPs_information(self, channels_selected):
        file_data = self.main_model.get_file_data()
        self.main_view.plot_erps(file_data, channels_selected)

    # Time frequency
    def plot_time_frequency_clicked(self):
        all_channels_names = self.main_model.get_all_channels_names()
        self.time_frequency_ersp_itc_controller = timeFrequencyErspItcController(all_channels_names)
        self.time_frequency_ersp_itc_controller.set_listener(self)

    def plot_time_frequency_information(self, method_tfr, channel_selected, min_frequency, max_frequency, n_cycles):
        processing_title = "Time frequency analysis running, please wait."
        finish_method = "time_frequency"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.time_frequency(method_tfr, channel_selected, min_frequency, max_frequency, n_cycles)

    def plot_time_frequency_computation_finished(self):
        processing_title_finished = "Time frequency analysis finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def plot_time_frequency_computation_error(self):
        processing_title_finished = "An error as occurred during the time frequency analysis, please try again."
        self.waiting_while_processing_controller.set_finish_method("error")
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def plot_time_frequency_finished(self):
        channel_selected = self.main_model.get_tfr_channel_selected()
        power = self.main_model.get_power()
        itc = self.main_model.get_itc()
        self.time_frequency_ersp_itc_controller.plot_ersp_itc(channel_selected, power, itc)

    """
    Connectivity menu
    """
    def envelope_correlation_clicked(self):
        number_of_channels = self.main_model.get_number_of_channels()
        self.envelope_correlation_controller = envelopeCorrelationController(number_of_channels)
        self.envelope_correlation_controller.set_listener(self)

    def envelope_correlation_information(self):
        processing_title = "Envelope correlation running, please wait."
        finish_method = "envelope_correlation"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.envelope_correlation()

    def envelope_correlation_computation_finished(self):
        processing_title_finished = "Envelope correlation finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def envelope_correlation_finished(self):
        envelope_correlation_data = self.main_model.get_envelope_correlation_data()
        channel_names = self.main_model.get_all_channels_names()
        self.envelope_correlation_controller.plot_envelope_correlation(envelope_correlation_data, channel_names)

    def source_space_connectivity_clicked(self):
        number_of_channels = self.main_model.get_number_of_channels()
        self.source_space_connectivity_controller = sourceSpaceConnectivityController(number_of_channels)
        self.source_space_connectivity_controller.set_listener(self)

    def source_space_connectivity_information(self, connectivity_method, spectrum_estimation_method, source_estimation_method,
                                              save_data, load_data, n_jobs):
        processing_title = "Source Space Connectivity running, please wait."
        finish_method = "source_space_connectivity"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.source_space_connectivity(connectivity_method, spectrum_estimation_method, source_estimation_method,
                                                  save_data, load_data, n_jobs)

    def source_space_connectivity_computation_finished(self):
        processing_title_finished = "Source Space Connectivity finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def source_space_connectivity_computation_error(self):
        processing_title_finished = "An error as occurred during the computation of the source space connectivity, please try again."
        self.waiting_while_processing_controller.set_finish_method("error")
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def source_space_connectivity_finished(self):
        source_space_connectivity_data = self.main_model.get_source_space_connectivity_data()
        self.source_space_connectivity_controller.plot_source_space_connectivity(source_space_connectivity_data)

    def sensor_space_connectivity_clicked(self):
        file_info = self.main_model.get_file_data().info
        self.sensor_space_connectivity_controller = sensorSpaceConnectivityController(file_info)
        self.sensor_space_connectivity_controller.set_listener(self)

    def sensor_space_connectivity_information(self):
        processing_title = "Sensor Space Connectivity running, please wait."
        finish_method = "sensor_space_connectivity"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.sensor_space_connectivity()

    def sensor_space_connectivity_computation_finished(self):
        processing_title_finished = "Sensor Space Connectivity finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def sensor_space_connectivity_finished(self):
        sensor_space_connectivity_data = self.main_model.get_sensor_space_connectivity_data()
        self.sensor_space_connectivity_controller.plot_sensor_space_connectivity(sensor_space_connectivity_data)

    def spectro_temporal_connectivity_clicked(self):
        self.spectro_temporal_connectivity_controller = spectroTemporalConnectivityController()
        self.spectro_temporal_connectivity_controller.set_listener(self)

    def spectro_temporal_connectivity_information(self):
        print("Spectro-Temporal Connectivity")

    """
    Classification menu
    """
    def classify_clicked(self):
        self.classify_controller = classifyController()
        self.classify_controller.set_listener(self)

    def classify_information(self, pipeline_selected, feature_selection, hyper_tuning, cross_val_number):
        processing_title = "Classification running, please wait."
        finish_method = "classify"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.classify(pipeline_selected, feature_selection, hyper_tuning, cross_val_number)

    def classify_computation_finished(self):
        processing_title_finished = "Classification finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def classify_finished(self):
        classifier = self.main_model.get_classifier()
        self.classify_controller.plot_results(classifier)

    """
    Others
    """
    def display_all_info(self):
        all_info = self.main_model.get_all_displayed_info()
        self.main_view.display_info(all_info)
        self.menubar_controller.enable_menu_when_file_loaded()

    def waiting_while_processing_finished(self, finish_method):
        if finish_method == "open_fif_file":
            self.open_cnt_file_finished()
        elif finish_method == "open_cnt_file":
            self.open_cnt_file_finished()
        elif finish_method == "open_set_file":
            self.open_set_file_finished()
        elif finish_method == "filtering":
            self.filter_finished()
        elif finish_method == "resampling":
            self.resampling_finished()
        elif finish_method == "re-referencing":
            self.re_referencing_finished()
        elif finish_method == "ica_decomposition":
            self.ica_decomposition_finished()
        elif finish_method == "extract_epochs":
            self.extract_epochs_finished()
        elif finish_method == "source_estimation":
            self.source_estimation_finished()
        elif finish_method == "plot_spectra_maps":
            self.plot_spectra_maps_finished()
        elif finish_method == "time_frequency":
            self.plot_time_frequency_finished()
        elif finish_method == "envelope_correlation":
            self.envelope_correlation_finished()
        elif finish_method == "source_space_connectivity":
            self.source_space_connectivity_finished()
        elif finish_method == "sensor_space_connectivity":
            self.sensor_space_connectivity_finished()
        elif finish_method == "classify":
            self.classify_finished()

    """
    Getters
    """
    def get_screen_geometry(self):
        screen = self.app.primaryScreen()
        size = screen.size()
        return size
