#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

from copy import copy

from main_model import mainModel
from main_view import mainView
from main_listener import mainListener

from menubar.menubar_controller import menubarController

from file.load_data_info.load_data_info_controller import loadDataInfoController
from file.find_events_from_channel.find_events_from_channel_controller import findEventsFromChannelController
from file.study_creation.study_creation_controller import studyCreationController

from edit.dataset_info.dataset_info_controller import datasetInfoController
from edit.event_values.event_values_controller import eventValuesController
from edit.channel_location.channel_location_controller import channelLocationController

from tools.filter.filter_controller import filterController
from tools.resampling.resampling_controller import resamplingController
from tools.re_referencing.re_referencing_controller import reReferencingController
from tools.ICA_decomposition.ICA_decomposition_controller import icaDecompositionController
from tools.extract_epochs.extract_epochs_controller import extractEpochsController
from tools.signal_to_noise_ratio.signal_to_noise_ratio_controller import signalToNoiseRatioController
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

from statistics.statistics_snr.statistics_snr_controller import statisticsSnrController
from statistics.statistics_erp.statistics_erp_controller import statisticsErpController
from statistics.statistics_connectivity.statistics_connectivity_controller import statisticsConnectivityController
from statistics.statistics_ersp_itc.statistics_ersp_itc_controller import statisticsErspItcController
from statistics.statistics_psd.statistics_psd_controller import statisticsPsdController

from study.study_edit_info.study_edit_info_controller import studyEditInfoController
from study.study_plots.study_plots_controller import studyPlotsController

