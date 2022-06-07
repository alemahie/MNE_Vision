#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

from main_model import mainModel
from main_view import mainView
from main_listener import mainListener

from menubar.menubar_controller import menubarController

from file.load_data_info.load_data_info_controller import loadDataInfoController
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
from connectivity.sensor_space_connectivity.sensor_space_connectivity_controller import sensorSpaceConnectivityController
from connectivity.spectro_temporal_connectivity.spectro_temporal_connectivity_controller import \
    spectroTemporalConnectivityController

from classification.classify.classify_controller import classifyController

from utils.download_fsaverage_mne_data.download_fsaverage_mne_data_controller import downloadFsaverageMneDataController
from utils.waiting_while_processing.waiting_while_processing_controller import waitingWhileProcessingController
from utils.error_window import errorWindow
from utils.file_path_search import get_project_freesurfer_path

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class mainController(mainListener):
    def __init__(self, screen_size, splash_screen_runnable = False):
        """
        The main controller is the link between the main model and the main view.
        It will "control" where the information needs to go and who does what.
        All the information for the computation will be directed to the main model, while the information to be displayed
        will be sent to the main view.
        It is responsible for creating the other controllers that will display other windows.
        :param screen_size: Tuple of int corresponding to the size of the screen.
        :type screen_size: QSize
        :param splash_screen_runnable: Runnable for the splash screen, that will be closed on the opening of the main window.
        :type splash_screen_runnable: splashScreenRunnable
        """
        self.main_model = mainModel()
        self.main_model.set_listener(self)

        self.main_view = mainView()
        self.main_view.resize(0.8 * screen_size.width(), 0.8 * screen_size.height())

        self.menubar_controller = menubarController()
        self.menubar_controller.set_listener(self)
        self.menubar_view = self.menubar_controller.get_view()
        self.main_view.setMenuBar(self.menubar_view)

        self.load_data_info_controller = None
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
        self.download_fsaverage_mne_data_controller = None

        # splash_screen_runnable.close()
        self.main_view.show()

    """
    File menu
    """
    # Open FIF File
    def open_fif_file_clicked(self, path_to_file):
        """
        Check if the path to the file is correct.
        Create the waiting window while the FIF file is opened.
        :param path_to_file: Path to the file.
        :type path_to_file: str
        """
        if path_to_file != '':
            processing_title = "FIF file reading running, please wait."
            finish_method = "open_fif_file"
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
            self.waiting_while_processing_controller.set_listener(self)
            self.main_model.open_fif_file(path_to_file)

    def open_fif_file_computation_finished(self):
        """
        Close the waiting window when the FIF file is opened.
        """
        processing_title_finished = "FIF file reading finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def open_fif_file_finished(self):
        """
        The FIF file is loaded, ask more information about the dataset that will be used.
        """
        self.load_data_info()

    # Open CNT file
    def open_cnt_file_clicked(self, path_to_file):
        """
        Check if the path to the file is correct.
        Create the waiting window while the CNT file is opened.
        :param path_to_file: Path to the file.
        :type path_to_file: str
        """
        if path_to_file != '':
            processing_title = "CNT file reading running, please wait."
            finish_method = "open_cnt_file"
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
            self.waiting_while_processing_controller.set_listener(self)
            self.main_model.open_cnt_file(path_to_file)

    def open_cnt_file_computation_finished(self):
        """
        Close the waiting window when the CNT file is opened.
        """
        processing_title_finished = "CNT file reading finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def open_cnt_file_finished(self):
        """
        The CNT file is loaded, ask more information about the dataset that will be used.
        """
        self.load_data_info()

    # Open SET file
    def open_set_file_clicked(self, path_to_file):
        """
        Check if the path to the file is correct.
        Create the waiting window while the SET file is opened.
        :param path_to_file: Path to the file.
        :type path_to_file: str
        """
        if path_to_file != '':
            processing_title = "SET file reading running, please wait."
            finish_method = "open_set_file"
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
            self.waiting_while_processing_controller.set_listener(self)
            self.main_model.open_set_file(path_to_file)

    def open_set_file_computation_finished(self):
        """
        Close the waiting window when the SET file is opened.
        """
        processing_title_finished = "SET file reading finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def open_set_file_finished(self):
        """
        The SET file is loaded, ask more information about the dataset that will be used.
        """
        self.load_data_info()

    # Load Data Info
    def load_data_info(self):
        """
        Create the controller for loading more information about the dataset.
        """
        channel_names = self.main_model.get_all_tmp_channels_names()
        tmin = self.main_model.get_tmp_epochs_start()
        tmax = self.main_model.get_tmp_epochs_end()
        self.load_data_info_controller = loadDataInfoController(channel_names, tmin, tmax)
        self.load_data_info_controller.set_listener(self)

    def load_data_info_information(self, montage, channels_selected, tmin, tmax):
        """
        Create the waiting window while more information about the dataset are loaded.
        :param montage: Montage of the headset
        :type montage: str
        :param channels_selected: Channels selected
        :type channels_selected: list of str
        :param tmin: Start time of the epoch or raw file to keep
        :type tmin: float
        :param tmax: End time of the epoch or raw file to keep
        :type tmax: float
        """
        processing_title = "Loading selected data info, please wait."
        finish_method = "load_data_info"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.load_data_info(montage, channels_selected, tmin, tmax)

    def load_data_info_computation_finished(self):
        """
        Close the waiting window when the additional information about the dataset are loaded.
        """
        processing_title_finished = "Selected data info loaded."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def load_data_info_finished(self):
        """
        More information about the dataset are loaded, tell the main window to display all the information about the dataset.
        """
        self.display_all_info()

    # Read Events
    def read_events_file_clicked(self, path_to_file):
        """
        Check if the path to the file is correct.
        Read the event file if the dataset is "Raw", otherwise display an error message because "Epochs" dataset already
        have events, and they can be modified directly.
        :param path_to_file: Path to the file.
        :type path_to_file: str
        """
        if path_to_file != '':
            file_type = self.main_model.get_file_type()
            if file_type == "Raw":
                self.main_model.read_events_file(path_to_file)
            else:
                error_message = "You can only find events when processing a raw file."
                error_window = errorWindow(error_message)
                error_window.show()

    def find_events_from_channel_clicked(self):
        """
        Create the controller for finding the events based on a stimulation channel.
        """
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
        """
        Create the waiting window while finding the events based on the stimulation channel.
        :param stim_channel: The stimulation channel used to find the events.
        :type stim_channel: str
        """
        processing_title = "Finding events from the channel, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.find_events_from_channel(stim_channel)

    def find_events_from_channel_computation_finished(self):
        """
        Close the waiting window when the events are found based on the stimulation channel.
        """
        processing_title_finished = "Finding events from the channel finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def find_events_from_channel_computation_error(self):
        """
        Close the waiting window and display an error message because an error occurred during the computation.
        """
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
        """
        Save the file into the fif format and display the new path file on the main window.
        """
        if self.main_model.is_fif_file():
            path_to_file = self.main_model.get_file_path_name()
        else:
            path_to_file = self.main_view.get_path_to_file()
        if path_to_file != '':
            self.main_model.save_file(path_to_file)
            self.main_view.update_path_to_file(self.main_model.get_file_path_name())

    def save_file_as_clicked(self):
        """
        Save the file into the fif format and display the new path file on the main window.
        """
        path_to_file = self.main_view.get_path_to_file()
        if path_to_file != '':
            self.main_model.save_file_as(path_to_file)
            self.main_view.update_path_to_file(self.main_model.get_file_path_name())

    """
    Edit menu
    """
    def dataset_info_clicked(self):
        """
        Create the controller for displaying some information about the dataset.
        """
        sampling_rate = self.main_model.get_sampling_frequency()
        number_of_frames = self.main_model.get_number_of_frames()
        start_time = self.main_model.get_epochs_start()
        self.dataset_info_controller = datasetInfoController(sampling_rate, number_of_frames, start_time)
        self.dataset_info_controller.set_listener(self)

    def event_values_clicked(self):
        """
        Create the controller for displaying information about the event of the dataset.
        Display an error message if the dataset is a "Raw" dataset, because only "Epochs" dataset have events.
        """
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
        """
        Update the event values that have been modified by the user and display the information on the main window.
        :param event_values: Event values
        :type event_values: list of, list of int
        :param event_ids: Event ids
        :type event_ids: dict
        """
        self.main_model.set_event_values(event_values)
        self.main_model.set_event_ids(event_ids)
        number_of_events = self.main_model.get_number_of_events()
        self.main_view.update_number_of_events(number_of_events)

    def channel_location_clicked(self):
        """
        Create the controller for displaying information about the channel locations of the dataset.
        """
        channel_location = self.main_model.get_channels_locations()
        channel_names = self.main_model.get_all_channels_names()
        self.channel_location_controller = channelLocationController(channel_location, channel_names)
        self.channel_location_controller.set_listener(self)

    def channel_location_finished(self, channel_locations, channel_names):
        """
        Modify information about channels of the dataset that have been changed by the user.
        :param channel_locations: Channel location
        :type channel_locations: dict
        :param channel_names: Channel names
        :type channel_names: list of str
        """
        self.main_model.set_channel_locations(channel_locations, channel_names)
        self.main_model.set_channel_names(channel_names)

    def select_data_clicked(self):
        pass

    def select_data_events_clicked(self):
        pass

    """
    Tools menu
    """
    # Filtering
    def filter_clicked(self):
        """
        Create the controller for filtering the dataset.
        """
        all_channels_names = self.main_model.get_all_channels_names()
        self.filter_controller = filterController(all_channels_names)
        self.filter_controller.set_listener(self)

    def filter_information(self, low_frequency, high_frequency, channels_selected):
        """
        Create the waiting window while the filtering is done on the dataset.
        :param low_frequency: Lowest frequency from where the data will be filtered.
        :type low_frequency: float
        :param high_frequency: Highest frequency from where the data will be filtered.
        :type high_frequency: float
        :param channels_selected: Channels on which the filtering will be performed.
        :type channels_selected: list of str
        """
        processing_title = "Filtering running, please wait."
        finish_method = "filtering"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.filter(low_frequency, high_frequency, channels_selected)

    def filter_computation_finished(self):
        """
        Close the waiting window when the filtering is done on the dataset.
        """
        processing_title_finished = "Filtering finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def filter_finished(self):
        """
        The filtering is completely done, update the information on the main window.
        """
        dataset_size = self.main_model.get_dataset_size()
        self.main_view.update_dataset_size(dataset_size)

    # Resampling
    def resampling_clicked(self):
        """
        Create the controller for filtering the dataset.
        """
        frequency = self.main_model.get_sampling_frequency()
        self.resampling_controller = resamplingController(frequency)
        self.resampling_controller.set_listener(self)

    def resampling_information(self, frequency):
        """
        Create the waiting window while the resampling is done on the dataset.
        :param frequency: The new frequency at which the data will be resampled.
        :type frequency: int
        """
        processing_title = "Resampling running, please wait."
        finish_method = "resampling"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.resampling(frequency)

    def resampling_computation_finished(self):
        """
        Close the waiting window when the resampling is done on the dataset.
        """
        processing_title_finished = "Resampling finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def resampling_finished(self):
        """
        The resampling is completely done, update the information on the main window.
        """
        frequency = self.main_model.get_sampling_frequency()
        number_of_frames = self.main_model.get_number_of_frames()
        dataset_size = self.main_model.get_dataset_size()
        self.main_view.update_sampling_frequency(frequency)
        self.main_view.update_number_of_frames(number_of_frames)
        self.main_view.update_dataset_size(dataset_size)

    # Re-referencing
    def re_referencing_clicked(self):
        """
        Create the controller for re-referencing the dataset.
        """
        reference = self.main_model.get_reference()
        all_channels_names = self.main_model.get_all_channels_names()
        self.re_referencing_controller = reReferencingController(reference, all_channels_names)
        self.re_referencing_controller.set_listener(self)

    def re_referencing_information(self, references, n_jobs):
        """
        Create the waiting window while the re-referencing is done on the dataset.
        :param references: References from which the data will be re-referenced. Can be a single or multiple channels;
        Can be an average of all channels; Can be a "point to infinity".
        :type references: list of str; str
        :param n_jobs: Number of parallel processes used to compute the re-referencing
        :type n_jobs: int
        """
        subjects_dir = get_project_freesurfer_path()
        if subjects_dir is None and references == "infinity":
            self.download_fsaverage_mne_data_controller = downloadFsaverageMneDataController()
            self.download_fsaverage_mne_data_controller.set_listener(self)
        else:
            processing_title = "Re-referencing running, please wait."
            finish_method = "re-referencing"
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
            self.waiting_while_processing_controller.set_listener(self)
            self.main_model.re_referencing(references, n_jobs)

    def re_referencing_computation_finished(self):
        """
        Close the waiting window when the re-referencing is done on the dataset.
        """
        processing_title_finished = "Re-referencing finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def re_referencing_finished(self):
        """
        The re-referencing is completely done, update the information on the main window.
        """
        references = self.main_model.get_reference()
        self.main_view.update_reference(references)

    # Reject data
    def inspect_reject_data_clicked(self):
        pass

    # ICA decomposition
    def ica_decomposition_clicked(self):
        """
        Create the controller for computing the ICA decomposition on the dataset.
        """
        self.ica_decomposition_controller = icaDecompositionController()
        self.ica_decomposition_controller.set_listener(self)

    def ica_decomposition_information(self, ica_method):
        """
        Create the waiting window while the computation the ICA decomposition is done on the dataset.
        :param ica_method: Method used for performing the ICA decomposition
        :type ica_method: str
        """
        processing_title = "ICA decomposition running, please wait."
        finish_method = "ica_decomposition"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.ica_data_decomposition(ica_method)

    def ica_decomposition_computation_finished(self):
        """
        Close the waiting window when the computation the ICA decomposition is done on the dataset.
        """
        processing_title_finished = "ICA decomposition finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def ica_decomposition_finished(self):
        """
        The computation the ICA decomposition is completely done, update the information on the main window.
        """
        ica_status = self.main_model.get_ica()
        self.main_view.update_ica_decomposition(ica_status)

    # Extract Epochs
    def extract_epochs_clicked(self):
        """
        Create the controller for extracting epochs from the dataset.
        """
        self.extract_epochs_controller = extractEpochsController()
        self.extract_epochs_controller.set_listener(self)

    def extract_epochs_information(self, tmin, tmax):
        """
        Create the waiting window while the extraction of epochs is done on the dataset.
        :param tmin: Start time of the epoch to keep
        :type tmin: float
        :param tmax: End time of the epoch to keep
        :type tmax: float
        """
        processing_title = "Epochs extraction running, please wait."
        finish_method = "extract_epochs"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.extract_epochs(tmin, tmax)

    def extract_epochs_computation_finished(self):
        """
        Close the waiting window when the extraction of epochs is done on the dataset.
        """
        processing_title_finished = "Epochs extraction finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def extract_epochs_finished(self):
        """
        The extraction of epochs is completely done, update the information on the main window.
        """
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

    # Signal-to-noise ratio
    def snr_clicked(self):
        """

        """
        print("SNR")

    # Source Estimation
    def source_estimation_clicked(self):
        """
        Create the controller for computing the source estimation of the dataset.
        """
        subjects_dir = get_project_freesurfer_path()
        if subjects_dir is None:
            self.download_fsaverage_mne_data_controller = downloadFsaverageMneDataController()
            self.download_fsaverage_mne_data_controller.set_listener(self)
        else:
            number_of_epochs = self.main_model.get_number_of_epochs()
            self.source_estimation_controller = sourceEstimationController(number_of_epochs)
            self.source_estimation_controller.set_listener(self)

    def source_estimation_information(self, source_estimation_method, save_data, load_data, epochs_method, trial_number,
                                      n_jobs):
        """
        Create the waiting window while the computation of the source estimation is done on the dataset.
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
        :param trial_number: The trial's number selected for the "single trial" epochs method.
        :type trial_number: int
        :param n_jobs: Number of processes used to compute the source estimation
        :type n_jobs: int
        """
        processing_title = "Source estimation running, please wait."
        finish_method = "source_estimation"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.source_estimation(source_estimation_method, save_data, load_data, epochs_method, trial_number,
                                          n_jobs)

    def source_estimation_computation_finished(self):
        """
        Close the waiting window when the computation of the source estimation is done on the dataset.
        """
        processing_title_finished = "Source estimation finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def source_estimation_computation_error(self):
        """
        Close the waiting window and display an error message because an error occurred during the computation.
        """
        processing_title_finished = "An error as occurred during the computation of the source estimation, please try again."
        self.waiting_while_processing_controller.set_finish_method("error")
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def source_estimation_finished(self):
        """
        The computation of the source estimation is completely done, update the information on the main window.
        """
        source_estimation_data = self.main_model.get_source_estimation_data()
        self.source_estimation_controller.plot_source_estimation(source_estimation_data)

    """
    Plot menu
    """
    def plot_channel_locations_clicked(self):
        """
        Create the controller for plotting the channels' locations of the dataset.
        """
        file_data = self.main_model.get_file_data()
        self.main_view.plot_channel_locations(file_data)

    def plot_data_clicked(self):
        """
        Plot the data of the dataset.
        """
        file_data = self.main_model.get_file_data()
        file_type = self.main_model.get_file_type()
        if file_type == "Raw":
            self.main_view.plot_data(file_data, file_type)
        else:
            event_values = self.main_model.get_event_values()
            event_ids = self.main_model.get_event_ids()
            self.main_view.plot_data(file_data, file_type, events=event_values, event_id=event_ids)

    def plot_topographies_clicked(self):
        """
        Create the controller for plotting the topographies of the dataset.
        """
        self.topographies_controller = topographiesController()
        self.topographies_controller.set_listener(self)

    def plot_topographies_information(self, time_points, mode):
        """
        Plot the topographies of the dataset.
        :param time_points: Time points at which the topographies will be plotted.
        :type time_points: list of float
        :param mode: Mode used for plotting the topographies.
        :type mode: str
        """
        file_data = self.main_model.get_file_data()
        self.main_view.plot_topographies(file_data, time_points, mode)

    # Spectra maps
    def plot_spectra_maps_clicked(self):
        """
        Create the controller for computing the power spectral density of the dataset.
        """
        minimum_time = self.main_model.get_epochs_start()
        maximum_time = self.main_model.get_epochs_end()
        self.power_spectral_density_controller = powerSpectralDensityController(minimum_time, maximum_time)
        self.power_spectral_density_controller.set_listener(self)

    def plot_spectra_maps_information(self, method_psd, minimum_frequency, maximum_frequency, minimum_time, maximum_time):
        """
        Create the waiting window while the computation of the power spectral density is done on the dataset.
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
        processing_title = "PSD running, please wait."
        finish_method = "plot_spectra_maps"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.power_spectral_density(method_psd, minimum_frequency, maximum_frequency, minimum_time, maximum_time)

    def plot_spectra_maps_computation_finished(self):
        """
        Close the waiting window when the computation of the power spectral density is done on the dataset.
        """
        processing_title_finished = "PSD finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def plot_spectra_maps_finished(self):
        """
        The computation of the power spectral density is completely done, plot it.
        """
        psds = self.main_model.get_psds()
        freqs = self.main_model.get_freqs()
        self.power_spectral_density_controller.plot_psd(psds, freqs)

    # ERP Image
    def plot_ERP_image_clicked(self):
        """
        Create the controller for computing the ERP image the dataset.
        """
        all_channels_names = self.main_model.get_all_channels_names()
        self.erp_image_controller = erpImageController(all_channels_names)
        self.erp_image_controller.set_listener(self)

    def plot_ERP_image_information(self, channel_selected):
        """
        The computation of the ERP image is completely done, plot it.
        :param channel_selected: Channel selected for the ERP image.
        :type channel_selected: str
        """
        file_data = self.main_model.get_file_data()
        self.main_view.plot_erp_image(file_data, channel_selected)

    # ERPs
    def plot_ERPs_clicked(self):
        """
        Create the controller for computing the ERPs the dataset.
        """
        all_channels_names = self.main_model.get_all_channels_names()
        self.erp_controller = erpController(all_channels_names)
        self.erp_controller.set_listener(self)

    def plot_ERPs_information(self, channels_selected):
        """
        The computation of the ERPs is completely done, plot it.
        :param channels_selected: Channels selected for the ERP image.
        :type channels_selected: list of str
        """
        file_data = self.main_model.get_file_data()
        self.main_view.plot_erps(file_data, channels_selected)

    # Time frequency
    def plot_time_frequency_clicked(self):
        """
        Create the controller for computing the time-frequency analysis on the dataset.
        """
        all_channels_names = self.main_model.get_all_channels_names()
        self.time_frequency_ersp_itc_controller = timeFrequencyErspItcController(all_channels_names)
        self.time_frequency_ersp_itc_controller.set_listener(self)

    def plot_time_frequency_information(self, method_tfr, channel_selected, min_frequency, max_frequency, n_cycles):
        """
        Create the waiting window while the computation of the time-frequency analysis is done on the dataset.
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
        processing_title = "Time frequency analysis running, please wait."
        finish_method = "time_frequency"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.time_frequency(method_tfr, channel_selected, min_frequency, max_frequency, n_cycles)

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
        self.waiting_while_processing_controller.set_finish_method("error")
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def plot_time_frequency_finished(self):
        """
        The computation of the time-frequency analysis is completely done, plot it.
        """
        channel_selected = self.main_model.get_tfr_channel_selected()
        power = self.main_model.get_power()
        itc = self.main_model.get_itc()
        self.time_frequency_ersp_itc_controller.plot_ersp_itc(channel_selected, power, itc)

    """
    Connectivity menu
    """
    # Envelope correlation
    def envelope_correlation_clicked(self):
        """
        Create the controller for computing the envelope correlation on the dataset.
        """
        number_of_channels = self.main_model.get_number_of_channels()
        self.envelope_correlation_controller = envelopeCorrelationController(number_of_channels)
        self.envelope_correlation_controller.set_listener(self)

    def envelope_correlation_information(self):
        """
        Create the waiting window while the computation of the envelope correlation is done on the dataset.
        """
        processing_title = "Envelope correlation running, please wait."
        finish_method = "envelope_correlation"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.envelope_correlation()

    def envelope_correlation_computation_finished(self):
        """
        Close the waiting window when the computation of the envelope correlation is done on the dataset.
        """
        processing_title_finished = "Envelope correlation finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def envelope_correlation_finished(self):
        """
        The computation of the envelope correlation is completely done, plot it.
        """
        envelope_correlation_data = self.main_model.get_envelope_correlation_data()
        channel_names = self.main_model.get_all_channels_names()
        self.envelope_correlation_controller.plot_envelope_correlation(envelope_correlation_data, channel_names)

    # Source space connectivity
    def source_space_connectivity_clicked(self):
        """
        Create the controller for computing the source space connectivity on the dataset.
        """
        subjects_dir = get_project_freesurfer_path()
        if subjects_dir is None:
            self.download_fsaverage_mne_data_controller = downloadFsaverageMneDataController()
            self.download_fsaverage_mne_data_controller.set_listener(self)
        else:
            number_of_channels = self.main_model.get_number_of_channels()
            self.source_space_connectivity_controller = sourceSpaceConnectivityController(number_of_channels)
            self.source_space_connectivity_controller.set_listener(self)

    def source_space_connectivity_information(self, connectivity_method, spectrum_estimation_method, source_estimation_method,
                                              save_data, load_data, n_jobs):
        """
        Create the waiting window while the computation of the source space connectivity is done on the dataset.
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
        :param n_jobs: Number of processes used to compute the source estimation
        :type n_jobs: int
        """
        processing_title = "Source Space Connectivity running, please wait."
        finish_method = "source_space_connectivity"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.source_space_connectivity(connectivity_method, spectrum_estimation_method, source_estimation_method,
                                                  save_data, load_data, n_jobs)

    def source_space_connectivity_computation_finished(self):
        """
        Close the waiting window when the computation of the source space connectivity is done on the dataset.
        """
        processing_title_finished = "Source Space Connectivity finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def source_space_connectivity_computation_error(self):
        """
        Close the waiting window and display an error message because an error occurred during the computation.
        """
        processing_title_finished = "An error as occurred during the computation of the source space connectivity, please try again."
        self.waiting_while_processing_controller.set_finish_method("error")
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def source_space_connectivity_finished(self):
        """
        The computation of the source space connectivity is completely done, plot it.
        """
        source_space_connectivity_data = self.main_model.get_source_space_connectivity_data()
        self.source_space_connectivity_controller.plot_source_space_connectivity(source_space_connectivity_data)

    # Sensor space connectivity
    def sensor_space_connectivity_clicked(self):
        """
        Create the controller for computing the sensor space connectivity on the dataset.
        """
        file_info = self.main_model.get_file_data().info
        self.sensor_space_connectivity_controller = sensorSpaceConnectivityController(file_info)
        self.sensor_space_connectivity_controller.set_listener(self)

    def sensor_space_connectivity_information(self):
        """
        Create the waiting window while the computation of the sensor space connectivity is done on the dataset.
        """
        processing_title = "Sensor Space Connectivity running, please wait."
        finish_method = "sensor_space_connectivity"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.sensor_space_connectivity()

    def sensor_space_connectivity_computation_finished(self):
        """
        Close the waiting window when the computation of the sensor space connectivity is done on the dataset.
        """
        processing_title_finished = "Sensor Space Connectivity finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def sensor_space_connectivity_finished(self):
        """
        The computation of the sensor space connectivity is completely done, plot it.
        """
        sensor_space_connectivity_data = self.main_model.get_sensor_space_connectivity_data()
        self.sensor_space_connectivity_controller.plot_sensor_space_connectivity(sensor_space_connectivity_data)

    # Spectro temporal connectivity
    def spectro_temporal_connectivity_clicked(self):
        self.spectro_temporal_connectivity_controller = spectroTemporalConnectivityController()
        self.spectro_temporal_connectivity_controller.set_listener(self)

    def spectro_temporal_connectivity_information(self):
        print("Spectro-Temporal Connectivity")

    """
    Classification menu
    """
    def classify_clicked(self):
        """
        Create the controller for classifying the dataset.
        """
        number_of_channels = self.main_model.get_number_of_channels()
        self.classify_controller = classifyController(number_of_channels)
        self.classify_controller.set_listener(self)

    def classify_information(self, pipeline_selected, feature_selection, number_of_channels_to_select, hyper_tuning, cross_val_number):
        """
        Create the waiting window while the classification is done on the dataset.
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
        """
        processing_title = "Classification running, please wait."
        finish_method = "classify"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.classify(pipeline_selected, feature_selection, number_of_channels_to_select, hyper_tuning, cross_val_number)

    def classify_computation_finished(self):
        """
        Close the waiting window when the classification is done on the dataset.
        """
        processing_title_finished = "Classification finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def classify_finished(self):
        """
        The classification is completely done, plot the results.
        """
        classifier = self.main_model.get_classifier()
        self.classify_controller.plot_results(classifier)

    """
    Others
    """
    def display_all_info(self):
        """
        Retrieve all the information that will be displayed on the main window and unlock all the menus.
        """
        all_info = self.main_model.get_all_displayed_info()
        self.main_view.display_info(all_info)
        self.menubar_controller.enable_menu_when_file_loaded()

    def waiting_while_processing_finished(self, finish_method):
        """
        When the waiting window is closed, call the correct method depending on the controller/method that has been called
        earlier.
        :param finish_method: The method to call.
        :type finish_method: str
        """
        if finish_method == "open_fif_file":
            self.open_cnt_file_finished()
        elif finish_method == "open_cnt_file":
            self.open_cnt_file_finished()
        elif finish_method == "open_set_file":
            self.open_set_file_finished()
        elif finish_method == "load_data_info":
            self.load_data_info_finished()
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

    def download_fsaverage_mne_data_information(self):
        """
        Create the waiting window while the download of the fsaverage and sample datasets is done.
        """
        processing_title = "Downloading, please wait."
        finish_method = "downloading"
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, finish_method)
        self.waiting_while_processing_controller.set_listener(self)
        self.download_fsaverage_mne_data_controller.download_fsaverage_mne_data()

    def download_fsaverage_mne_data_computation_finished(self):
        """
        Close the waiting window when the download of the fsaverage and sample datasets is done.
        """
        processing_title_finished = "Download finished. \n You can now use the tools where the source space is needed."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)