from utils.download_fsaverage_mne_data.download_fsaverage_mne_data_controller import downloadFsaverageMneDataController
from utils.waiting_while_processing.waiting_while_processing_controller import waitingWhileProcessingController
from utils.view.error_window import errorWindow
from utils.view.warning_window import warningWindow
from utils.file_path_search import get_project_freesurfer_path

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class mainController(mainListener):
    def __init__(self, screen_size):
        """
        The main controller is the link between the main model and the main view.
        It will "control" where the information needs to go and who does what.
        All the information for the computation will be directed to the main model, while the information to be displayed
        will be sent to the main view.
        It is responsible for creating the other controllers that will display other windows.
        :param screen_size: Tuple of int corresponding to the size of the screen.
        :type screen_size: QSize
        """
        self.main_model = mainModel()
        self.main_model.set_listener(self)

        self.main_view = mainView()
        self.main_view.resize(0.8 * screen_size.width(), 0.8 * screen_size.height())

        # Menubar
        self.menubar_controller = menubarController()
        self.menubar_controller.set_listener(self)
        self.menubar_view = self.menubar_controller.get_view()
        self.main_view.setMenuBar(self.menubar_view)

        # File
        self.load_data_info_controller = None
        self.find_events_from_channel_controller = None
        self.study_creation_controller = None

        # Edit
        self.dataset_info_controller = None
        self.event_values_controller = None
        self.channel_location_controller = None

        # Tools
        self.filter_controller = None
        self.resampling_controller = None
        self.re_referencing_controller = None
        self.ica_decomposition_controller = None
        self.extract_epochs_controller = None
        self.snr_controller = None
        self.source_estimation_controller = None

        # Plot
        self.power_spectral_density_controller = None
        self.topographies_controller = None
        self.erp_image_controller = None
        self.erp_controller = None
        self.time_frequency_ersp_itc_controller = None

        # Connectivity
        self.envelope_correlation_controller = None
        self.source_space_connectivity_controller = None
        self.sensor_space_connectivity_controller = None
        self.spectro_temporal_connectivity_controller = None

        # Classification
        self.classify_controller = None

        # Statistics
        self.statistics_snr_controller = None
        self.statistics_erp_controller = None
        self.statistics_psd_controller = None
        self.statistics_ersp_itc_controller = None
        self.statistics_connectivity_controller = None

        # Study
        self.study_edit_controller = None
        self.study_plots_controller = None

        # Utils
        self.waiting_while_processing_controller = None
        self.download_fsaverage_mne_data_controller = None

        # Others
        self.study_currently_selected = False
        self.study_indexes_to_compute = None

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
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.open_fif_file_finished)
            self.waiting_while_processing_controller.set_listener(self)
            self.main_model.open_fif_file(path_to_file)

    def open_fif_file_computation_finished(self):
        """
        Close the waiting window when the FIF file is opened.
        """
        processing_title_finished = "FIF file reading finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def open_fif_file_computation_error(self):
        """
        Close the waiting window because the opening of the FIF file had an error.
        """
        processing_title_finished = "The opening of the FIF file had an error."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

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
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.open_cnt_file_finished)
            self.waiting_while_processing_controller.set_listener(self)
            self.main_model.open_cnt_file(path_to_file)

    def open_cnt_file_computation_finished(self):
        """
        Close the waiting window when the CNT file is opened.
        """
        processing_title_finished = "CNT file reading finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def open_cnt_file_computation_error(self):
        """
        Close the waiting window because the opening of the ANT eego CNT file had an error.
        """
        processing_title_finished = "The opening of the ANT eego CNT file had an error."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

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
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.open_set_file_finished)
            self.waiting_while_processing_controller.set_listener(self)
            self.main_model.open_set_file(path_to_file)

    def open_set_file_computation_finished(self):
        """
        Close the waiting window when the SET file is opened.
        """
        processing_title_finished = "SET file reading finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def open_set_file_computation_error(self):
        """
        Close the waiting window because the opening of the SET file had an error.
        """
        processing_title_finished = "The opening of the SET file had an error."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

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

    def load_data_info_information(self, montage, channels_selected, tmin, tmax, dataset_name):
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
        :param dataset_name: The name of the loaded dataset.
        :type dataset_name: str
        """
        processing_title = "Loading selected data info, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.load_data_info_finished)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.load_data_info(montage, channels_selected, tmin, tmax, dataset_name)

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
        study = self.main_model.get_study()
        if study is not None:
            warning_message = "Loading a supplementary dataset will clear the current study, are you sure you want to " \
                              "continue ?"
            warning_window = warningWindow(warning_message, self.load_data_info_confirmed)
            warning_window.set_listener(self)
            warning_window.show()
        else:
            self.load_data_info_confirmed()

    def load_data_info_confirmed(self):
        """
        The loading of more information is confirmed.
        """
        current_dataset_index = self.main_model.get_current_dataset_index()
        dataset_name = self.main_model.get_dataset_name()

        self.main_model.clear_study()
        study_available = False

        self.menubar_controller.add_dataset(current_dataset_index, dataset_name, study_available)
        self.menubar_controller.study_selection_deactivation(study_exist=study_available)

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
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.find_events_from_channel_finished)
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
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def find_events_from_channel_finished(self):
        """
        Display the new information about the events on the main window.
        """
        number_of_events = self.main_model.get_number_of_events()
        self.main_view.update_number_of_events(number_of_events)

    # Export CSV
    def export_data_to_csv_file_clicked(self, path_to_file):
        """
        Check if the path to the file is correct.
        Export the data to a CSV file.
        :param path_to_file: Path to the file.
        :type path_to_file: str
        """
        if path_to_file != '':
            processing_title = "Export data into a CSV file, please wait."
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title)
            self.waiting_while_processing_controller.set_listener(self)
            self.main_model.export_data_to_csv_file_clicked(path_to_file)

    def export_data_csv_computation_finished(self):
        """
        Close the waiting window when the exportation of the data into a CSV file is done.
        """
        processing_title_finished = "Exportation of the data into a CSV file is finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def export_data_csv_computation_error(self):
        """
        Close the waiting window because the exportation of the data into a CSV file had an error.
        """
        processing_title_finished = "The exportation of the data into a CSV file had an error."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    # Export SET
    def export_data_to_set_file_clicked(self, path_to_file):
        """
        Check if the path to the file is correct.
        Export the data to a SET file.
        :param path_to_file: Path to the file.
        :type path_to_file: str
        """
        if path_to_file != '':
            processing_title = "Export data into a SET file, please wait."
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title)
            self.waiting_while_processing_controller.set_listener(self)
            self.main_model.export_data_to_set_file_clicked(path_to_file)

    def export_data_set_computation_finished(self):
        """
        Close the waiting window when the exportation of the data into a SET file is done.
        """
        processing_title_finished = "Exportation of the data into a SET file is finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def export_data_set_computation_error(self):
        """
        Close the waiting window because the exportation of the data into a SET file had an error.
        """
        processing_title_finished = "The exportation of the data into a SET file had an error."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    # Export events
    def export_events_to_file_clicked(self):
        """
        Check if the path to the file is correct.
        Export the events to a TXT file.
        """
        file_type = self.main_model.get_file_type()
        if file_type == "Epochs":
            path_to_file = self.main_view.get_export_path()
            if path_to_file != '':
                processing_title = "Export events into a TXT file, please wait."
                self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title)
                self.waiting_while_processing_controller.set_listener(self)
                self.main_model.export_events_to_file_clicked(path_to_file)
        else:
            error_message = "You can only export events when processing a epochs file."
            error_window = errorWindow(error_message)
            error_window.show()

    def export_events_txt_computation_finished(self):
        """
        Close the waiting window when the exportation of the events of the dataset into a TXT file is done.
        """
        processing_title_finished = "Exportation of the events into a TXT file is finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def export_events_txt_computation_error(self):
        """
        Close the waiting window because the exportation of the data into a TXT file had an error.
        """
        processing_title_finished = "The exportation of the events into a TXT file had an error."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    # Save
    def save_file_clicked(self):
        """
        Save the file into the fif format and display the new path file on the main window.
        """
        if self.main_model.is_fif_file():
            path_to_file = self.main_model.get_file_path_name()
        else:
            path_to_file = self.main_view.get_save_path()
        if path_to_file != '':
            self.main_model.save_file(path_to_file)
            self.main_view.update_path_to_file(self.main_model.get_file_path_name())

    def save_file_as_clicked(self):
        """
        Save the file into the fif format and display the new path file on the main window.
        """
        path_to_file = self.main_view.get_save_path()
        if path_to_file != '':
            self.main_model.save_file_as(path_to_file)
            self.main_view.update_path_to_file(self.main_model.get_file_path_name())

    # Clear dataset
    def clear_dataset_clicked(self):
        """
        Remove the current dataset loaded.
        """
        study = self.main_model.get_study()
        if study is not None:
            warning_message = "Clearing a dataset will clear the current study, are you sure you want to continue ?"
            warning_window = warningWindow(warning_message, self.clear_data_confirmed)
            warning_window.set_listener(self)
            warning_window.show()
        else:
            self.clear_data_confirmed()

    def clear_data_confirmed(self):
        """
        The clearing of the dataset is confirmed.
        """
        current_dataset_index = self.main_model.get_current_dataset_index()

        study_available = False
        self.main_model.clear_study()
        self.menubar_controller.study_selection_deactivation(study_exist=study_available)

        self.menubar_controller.remove_dataset(current_dataset_index, study_available)
        self.main_model.clear_current_dataset()

        new_current_dataset_index = self.main_model.get_current_dataset_index()
        if new_current_dataset_index == -1:     # No dataset loaded
            self.main_view.clear_display()
            self.menubar_controller.disable_menu()
        else:       # Display the new current dataset
            self.main_view.create_display()
            all_info = self.main_model.get_all_displayed_info()
            self.main_view.display_info(all_info)

    # Study
    def create_study_clicked(self):
        """
        Create the controller for retrieving information about the study that is wanted to be created.
        """
        dataset_names = self.main_model.get_all_dataset_names()
        self.study_creation_controller = studyCreationController(dataset_names)
        self.study_creation_controller.set_listener(self)

    def create_study_information(self, study_name, task_name, dataset_names, dataset_indexes, subjects, sessions, runs,
                                 conditions, groups):
        """
        Call the creation of the study with the given parameters.
        :param study_name: The name of the study
        :type study_name: str
        :param task_name: The name of the task linked to the study
        :type task_name: str
        :param dataset_names: All the dataset names
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
        self.main_model.create_study(study_name, task_name, dataset_names, dataset_indexes, subjects, sessions, runs,
                                     conditions, groups)
        # Display the study info
        self.main_view.create_study_display()
        all_info = self.main_model.get_all_study_displayed_info()
        self.main_view.display_study_info(all_info)
        # Enable the menu
        self.menubar_controller.study_selection_activation()

    def clear_study_clicked(self):
        """
        Remove the current study loaded.
        """
        self.main_model.clear_study()
        self.menubar_controller.study_selection_deactivation(study_exist=False)

        current_dataset_index = self.main_model.get_current_dataset_index()
        if current_dataset_index == -1:     # No dataset loaded
            self.main_view.clear_display()
            self.menubar_controller.disable_menu()
        else:       # Display the current dataset
            self.main_view.create_display()
            all_info = self.main_model.get_all_displayed_info()
            self.main_view.display_info(all_info)

    """
    Edit menu
    """
    # Dataset info
    def dataset_info_clicked(self):
        """
        Create the controller for displaying some information about the dataset.
        """
        all_channels_names = self.main_model.get_all_channels_names()
        self.dataset_info_controller = datasetInfoController(all_channels_names)
        self.dataset_info_controller.set_listener(self)

    def dataset_info_information(self, channels_selected):
        """
        Change the information that have been modified by the user manually.
        :param channels_selected:
        :type channels_selected:
        """
        self.main_model.set_reference(channels_selected)
        reference = self.main_model.get_reference()
        self.main_view.update_reference(reference)

    # Event values
    def event_values_clicked(self):
        """
        Create the controller for displaying information about the event of the dataset.
        Display an error message if the dataset is a "Raw" dataset, because only "Epochs" dataset have events.
        """
        event_values = self.main_model.get_event_values()
        number_of_events = self.main_model.get_number_of_events()
        if event_values is not None and number_of_events != 0:
            file_type = self.main_model.get_file_type()
            event_values = self.main_model.get_event_values()
            event_ids = self.main_model.get_event_ids()
            number_of_epochs = self.main_model.get_number_of_epochs()
            number_of_frames = self.main_model.get_number_of_frames()
            self.event_values_controller = eventValuesController(file_type, event_values, event_ids, number_of_epochs,
                                                                 number_of_frames)
            self.event_values_controller.set_listener(self)
        else:
            error_message = "It seems like no events are loaded from the dataset. " \
                            "Please try to read the events from a channel or a file under the 'file' menu or work with" \
                            "an epoched dataset."
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

    # Channel location
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
        self.main_model.set_channel_names(channel_names)
        self.main_model.set_channel_locations(channel_locations, channel_names)

    # Select data
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

    def filter_information(self, low_frequency, high_frequency, channels_selected, filter_method):
        """
        Create the waiting window while the filtering is done on the dataset.
        :param low_frequency: Lowest frequency from where the data will be filtered.
        :type low_frequency: float
        :param high_frequency: Highest frequency from where the data will be filtered.
        :type high_frequency: float
        :param channels_selected: Channels on which the filtering will be performed.
        :type channels_selected: list of str
        :param filter_method: Method used for the filtering, either FIR or IIR.
        :type filter_method: str
        """
        processing_title = "Filtering running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.filter_finished)
        self.waiting_while_processing_controller.set_listener(self)

        self.study_currently_selected = self.main_model.get_study_selected()
        if self.study_currently_selected:
            self.study_indexes_to_compute = copy(self.main_model.get_study().get_dataset_indexes())
            self.filter_computation(low_frequency, high_frequency, channels_selected, filter_method,
                                    self.study_indexes_to_compute[0])
            del self.study_indexes_to_compute[0]
        else:
            self.filter_computation(low_frequency, high_frequency, channels_selected, filter_method)

    def filter_computation(self, low_frequency, high_frequency, channels_selected, filter_method, index=None):
        """
        Call the model to perform the filtering on the chosen dataset.
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
        self.main_model.filter(low_frequency, high_frequency, channels_selected, filter_method, index)

    def filter_computation_finished(self, low_frequency=None, high_frequency=None, channels_selected=None,
                                    filter_method=None):
        """
        Close the waiting window when the filtering is done on the dataset.
        :param low_frequency: Lowest frequency from where the data will be filtered.
        :type low_frequency: float
        :param high_frequency: Highest frequency from where the data will be filtered.
        :type high_frequency: float
        :param channels_selected: Channels on which the filtering will be performed.
        :type channels_selected: list of str
        :param filter_method: Method used for the filtering, either FIR or IIR.
        :type filter_method: str
        """
        if self.study_currently_selected:
            if len(self.study_indexes_to_compute) == 0:     # All study computation done
                processing_title_finished = "Filtering finished."
                self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)
            else:
                self.filter_computation(low_frequency, high_frequency, channels_selected, filter_method,
                                        self.study_indexes_to_compute[0])
                del self.study_indexes_to_compute[0]
        else:
            processing_title_finished = "Filtering finished."
            self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def filter_computation_error(self):
        """
        Close the waiting window because the filtering had an error.
        """
        processing_title_finished = "The filtering had an error."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def filter_finished(self):
        """
        The filtering is completely done, update the information on the main window.
        """
        if self.study_currently_selected:
            all_info = self.main_model.get_all_study_displayed_info()
            self.main_view.display_study_info(all_info)
        else:
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
        Create the waiting window while the resampling is done on the dataset or the study.
        :param frequency: The new frequency at which the data will be resampled.
        :type frequency: int
        """
        processing_title = "Resampling running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.resampling_finished)
        self.waiting_while_processing_controller.set_listener(self)

        self.study_currently_selected = self.main_model.get_study_selected()
        if self.study_currently_selected:
            self.study_indexes_to_compute = copy(self.main_model.get_study().get_dataset_indexes())
            self.resampling_computation(frequency, self.study_indexes_to_compute[0])
            del self.study_indexes_to_compute[0]
        else:
            self.resampling_computation(frequency)

    def resampling_computation(self, frequency, index=None):
        """
        Call the model to do the resampling.
        :param frequency: The new frequency at which the data will be resampled.
        :type frequency: int
        :param index: The index of the dataset of the study.
        :type index: int
        """
        self.main_model.resampling(frequency, index)

    def resampling_computation_finished(self, frequency=None):
        """
        Close the waiting window when the resampling is done on the dataset.
        :param frequency: The new frequency at which the data will be resampled.
        :type frequency: int
        """
        if self.study_currently_selected:
            if len(self.study_indexes_to_compute) == 0:     # All study computation done
                processing_title_finished = "Resampling finished."
                self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)
            else:
                self.resampling_computation(frequency, self.study_indexes_to_compute[0])
                del self.study_indexes_to_compute[0]
        else:
            processing_title_finished = "Resampling finished."
            self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def resampling_computation_error(self):
        """
        Close the waiting window because the resampling had an error.
        """
        processing_title_finished = "The resampling had an error."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def resampling_finished(self):
        """
        The resampling is completely done, update the information on the main window.
        """
        if self.study_currently_selected:
            all_info = self.main_model.get_all_study_displayed_info()
            self.main_view.display_study_info(all_info)
        else:
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

    def re_referencing_information(self, references, save_data, load_data, n_jobs):
        """
        Create the waiting window while the re-referencing is done on the dataset.
        :param references: References from which the data will be re-referenced. Can be a single or multiple channels;
        Can be an average of all channels; Can be a "point to infinity".
        :type references: list of str; str
        :param save_data: Boolean telling if the data computed must be saved into files.
        :type save_data: bool
        :param load_data: Boolean telling if the data used for the computation can be read from computer files.
        :type load_data: bool
        :param n_jobs: Number of parallel processes used to compute the re-referencing
        :type n_jobs: int
        """
        subjects_dir = get_project_freesurfer_path()
        if subjects_dir is None and references == "infinity":
            self.download_fsaverage_mne_data_controller = downloadFsaverageMneDataController()
            self.download_fsaverage_mne_data_controller.set_listener(self)
        else:
            processing_title = "Re-referencing running, please wait."
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.re_referencing_finished)
            self.waiting_while_processing_controller.set_listener(self)

            self.study_currently_selected = self.main_model.get_study_selected()
            if self.study_currently_selected:
                self.study_indexes_to_compute = copy(self.main_model.get_study().get_dataset_indexes())
                self.re_referencing_computation(references, save_data, load_data, n_jobs, self.study_indexes_to_compute[0])
                del self.study_indexes_to_compute[0]
            else:
                self.re_referencing_computation(references, save_data, load_data, n_jobs)

    def re_referencing_computation(self, references, save_data, load_data, n_jobs, index=None):
        """
        Call the model to do the re-referencing.
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
        self.main_model.re_referencing(references, save_data, load_data, n_jobs, index)

    def re_referencing_computation_finished(self, references=None, save_data=None, load_data=None, n_jobs=None):
        """
        Close the waiting window when the re-referencing is done on the dataset.
        :param references: References from which the data will be re-referenced. Can be a single or multiple channels;
        Can be an average of all channels; Can be a "point to infinity".
        :type references: list of str; str
        :param save_data: Boolean telling if the data computed must be saved into files.
        :type save_data: bool
        :param load_data: Boolean telling if the data used for the computation can be read from computer files.
        :type load_data: bool
        :param n_jobs: Number of parallel processes used to compute the re-referencing
        :type n_jobs: int
        """
        if self.study_currently_selected:
            if len(self.study_indexes_to_compute) == 0:     # All study computation done
                processing_title_finished = "Re-referencing finished."
                self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)
            else:
                self.re_referencing_computation(references, save_data, load_data, n_jobs, self.study_indexes_to_compute[0])
                del self.study_indexes_to_compute[0]
        else:
            processing_title_finished = "Re-referencing finished."
            self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)
        
    def re_referencing_computation_error(self):
        """
        Close the waiting window because the re-referencing had an error.
        """
        processing_title_finished = "Re-referencing had an error."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def re_referencing_finished(self):
        """
        The re-referencing is completely done, update the information on the main window.
        """
        if self.study_currently_selected:
            all_info = self.main_model.get_all_study_displayed_info()
            self.main_view.display_study_info(all_info)
        else:
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
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.ica_decomposition_finished)
        self.waiting_while_processing_controller.set_listener(self)

        self.study_currently_selected = self.main_model.get_study_selected()
        if self.study_currently_selected:
            self.study_indexes_to_compute = copy(self.main_model.get_study().get_dataset_indexes())
            self.ica_decomposition_computation(ica_method, self.study_indexes_to_compute[0])
            del self.study_indexes_to_compute[0]
        else:
            self.ica_decomposition_computation(ica_method)

    def ica_decomposition_computation(self, ica_method, index=None):
        """
        Call the model for computing the ica decomposition on the chosen dataset.
        :param ica_method: Method used for performing the ICA decomposition
        :type ica_method: str
        :param index: The index of the dataset of the study.
        :type index: int
        """
        self.main_model.ica_data_decomposition(ica_method, index)

    def ica_data_decomposition_computation_finished(self, ica_method=None):
        """
        Close the waiting window when the computation the ICA decomposition is done on the dataset.
        :param ica_method: Method used for performing the ICA decomposition
        :type ica_method: str
        """
        if self.study_currently_selected:
            if len(self.study_indexes_to_compute) == 0:     # All study computation done
                processing_title_finished = "ICA decomposition finished."
                self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)
            else:
                self.ica_decomposition_computation(ica_method, self.study_indexes_to_compute[0])
                del self.study_indexes_to_compute[0]
        else:
            processing_title_finished = "ICA decomposition finished."
            self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def ica_data_decomposition_computation_error(self):
        """
        Close the waiting window because the ICA decomposition had an error.
        """
        processing_title_finished = "ICA decomposition had an error."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def ica_decomposition_finished(self):
        """
        The computation the ICA decomposition is completely done, update the information on the main window.
        """
        if self.study_currently_selected:
            all_info = self.main_model.get_all_study_displayed_info()
            self.main_view.display_study_info(all_info)
        else:
            ica_status = self.main_model.get_ica()
            self.main_view.update_ica_decomposition(ica_status)

    # Extract Epochs
    def extract_epochs_clicked(self):
        """
        Create the controller for extracting epochs from the dataset.
        """
        file_type = self.main_model.get_file_type()
        if file_type == "Raw":
            read_events = self.main_model.get_read_events()
            number_of_events = self.main_model.get_number_of_events()
            if read_events is not None and number_of_events != 0:
                event_values = self.main_model.get_event_values()
                event_ids = self.main_model.get_event_ids()
                self.extract_epochs_controller = extractEpochsController(event_values, event_ids)
                self.extract_epochs_controller.set_listener(self)
            else:
                error_message = "It seems like no events are loaded from the dataset. " \
                                "Please try to read the events from a channel or a file under the 'file' menu, before " \
                                "extracting the epochs"
                error_window = errorWindow(error_message)
                error_window.show()
        else:
            error_message = "You can not extract epochs when you already are in an epoched file"
            error_window = errorWindow(error_message)
            error_window.show()

    def extract_epochs_information(self, tmin, tmax, trials_selected):
        """
        Create the waiting window while the extraction of epochs is done on the dataset.
        :param tmin: Start time of the epoch to keep
        :type tmin: float
        :param tmax: End time of the epoch to keep
        :type tmax: float
        :param trials_selected: The indexes of the trials selected for the computation
        :type trials_selected: list of int
        """
        processing_title = "Epochs extraction running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.extract_epochs_finished)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.extract_epochs(tmin, tmax, trials_selected)

    def extract_epochs_computation_finished(self):
        """
        Close the waiting window when the extraction of epochs is done on the dataset.
        """
        processing_title_finished = "Epochs extraction finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def extract_epochs_computation_error(self):
        """
        Close the waiting window because the extraction of epochs had an error.
        """
        processing_title_finished = "Epochs extraction had an error."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

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
        Create the controller for computation the SNR from the dataset.
        """
        all_channels_names = self.main_model.get_all_channels_names()
        event_values = self.main_model.get_event_values()
        event_ids = self.main_model.get_event_ids()
        self.snr_controller = signalToNoiseRatioController(all_channels_names, event_values, event_ids)
        self.snr_controller.set_listener(self)

    def snr_information(self, snr_methods, source_method, read, write, picks, trials_selected):
        """
        Create the waiting window while the SNR computation is done on the dataset.
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
        :param trials_selected: The indexes of the trials selected for the computation
        :type trials_selected: list of int
        """
        processing_title = "SNR running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title,
                                                                                    self.snr_finished)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.signal_to_noise_ratio(snr_methods, source_method, read, write, picks, trials_selected)

    def snr_computation_finished(self):
        """
        Close the waiting window when the computation of the SNR is done on the dataset.
        """
        processing_title_finished = "SNR computation finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def snr_computation_error(self):
        """
        Close the waiting window because the computation of the SNR had an error.
        """
        processing_title_finished = "SNR computation had an error."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def snr_finished(self):
        """
        The computation of the SNR is completely done, plot the results.
        """
        SNRs = self.main_model.get_SNRs()
        SNR_methods = self.main_model.get_SNR_methods()
        self.snr_controller.plot_SNRs(SNRs, SNR_methods)

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
            file_type = self.main_model.get_file_type()
            if file_type == "Epochs":
                number_of_epochs = self.main_model.get_number_of_epochs()
                event_values = self.main_model.get_event_values()
                event_ids = self.main_model.get_event_ids()
                tmin = self.main_model.get_epochs_start()
                tmax = self.main_model.get_epochs_end()
                self.source_estimation_controller = sourceEstimationController(number_of_epochs, event_values, event_ids,
                                                                               tmin, tmax)
                self.source_estimation_controller.set_listener(self)
            else:
                error_message = "You can not compute the source estimation on a raw file"
                error_window = errorWindow(error_message)
                error_window.show()

    def source_estimation_information(self, source_estimation_method, save_data, load_data, epochs_method, trials_selected,
                                      tmin, tmax, n_jobs, export_path):
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
        :type epochs_method: str
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
        processing_title = "Source estimation running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.source_estimation_finished)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.source_estimation(source_estimation_method, save_data, load_data, epochs_method, trials_selected,
                                          tmin, tmax, n_jobs, export_path)

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
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def source_estimation_finished(self):
        """
        The computation of the source estimation is completely done, update the information on the main window.
        """
        source_estimation_data = self.main_model.get_source_estimation_data()
        self.source_estimation_controller.plot_source_estimation(source_estimation_data)

    """
    Plot menu
    """
    # Plot channel locations
    def plot_channel_locations_clicked(self):
        """
        Create the controller for plotting the channels' locations of the dataset.
        """
        file_data = self.main_model.get_file_data()
        self.main_view.plot_channel_locations(file_data)

    # Plot data
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

    # Topographies
    def plot_topographies_clicked(self):
        """
        Create the controller for plotting the topographies of the dataset.
        """
        file_type = self.main_model.get_file_type()
        if file_type == "Epochs":
            self.topographies_controller = topographiesController()
            self.topographies_controller.set_listener(self)
        else:
            error_message = "You can not compute the topographies on a raw file"
            error_window = errorWindow(error_message)
            error_window.show()

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
        file_type = self.main_model.get_file_type()
        if file_type == "Epochs":
            minimum_time = self.main_model.get_epochs_start()
            maximum_time = self.main_model.get_epochs_end()
            self.power_spectral_density_controller = powerSpectralDensityController(minimum_time, maximum_time)
            self.power_spectral_density_controller.set_listener(self)
        else:
            error_message = "You can not compute the PSD on a raw file"
            error_window = errorWindow(error_message)
            error_window.show()

    def plot_spectra_maps_information(self, minimum_frequency, maximum_frequency, minimum_time, maximum_time, topo_time_points):
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
        self.main_model.power_spectral_density(minimum_frequency, maximum_frequency, minimum_time, maximum_time, topo_time_points)

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
        psd_fig = self.main_model.get_psd_fig()
        topo_fig = self.main_model.get_psd_topo_fig()
        self.power_spectral_density_controller.plot_psd(psd_fig, topo_fig)

    # ERP Image
    def plot_ERP_image_clicked(self):
        """
        Create the controller for computing the ERP image the dataset.
        """
        file_type = self.main_model.get_file_type()
        if file_type == "Epochs":
            all_channels_names = self.main_model.get_all_channels_names()
            self.erp_image_controller = erpImageController(all_channels_names)
            self.erp_image_controller.set_listener(self)
        else:
            error_message = "You can not compute the ERP image on a raw file"
            error_window = errorWindow(error_message)
            error_window.show()

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
        file_type = self.main_model.get_file_type()
        if file_type == "Epochs":
            all_channels_names = self.main_model.get_all_channels_names()
            self.erp_controller = erpController(all_channels_names)
            self.erp_controller.set_listener(self)
        else:
            error_message = "You can not compute the ERPs on a raw file"
            error_window = errorWindow(error_message)
            error_window.show()

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
        file_type = self.main_model.get_file_type()
        if file_type == "Epochs":
            all_channels_names = self.main_model.get_all_channels_names()
            self.time_frequency_ersp_itc_controller = timeFrequencyErspItcController(all_channels_names)
            self.time_frequency_ersp_itc_controller.set_listener(self)
        else:
            error_message = "You can not compute the ERSP-ITC on a raw file"
            error_window = errorWindow(error_message)
            error_window.show()

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
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.plot_time_frequency_finished)
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
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

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
        file_data = self.main_model.get_file_data()
        self.envelope_correlation_controller = envelopeCorrelationController(number_of_channels, file_data)
        self.envelope_correlation_controller.set_listener(self)

    def envelope_correlation_information(self, psi, fmin, fmax, connectivity_method, n_jobs, export_path):
        """
        Create the waiting window while the computation of the envelope correlation is done on the dataset.
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
        processing_title = "Envelope correlation running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.envelope_correlation_finished)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.envelope_correlation(psi, fmin, fmax, connectivity_method, n_jobs, export_path)

    def envelope_correlation_computation_finished(self):
        """
        Close the waiting window when the computation of the envelope correlation is done on the dataset.
        """
        processing_title_finished = "Envelope correlation finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def envelope_correlation_computation_error(self):
        """
        Close the waiting window and display an error message because an error occurred during the computation.
        """
        processing_title_finished = "An error as occurred during the computation of the envelope correlation, please try again."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def envelope_correlation_finished(self):
        """
        The computation of the envelope correlation is completely done, plot it.
        """
        envelope_correlation_data = self.main_model.get_envelope_correlation_data()
        psi = self.main_model.get_psi_data_envelope_correlation()
        channel_names = self.main_model.get_all_channels_names()
        self.envelope_correlation_controller.plot_envelope_correlation(envelope_correlation_data, psi, channel_names)

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
                                              save_data, load_data, n_jobs, export_path, psi, fmin, fmax):
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
        processing_title = "Source Space Connectivity running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.source_space_connectivity_finished)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.source_space_connectivity(connectivity_method, spectrum_estimation_method, source_estimation_method,
                                                  save_data, load_data, n_jobs, export_path, psi, fmin, fmax)

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
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def source_space_connectivity_finished(self):
        """
        The computation of the source space connectivity is completely done, plot it.
        """
        source_space_connectivity_data = self.main_model.get_source_space_connectivity_data()
        psi = self.main_model.get_psi_data_source_space()
        self.source_space_connectivity_controller.plot_source_space_connectivity(source_space_connectivity_data, psi)

    # Sensor space connectivity
    def sensor_space_connectivity_clicked(self):
        """
        Create the controller for computing the sensor space connectivity on the dataset.
        """
        file_info = self.main_model.get_file_data().info
        self.sensor_space_connectivity_controller = sensorSpaceConnectivityController(file_info)
        self.sensor_space_connectivity_controller.set_listener(self)

    def sensor_space_connectivity_information(self, export_path):
        """
        Create the waiting window while the computation of the sensor space connectivity is done on the dataset.
        :param export_path: Path where the sensor space connectivity data will be stored.
        :type export_path: str
        """
        processing_title = "Sensor Space Connectivity running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.sensor_space_connectivity_finished)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.sensor_space_connectivity(export_path)

    def sensor_space_connectivity_computation_finished(self):
        """
        Close the waiting window when the computation of the sensor space connectivity is done on the dataset.
        """
        processing_title_finished = "Sensor Space Connectivity finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def sensor_space_connectivity_computation_error(self):
        """
        Close the waiting window and display an error message because an error occurred during the computation.
        """
        processing_title_finished = "An error as occurred during the computation of the sensor space connectivity, please try again."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

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
        event_values = self.main_model.get_event_values()
        event_ids = self.main_model.get_event_ids()
        self.classify_controller = classifyController(number_of_channels, event_values, event_ids)
        self.classify_controller.set_listener(self)

    def classify_information(self, pipeline_selected, feature_selection, number_of_channels_to_select, hyper_tuning,
                             cross_val_number, trials_selected):
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
        :param trials_selected: The indexes of the trials selected for the computation
        :type trials_selected: list of int
        """
        processing_title = "Classification running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title, self.classify_finished)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.classify(pipeline_selected, feature_selection, number_of_channels_to_select, hyper_tuning,
                                 cross_val_number, trials_selected)

    def classify_computation_finished(self):
        """
        Close the waiting window when the classification is done on the dataset.
        """
        processing_title_finished = "Classification finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def classify_computation_error(self):
        """
        Close the waiting window and display an error message because an error occurred during the computation.
        """
        processing_title_finished = "An error as occurred during the computation of the classification, please try again."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def classify_finished(self):
        """
        The classification is completely done, plot the results.
        """
        classifier = self.main_model.get_classifier()
        self.classify_controller.plot_results(classifier)

    """
    Statistics Menu
    """
    # SNR
    def statistics_snr_clicked(self):
        """
        Create the controller for computing the SNR from the dataset and the statistics on specified data.
        """
        all_channels_names = self.main_model.get_all_channels_names()
        event_values = self.main_model.get_event_values()
        event_ids = self.main_model.get_event_ids()
        self.statistics_snr_controller = statisticsSnrController(all_channels_names, event_values, event_ids)
        self.statistics_snr_controller.set_listener(self)

    def statistics_snr_information(self, snr_methods, source_method, read, write, picks, stats_first_variable, stats_second_variable):
        """
        Create the waiting window while the SNR computation and the statistics is done on the dataset.
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
        processing_title = "SNR running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title,
                                                                                    self.statistics_snr_finished)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.statistics_snr(snr_methods, source_method, read, write, picks, stats_first_variable, stats_second_variable)

    def statistics_snr_computation_finished(self):
        """
        Close the waiting window when the computation of the SNR and the statistics are done on the dataset.
        """
        processing_title_finished = "SNR computation finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def statistics_snr_computation_error(self):
        """
        Close the waiting window because the computation of the SNR and the statistics had an error.
        """
        processing_title_finished = "SNR computation had an error."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def statistics_snr_finished(self):
        """
        The computation of the SNR and the statistics are completely done, plot the results.
        """
        first_SNRs = self.main_model.get_statistics_first_SNRs()
        second_SNRs = self.main_model.get_statistics_second_SNRs()
        t_values = self.main_model.get_statistics_SNR_t_values()
        SNR_methods = self.main_model.get_statistics_SNR_methods()
        self.statistics_snr_controller.plot_SNRs(first_SNRs, second_SNRs, t_values, SNR_methods)

    # ERP
    def statistics_erp_clicked(self):
        """
        Create the controller for computing the ERPs the dataset.
        """
        all_channels_names = self.main_model.get_all_channels_names()
        event_ids = self.main_model.get_event_ids()
        self.statistics_erp_controller = statisticsErpController(all_channels_names, event_ids)
        self.statistics_erp_controller.set_listener(self)

    def statistics_erp_information(self, channels_selected, stats_first_variable, stats_second_variable):
        """
        The computation of the ERPs is completely done, plot it.
        :param channels_selected: Channels selected for the ERP.
        :type channels_selected: list of str
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        file_data = self.main_model.get_file_data()
        self.statistics_erp_controller.plot_erps(channels_selected, file_data, stats_first_variable, stats_second_variable)

    # PSD
    def statistics_psd_clicked(self):
        """
        Create the controller for computing the power spectral density and the statistics of the dataset.
        """
        minimum_time = self.main_model.get_epochs_start()
        maximum_time = self.main_model.get_epochs_end()
        event_ids = self.main_model.get_event_ids()
        all_channels_names = self.main_model.get_all_channels_names()
        self.statistics_psd_controller = statisticsPsdController(minimum_time, maximum_time, event_ids, all_channels_names)
        self.statistics_psd_controller.set_listener(self)

    def statistics_psd_information(self, minimum_frequency, maximum_frequency, minimum_time, maximum_time, topo_time_points,
                                   channel_selected, stats_first_variable, stats_second_variable):
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
        :param channel_selected: Channel selected for the ERP.
        :type channel_selected: str
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        processing_title = "PSD running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title,
                                                                                    self.statistics_psd_finished)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.statistics_psd(minimum_frequency, maximum_frequency, minimum_time, maximum_time, topo_time_points,
                                       channel_selected, stats_first_variable, stats_second_variable)

    def statistics_psd_computation_finished(self):
        """
        Close the waiting window when the computation of the power spectral density is done on the dataset.
        """
        processing_title_finished = "PSD finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def statistics_psd_computation_error(self):
        """
        Close the waiting window when the computation of the power spectral density is done on the dataset.
        """
        processing_title_finished = "An error has occurred during the computation of the PSD"
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def statistics_psd_finished(self):
        """
        The computation of the power spectral density is completely done, plot it.
        """
        psd_fig_one = self.main_model.get_statistics_psd_fig_one()
        topo_fig_one = self.main_model.get_statistics_psd_topo_fig_one()
        psd_fig_two = self.main_model.get_statistics_psd_fig_two()
        topo_fig_two = self.main_model.get_statistics_psd_topo_fig_two()
        self.statistics_psd_controller.plot_psd(psd_fig_one, topo_fig_one, psd_fig_two, topo_fig_two)

    # ERSP ITC
    def statistics_ersp_itc_clicked(self):
        """
        Create the controller for computing the time-frequency analysis and the statistics on the dataset.
        """
        all_channels_names = self.main_model.get_all_channels_names()
        event_ids = self.main_model.get_event_ids()
        self.statistics_ersp_itc_controller = statisticsErspItcController(all_channels_names, event_ids)
        self.statistics_ersp_itc_controller.set_listener(self)

    def statistics_ersp_itc_information(self, method_tfr, channel_selected, min_frequency, max_frequency, n_cycles,
                                        stats_first_variable, stats_second_variable):
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
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        processing_title = "Time frequency analysis running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title,
                                                                                    self.statistics_ersp_itc_finished)
        self.waiting_while_processing_controller.set_listener(self)
        self.main_model.statistics_ersp_itc(method_tfr, channel_selected, min_frequency, max_frequency, n_cycles,
                                            stats_first_variable, stats_second_variable)

    def statistics_ersp_itc_computation_finished(self):
        """
        Close the waiting window when the computation of the time-frequency analysis is done on the dataset.
        """
        processing_title_finished = "Time frequency analysis finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def statistics_ersp_itc_computation_error(self):
        """
        Close the waiting window and display an error message because an error occurred during the computation.
        """
        processing_title_finished = "An error as occurred during the time frequency analysis, please try again."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def statistics_ersp_itc_finished(self):
        """
        The computation of the time-frequency analysis is completely done, plot it.
        """
        channel_selected = self.main_model.get_statistics_ersp_itc_channel_selected()
        power_one = self.main_model.get_statistics_power_one()
        itc_one = self.main_model.get_statistics_itc_one()
        power_two = self.main_model.get_statistics_power_two()
        itc_two = self.main_model.get_statistics_itc_two()
        self.statistics_ersp_itc_controller.plot_ersp_itc(channel_selected, power_one, itc_one, power_two, itc_two)

    # Connectivity
    def statistics_connectivity_clicked(self):
        """
        Create the controller for computing the envelope correlation and the statistics on the dataset.
        """
        number_of_channels = self.main_model.get_number_of_channels()
        file_data = self.main_model.get_file_data()
        event_ids = self.main_model.get_event_ids()
        self.statistics_connectivity_controller = statisticsConnectivityController(number_of_channels, file_data, event_ids)
        self.statistics_connectivity_controller.set_listener(self)

    def statistics_connectivity_information(self, psi, fmin, fmax, connectivity_method, n_jobs, export_path, stats_first_variable,
                                            stats_second_variable):
        """
        Create the waiting window while the computation of the envelope correlation is done on the dataset.
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
        print("Statistics Connectivity")
        try:
            processing_title = "Envelope correlation running, please wait."
            self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title,
                                                                                        self.statistics_connectivity_finished)
            self.waiting_while_processing_controller.set_listener(self)
            self.main_model.statistics_connectivity(psi, fmin, fmax, connectivity_method, n_jobs, export_path, stats_first_variable,
                                                    stats_second_variable)
        except Exception as e:
            print(e)

    def statistics_connectivity_computation_finished(self):
        """
        Close the waiting window when the computation of the envelope correlation is done on the dataset.
        """
        processing_title_finished = "Envelope correlation finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def statistics_connectivity_computation_error(self):
        """
        Close the waiting window and display an error message because an error occurred during the computation.
        """
        processing_title_finished = "An error as occurred during the computation of the envelope correlation, please try again."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished, error=True)

    def statistics_connectivity_finished(self):
        """
        The computation of the envelope correlation is completely done, plot it.
        """
        connectivity_data_one = self.main_model.get_statistics_connectivity_data_one()
        psi_data_one = self.main_model.get_statistics_psi_data_one()
        connectivity_data_two = self.main_model.get_statistics_connectivity_data_two()
        psi_data_two = self.main_model.get_statistics_psi_data_two()
        channel_names = self.main_model.get_all_channels_names()
        self.statistics_connectivity_controller.plot_envelope_correlation(connectivity_data_one, connectivity_data_two,
                                                                          psi_data_one, psi_data_two, channel_names)

    """
    Study Menu
    """
    def edit_study_clicked(self):
        """
        Create the controller for editing the study.
        """
        study = self.main_model.get_study()
        self.study_edit_controller = studyEditInfoController(study)
        self.study_edit_controller.set_listener(self)

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
        self.main_model.edit_study_information(study_name, task_name, subjects, sessions, runs, conditions, groups)
        # Display the study info
        all_info = self.main_model.get_all_study_displayed_info()
        self.main_view.display_study_info(all_info)

    # Study Plots
    def plot_study_clicked(self):
        """
        Create the controller for plotting the study.
        """
        all_file_type = self.main_model.get_all_file_type()
        study = self.main_model.get_study()
        file_type_all_epochs = study.check_file_type_all_epochs(all_file_type)
        if file_type_all_epochs:      # The file types in the study are all epochs,
            self.study_plots_controller = studyPlotsController(study)
            self.study_plots_controller.set_listener(self)
        else:
            error_message = "There is at least one dataset in the study that is not epoched, it is not possible to " \
                            "compute the plots on this study."
            error_window = errorWindow(error_message)
            error_window.show()

    """
    Dataset Menu
    """
    def change_dataset(self, index_selected):
        """
        Change the dataset selected and display the corresponding information.
        :param index_selected: The index of the dataset selected.
        :type index_selected: int
        """
        self.main_model.set_current_dataset_index(index_selected)
        self.main_view.create_display()
        all_info = self.main_model.get_all_displayed_info()
        self.main_view.display_info(all_info)

    def study_selected(self):
        """
        Select the current study and display the corresponding information.
        """
        self.main_model.set_study_selected()
        self.main_view.create_study_display()
        all_info = self.main_model.get_all_study_displayed_info()
        self.main_view.display_study_info(all_info)

    """
    Others
    """
    def show(self):
        """
        Shows the main view.
        """
        self.main_view.show()

    def display_all_info(self):
        """
        Retrieve all the information that will be displayed on the main window and unlock all the menus.
        """
        all_info = self.main_model.get_all_displayed_info()
        self.main_view.create_display()
        self.main_view.display_info(all_info)
        self.menubar_controller.enable_menu()

    # Download fsaverage
    def download_fsaverage_mne_data_information(self):
        """
        Create the waiting window while the download of the fsaverage and sample datasets is done.
        """
        processing_title = "Downloading, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title)
        self.waiting_while_processing_controller.set_listener(self)
        self.download_fsaverage_mne_data_controller.download_fsaverage_mne_data()

    def download_fsaverage_mne_data_computation_finished(self):
        """
        Close the waiting window when the download of the fsaverage and sample datasets is done.
        """
        processing_title_finished = "Download finished. \n You can now use the tools where the source space is needed."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    """
    Getters
    """
    def get_main_view(self):
        """
        Gets the main view.
        :return: The main view
        :rtype: mainView
        """
        return self.main_view
