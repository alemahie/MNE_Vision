#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

from PyQt5.QtWidgets import QMenuBar, QMenu, QFileDialog, QAction

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class menubarView(QMenuBar):
    def __init__(self):
        """
        Displays the menubar on the top of the main window.
        """
        super().__init__()
        self.menubar_listener = None

        # File menu
        self.file_menu = QMenu("File", self)
        self.addMenu(self.file_menu)
        self.open_menu = QMenu("Open", self)
        self.create_open_menu()
        self.file_menu.addMenu(self.open_menu)
        self.events_menu = QMenu("Import events info", self)
        self.create_events_menu()
        self.file_menu.addMenu(self.events_menu)
        self.events_menu.setEnabled(False)
        self.export_menu = None
        self.export_menu = QMenu("Export", self)
        self.create_export_menu()
        self.file_menu.addMenu(self.export_menu)
        self.export_menu.setEnabled(False)
        self.create_file_menu()

        # Edit menu
        self.edit_menu = QMenu("Edit", self)
        self.addMenu(self.edit_menu)
        self.create_edit_menu()
        self.edit_menu.setEnabled(False)

        # Tools menu
        self.tools_menu = QMenu("Tools", self)
        self.addMenu(self.tools_menu)
        self.create_tools_menu()
        self.tools_menu.setEnabled(False)

        # Plot menu
        self.plot_menu = QMenu("Plot", self)
        self.addMenu(self.plot_menu)
        self.create_plot_menu()
        self.plot_menu.setEnabled(False)

        # Connectivity menu
        self.connectivity_menu = QMenu("Connectivity", self)
        self.addMenu(self.connectivity_menu)
        self.create_connectivity_menu()
        self.connectivity_menu.setEnabled(False)

        # Classification menu
        self.classification_menu = QMenu("Classification", self)
        self.addMenu(self.classification_menu)
        self.create_classification_menu()
        self.classification_menu.setEnabled(False)

        # Stats menu
        self.statistics_menu = QMenu("Statistics", self)
        self.addMenu(self.statistics_menu)
        self.create_statistics_menu()
        self.statistics_menu.setEnabled(False)

        # Separator
        self.separator_menu_1 = QAction("|", self)
        self.addAction(self.separator_menu_1)
        self.separator_menu_1.setEnabled(False)

        # Study menu
        self.study_menu = QMenu("Study", self)
        self.addMenu(self.study_menu)
        self.create_study_menu()
        self.study_menu.setEnabled(False)

        # Datasets menu
        self.dataset_menu = QMenu("Datasets", self)
        self.addMenu(self.dataset_menu)
        self.dataset_menu.setEnabled(False)

        # Separator 2
        self.separator_menu_2 = QAction("|", self)
        self.addAction(self.separator_menu_2)
        self.separator_menu_2.setEnabled(False)

        # Help menu
        self.help_menu = QMenu("Help", self)
        self.addMenu(self.help_menu)
        self.create_help_menu()

        # Other
        self.study_exist = False

    """
    Menu Creation
    """
    def create_open_menu(self):
        open_fif_file_action = QAction("FIF File", self)
        open_fif_file_action.triggered.connect(self.open_fif_file_trigger)
        self.open_menu.addAction(open_fif_file_action)
        self.open_menu.addSeparator()
        open_cnt_file_action = QAction("ANT eego CNT File", self)
        open_cnt_file_action.triggered.connect(self.open_cnt_file_trigger)
        self.open_menu.addAction(open_cnt_file_action)
        open_set_file_action = QAction("SET File", self)
        open_set_file_action.triggered.connect(self.open_set_file_trigger)
        self.open_menu.addAction(open_set_file_action)

    def create_events_menu(self):
        read_events_file_action = QAction("Read events from file (.fif/.txt)", self)
        read_events_file_action.triggered.connect(self.read_events_file_trigger)
        self.events_menu.addAction(read_events_file_action)
        find_events_from_channel_action = QAction("Read events from channel data", self)
        find_events_from_channel_action.triggered.connect(self.find_events_from_channel_trigger)
        self.events_menu.addAction(find_events_from_channel_action)

    def create_export_menu(self):
        export_data_to_csv_file_action = QAction("Export data to CSV file", self)
        export_data_to_csv_file_action.triggered.connect(self.export_data_to_csv_file_trigger)
        self.export_menu.addAction(export_data_to_csv_file_action)
        export_data_to_set_file_action = QAction("Export data to SET file", self)
        export_data_to_set_file_action.triggered.connect(self.export_data_to_set_file_trigger)
        self.export_menu.addAction(export_data_to_set_file_action)
        self.export_menu.addSeparator()
        export_events_to_file_action = QAction("Export events to TXT file", self)
        export_events_to_file_action.triggered.connect(self.export_events_to_file_trigger)
        self.export_menu.addAction(export_events_to_file_action)

    def create_file_menu(self):
        # Save
        self.file_menu.addSeparator()
        save_file_action = QAction("Save", self)
        save_file_action.triggered.connect(self.save_file_trigger)
        save_file_action.setEnabled(False)
        self.file_menu.addAction(save_file_action)
        save_file_as_action = QAction("Save As", self)
        save_file_as_action.triggered.connect(self.save_file_as_trigger)
        save_file_as_action.setEnabled(False)
        self.file_menu.addAction(save_file_as_action)
        # Clear dataset
        clear_dataset_action = QAction("Clear dataset", self)
        clear_dataset_action.triggered.connect(self.clear_dataset_trigger)
        clear_dataset_action.setEnabled(False)
        self.file_menu.addAction(clear_dataset_action)
        # Study
        self.file_menu.addSeparator()
        create_study_action = QAction("Create study from loaded datasets", self)
        create_study_action.triggered.connect(self.create_study_trigger)
        create_study_action.setEnabled(False)
        self.file_menu.addAction(create_study_action)
        clear_study_action = QAction("Clear study", self)
        clear_study_action.triggered.connect(self.clear_study_trigger)
        clear_study_action.setEnabled(False)
        self.file_menu.addAction(clear_study_action)
        # Other
        self.file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_program_trigger)
        self.file_menu.addAction(exit_action)

    def create_edit_menu(self):
        dataset_info_action = QAction("Dataset information", self)
        dataset_info_action.triggered.connect(self.dataset_info_trigger)
        self.edit_menu.addAction(dataset_info_action)
        event_values_action = QAction("Event values", self)
        event_values_action.triggered.connect(self.event_values_trigger)
        self.edit_menu.addAction(event_values_action)
        channel_location_action = QAction("Channel location", self)
        channel_location_action.triggered.connect(self.channel_location_trigger)
        self.edit_menu.addAction(channel_location_action)
        # self.edit_menu.addSeparator()
        # select_data_action = QAction("Select data", self)
        # select_data_action.triggered.connect(self.select_data_trigger)
        # select_data_action.setEnabled(False)
        # self.edit_menu.addAction(select_data_action)
        # select_data_events_action = QAction("Select data using events", self)
        # select_data_events_action.triggered.connect(self.select_data_events_trigger)
        # select_data_events_action.setEnabled(False)
        # self.edit_menu.addAction(select_data_events_action)

    def create_tools_menu(self):
        filter_action = QAction("Filter", self)
        filter_action.triggered.connect(self.filter_trigger)
        self.tools_menu.addAction(filter_action)
        resampling_action = QAction("Resampling", self)
        resampling_action.triggered.connect(self.resampling_trigger)
        self.tools_menu.addAction(resampling_action)
        re_referencing_action = QAction("Re-Referencing", self)
        re_referencing_action.triggered.connect(self.re_referencing_trigger)
        self.tools_menu.addAction(re_referencing_action)
        self.tools_menu.addSeparator()
        # inspect_reject_data_action = QAction("Inspect/Reject data by eyes", self)
        # inspect_reject_data_action.triggered.connect(self.inspect_reject_data_trigger)
        # inspect_reject_data_action.setEnabled(False)
        # self.tools_menu.addAction(inspect_reject_data_action)
        # self.tools_menu.addSeparator()
        decompose_ICA_action = QAction("Decompose data with ICA", self)
        decompose_ICA_action.triggered.connect(self.ica_decomposition_trigger)
        self.tools_menu.addAction(decompose_ICA_action)
        self.tools_menu.addSeparator()
        extract_epochs_action = QAction("Extract epochs", self)
        extract_epochs_action.triggered.connect(self.extract_epochs_trigger)
        self.tools_menu.addAction(extract_epochs_action)
        self.tools_menu.addSeparator()
        snr_action = QAction("Signal-to-noise ratio", self)
        snr_action.triggered.connect(self.snr_trigger)
        self.tools_menu.addAction(snr_action)
        self.tools_menu.addSeparator()
        source_estimation_action = QAction("Source estimation", self)
        source_estimation_action.triggered.connect(self.source_estimation_trigger)
        self.tools_menu.addAction(source_estimation_action)

    def create_plot_menu(self):
        plot_channel_locations_action = QAction("Channel locations", self)
        plot_channel_locations_action.triggered.connect(self.plot_channel_locations)
        self.plot_menu.addAction(plot_channel_locations_action)
        self.plot_menu.addSeparator()
        plot_data_action = QAction("Channel data", self)
        plot_data_action.triggered.connect(self.plot_data_trigger)
        self.plot_menu.addAction(plot_data_action)
        plot_topographies_action = QAction("Channel topographies", self)
        plot_topographies_action.triggered.connect(self.plot_topographies_trigger)
        self.plot_menu.addAction(plot_topographies_action)
        plot_channel_spectra_maps_action = QAction("Channel spectra (PSD)", self)
        plot_channel_spectra_maps_action.triggered.connect(self.plot_spectra_maps_trigger)
        self.plot_menu.addAction(plot_channel_spectra_maps_action)
        plot_ERP_image_action = QAction("Channel ERP image", self)
        plot_ERP_image_action.triggered.connect(self.plot_ERP_image_trigger)
        self.plot_menu.addAction(plot_ERP_image_action)
        plot_ERPs_action = QAction("Channel ERPs", self)
        plot_ERPs_action.triggered.connect(self.plot_ERPs_trigger)
        self.plot_menu.addAction(plot_ERPs_action)
        plot_time_frequency_action = QAction("Channel time-frequency (ERSP/ITC)", self)
        plot_time_frequency_action.triggered.connect(self.plot_time_frequency_trigger)
        self.plot_menu.addAction(plot_time_frequency_action)

    def create_connectivity_menu(self):
        envelope_correlation_action = QAction("Envelope Correlation", self)
        envelope_correlation_action.triggered.connect(self.envelope_correlation_trigger)
        self.connectivity_menu.addAction(envelope_correlation_action)
        source_space_connectivity_action = QAction("Source Space Connectivity", self)
        source_space_connectivity_action.triggered.connect(self.source_space_connectivity_trigger)
        self.connectivity_menu.addAction(source_space_connectivity_action)
        sensor_space_connectivity_action = QAction("3D Sensor Space Connectivity", self)
        sensor_space_connectivity_action.triggered.connect(self.sensor_space_connectivity_trigger)
        self.connectivity_menu.addAction(sensor_space_connectivity_action)
        # spectro_temporal_connectivity_action = QAction("Spectro-Temporal Connectivity", self)
        # spectro_temporal_connectivity_action.triggered.connect(self.spectro_temporal_connectivity_trigger)
        # spectro_temporal_connectivity_action.setEnabled(False)
        # self.connectivity_menu.addAction(spectro_temporal_connectivity_action)

    def create_classification_menu(self):
        classify_action = QAction("Classify", self)
        classify_action.triggered.connect(self.classify_trigger)
        self.classification_menu.addAction(classify_action)

    def create_statistics_menu(self):
        statistics_snr_action = QAction("Signal-to-Noise Ratio", self)
        statistics_snr_action.triggered.connect(self.statistics_snr_trigger)
        self.statistics_menu.addAction(statistics_snr_action)

        statistics_erp_action = QAction("ERP", self)
        statistics_erp_action.triggered.connect(self.statistics_erp_trigger)
        self.statistics_menu.addAction(statistics_erp_action)

        statistics_psd_action = QAction("PSD", self)
        statistics_psd_action.triggered.connect(self.statistics_psd_trigger)
        self.statistics_menu.addAction(statistics_psd_action)

        statistics_ersp_itc_action = QAction("ERSP-ITC", self)
        statistics_ersp_itc_action.triggered.connect(self.statistics_ersp_itc_trigger)
        self.statistics_menu.addAction(statistics_ersp_itc_action)

        statistics_connectivity_action = QAction("Connectivity", self)
        statistics_connectivity_action.triggered.connect(self.statistics_connectivity_trigger)
        self.statistics_menu.addAction(statistics_connectivity_action)

    def create_study_menu(self):
        edit_study_action = QAction("Edit Study Info", self)
        edit_study_action.triggered.connect(self.edit_study_trigger)
        self.study_menu.addAction(edit_study_action)
        self.study_menu.addSeparator()
        plot_study_action = QAction("Plots", self)
        plot_study_action.triggered.connect(self.plot_study_trigger)
        self.study_menu.addAction(plot_study_action)

    def create_help_menu(self):
        help_action = QAction("Help", self)
        help_action.triggered.connect(self.help_trigger)
        help_action.setEnabled(False)
        self.help_menu.addAction(help_action)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.about_trigger)
        about_action.setEnabled(False)
        self.help_menu.addAction(about_action)

    """
    Menu Manipulation
    """
    def change_menu_status(self, new_status):
        """
        Change the status of all the menus. Either all enabled of disabled.
        :param new_status: The new status of the menus
        :type new_status: bool
        """
        menu_actions = self.file_menu.actions()
        self.events_menu.setEnabled(new_status)
        self.export_menu.setEnabled(new_status)
        for action in menu_actions:
            if action.text() in ["Save", "Save As", "Clear dataset", "Create study from loaded datasets", "Clear study"]:
                action.setEnabled(new_status)
            if action.text() == "Exit":
                action.setEnabled(True)
            if not self.study_exist and action.text() == "Clear study":
                action.setEnabled(False)
        self.edit_menu.setEnabled(new_status)
        self.tools_menu.setEnabled(new_status)
        self.plot_menu.setEnabled(new_status)
        self.connectivity_menu.setEnabled(new_status)
        self.classification_menu.setEnabled(new_status)
        self.statistics_menu.setEnabled(new_status)
        self.dataset_menu.setEnabled(new_status)

    def enable_menu(self):
        """
        Make the menus enabled when at least dataset is loaded.
        """
        self.change_menu_status(True)

    def disable_menu(self):
        """
        Make the menus disabled when no dataset is loaded.
        """
        self.change_menu_status(False)

    def add_dataset(self, dataset_index, dataset_name, study_available):
        """
        Add a dataset in the dataset menu.
        :param dataset_index: The index of new dataset.
        :type dataset_index: int
        :param dataset_name: The name of the new dataset.
        :type dataset_name: str
        :param study_available: Enable the menu for selecting the study if it is available.
        :type study_available: bool
        """
        menu_actions = self.dataset_menu.actions()

        # Recreate all the menus.
        self.dataset_menu.clear()
        dataset_counter = 1
        for i in range(len(menu_actions)-2):    # -2 for the separator and the study
            dataset = menu_actions[i]
            dataset_complete_name = dataset.text()
            dataset_name_to_insert = dataset_complete_name.split(": ")[1]     # Get only the dataset name
            new_dataset_name = "Dataset " + str(dataset_counter) + " : " + dataset_name_to_insert
            dataset.setText(new_dataset_name)
            self.dataset_menu.addAction(dataset)
            dataset_counter += 1

        # Add new dataset
        dataset_menu_name = "Dataset " + str(dataset_index+1) + " : " + dataset_name
        new_dataset = QAction(dataset_menu_name, self)
        new_dataset.triggered.connect(self.dataset_clicked)
        self.dataset_menu.addAction(new_dataset)

        # Add study
        self.study_exist = study_available
        self.dataset_menu.addSeparator()
        study = QAction("Select study", self)
        study.triggered.connect(self.dataset_clicked)
        study.setEnabled(self.study_exist)
        self.dataset_menu.addAction(study)

    def remove_dataset(self, dataset_index, study_available):
        """
        Remove a dataset from the dataset menu.
        :param dataset_index: The index of dataset to remove
        :type dataset_index: int
        :param study_available: Enable the menu for selecting the study if it is available.
        :type study_available: bool
        """
        menu_actions = self.dataset_menu.actions()
        del menu_actions[dataset_index]     # Remove the dataset in the menus.

        # Recreate all the menus.
        self.dataset_menu.clear()
        dataset_counter = 1
        for i in range(len(menu_actions)-2):    # -2 for separator and study
            dataset = menu_actions[i]
            dataset_complete_name = dataset.text()
            dataset_name = dataset_complete_name.split(": ")[1]     # Get only the dataset name
            new_dataset_name = "Dataset " + str(dataset_counter) + " : " + dataset_name
            dataset.setText(new_dataset_name)
            self.dataset_menu.addAction(dataset)
            dataset_counter += 1

        # Add study
        self.study_exist = study_available
        self.dataset_menu.addSeparator()
        study = QAction("Select study", self)
        study.triggered.connect(self.dataset_clicked)
        study.setEnabled(self.study_exist)
        self.dataset_menu.addAction(study)

    def dataset_selected_menu_activation(self, study_exist):
        """
        Activate the menus when a dataset is selected.
        :param study_exist: True if the study exists, false otherwise
        :type study_exist: bool
        """
        self.study_exist = study_exist

        # File menu
        menu_actions = self.file_menu.actions()
        for action in menu_actions:
            if action.text() in ["Open", "Import events info", "Export", "Save", "Save As", "Clear dataset",
                                 "Create study from loaded datasets", "Exit"]:
                action.setEnabled(True)
            if action.text() == "Clear study":
                if self.study_exist:
                    action.setEnabled(True)
                else:
                    action.setEnabled(False)

        # Edit menu
        menu_actions = self.edit_menu.actions()
        for action in menu_actions:
            if action.text() in ["Dataset information", "Event values", "Channel location"]:
                action.setEnabled(True)

        # Tools menu
        menu_actions = self.tools_menu.actions()
        for action in menu_actions:
            if action.text() in ["Filter", "Resampling", "Re-Referencing", "Decompose data with ICA",
                                 "Extract epochs", "Signal-to-noise ratio", "Source estimation"]:
                action.setEnabled(True)

        # Dataset menu
        self.dataset_menu.setEnabled(True)
        menu_actions = self.dataset_menu.actions()
        menu_actions[-1].setEnabled(self.study_exist)  # The last element of the menu is always the study

        # Other menus
        self.plot_menu.setEnabled(True)
        self.connectivity_menu.setEnabled(True)
        self.classification_menu.setEnabled(True)
        self.statistics_menu.setEnabled(True)
        self.study_menu.setEnabled(False)

    def study_selected_menu_activation(self):
        """
        Activate the menus when the study is selected.
        """
        self.study_exist = True

        # File menu
        menu_actions = self.file_menu.actions()
        for action in menu_actions:
            if action.text() in ["Clear study", "Exit"]:
                action.setEnabled(True)
            else:
                action.setEnabled(False)

        # Edit menu
        menu_actions = self.edit_menu.actions()
        for action in menu_actions:
            if action.text() in ["Channel location"]:
                action.setEnabled(True)
            else:
                action.setEnabled(False)

        # Tools menu
        menu_actions = self.tools_menu.actions()
        for action in menu_actions:
            if action.text() in ["Filter", "Resampling", "Re-Referencing", "Decompose data with ICA",
                                 "Signal-to-noise ratio", "Source estimation"]:
                action.setEnabled(True)
            else:
                action.setEnabled(False)

        # Dataset menu
        self.dataset_menu.setEnabled(True)
        menu_actions = self.dataset_menu.actions()
        menu_actions[-1].setEnabled(True)               # The last element of the menu is always the study

        # Other menus
        self.plot_menu.setEnabled(False)
        self.connectivity_menu.setEnabled(False)
        self.classification_menu.setEnabled(False)
        self.statistics_menu.setEnabled(False)
        self.study_menu.setEnabled(True)

    """
    Triggers
    """

    """
    File menu triggers
    """
    def open_fif_file_trigger(self):
        path_to_file = QFileDialog().getOpenFileName(self, "Open file", "*.fif")
        self.menubar_listener.open_fif_file_clicked(path_to_file[0])

    def open_cnt_file_trigger(self):
        path_to_file = QFileDialog().getOpenFileName(self, "Open file", "*.cnt")
        self.menubar_listener.open_cnt_file_clicked(path_to_file[0])

    def open_set_file_trigger(self):
        path_to_file = QFileDialog().getOpenFileName(self, "Open file", "*.set")
        self.menubar_listener.open_set_file_clicked(path_to_file[0])

    def read_events_file_trigger(self):
        path_to_file = QFileDialog().getOpenFileName(self, "Open file")
        self.menubar_listener.read_events_file_clicked(path_to_file[0])

    def find_events_from_channel_trigger(self):
        self.menubar_listener.find_events_from_channel_clicked()

    def export_data_to_csv_file_trigger(self):
        path_to_file = QFileDialog().getSaveFileName(self, "Export data to CSV file")
        self.menubar_listener.export_data_to_csv_file_clicked(path_to_file[0])

    def export_data_to_set_file_trigger(self):
        path_to_file = QFileDialog().getSaveFileName(self, "Export data to SET file")
        self.menubar_listener.export_data_to_set_file_clicked(path_to_file[0])

    def export_events_to_file_trigger(self):
        self.menubar_listener.export_events_to_file_clicked()

    def save_file_trigger(self):
        self.menubar_listener.save_file_clicked()

    def save_file_as_trigger(self):
        self.menubar_listener.save_file_as_clicked()

    # Dataset
    def clear_dataset_trigger(self):
        self.menubar_listener.clear_dataset_clicked()

    # Study
    def create_study_trigger(self):
        self.menubar_listener.create_study_clicked()

    def clear_study_trigger(self):
        self.menubar_listener.clear_study_clicked()

    # Exit
    def exit_program_trigger(self):
        self.menubar_listener.exit_program_clicked()

    """
    Edit menu trigger
    """
    def dataset_info_trigger(self):
        self.menubar_listener.dataset_info_clicked()

    def event_values_trigger(self):
        self.menubar_listener.event_values_clicked()

    def channel_location_trigger(self):
        self.menubar_listener.channel_location_clicked()

    def select_data_trigger(self):
        self.menubar_listener.select_data_clicked()

    def select_data_events_trigger(self):
        self.menubar_listener.select_data_events_clicked()

    """
    Tools menu triggers
    """
    def filter_trigger(self):
        self.menubar_listener.filter_clicked()

    def resampling_trigger(self):
        self.menubar_listener.resampling_clicked()

    def re_referencing_trigger(self):
        self.menubar_listener.re_referencing_clicked()

    def inspect_reject_data_trigger(self):
        self.menubar_listener.inspect_reject_data_clicked()

    def ica_decomposition_trigger(self):
        self.menubar_listener.ica_decomposition_clicked()

    def extract_epochs_trigger(self):
        self.menubar_listener.extract_epochs_clicked()

    def snr_trigger(self):
        self.menubar_listener.snr_clicked()

    def source_estimation_trigger(self):
        self.menubar_listener.source_estimation_clicked()

    """
    Plot menu triggers
    """
    def plot_channel_locations(self):
        self.menubar_listener.plot_channel_locations_clicked()

    def plot_data_trigger(self):
        self.menubar_listener.plot_data_clicked()

    def plot_topographies_trigger(self):
        self.menubar_listener.plot_topographies_clicked()

    def plot_spectra_maps_trigger(self):
        self.menubar_listener.plot_spectra_maps_clicked()

    def plot_channel_properties_trigger(self):
        self.menubar_listener.plot_channel_properties_clicked()

    def plot_ERP_image_trigger(self):
        self.menubar_listener.plot_ERP_image_clicked()

    def plot_ERPs_trigger(self):
        self.menubar_listener.plot_ERPs_clicked()

    def plot_time_frequency_trigger(self):
        self.menubar_listener.plot_time_frequency_clicked()

    """
    Connectivity menu triggers
    """
    def envelope_correlation_trigger(self):
        self.menubar_listener.envelope_correlation_clicked()

    def source_space_connectivity_trigger(self):
        self.menubar_listener.source_space_connectivity_clicked()

    def sensor_space_connectivity_trigger(self):
        self.menubar_listener.sensor_space_connectivity_clicked()

    def spectro_temporal_connectivity_trigger(self):
        self.menubar_listener.spectro_temporal_connectivity_clicked()

    """
    Statistics menu triggers
    """
    def statistics_snr_trigger(self):
        self.menubar_listener.statistics_snr_clicked()

    def statistics_erp_trigger(self):
        self.menubar_listener.statistics_erp_clicked()

    def statistics_psd_trigger(self):
        self.menubar_listener.statistics_psd_clicked()

    def statistics_ersp_itc_trigger(self):
        self.menubar_listener.statistics_ersp_itc_clicked()

    def statistics_connectivity_trigger(self):
        self.menubar_listener.statistics_connectivity_clicked()

    """
    Classification menu triggers
    """
    def classify_trigger(self):
        self.menubar_listener.classify_clicked()

    """
    Study menu trigger
    """
    def edit_study_trigger(self):
        self.menubar_listener.edit_study_clicked()

    def plot_study_trigger(self):
        self.menubar_listener.plot_study_clicked()

    """
    Datasets menu trigger
    """
    def dataset_clicked(self):
        menu_actions = self.dataset_menu.actions()
        selected_action = self.sender()

        index_selected = 0
        while selected_action != menu_actions[index_selected]:
            index_selected += 1

        if index_selected == len(menu_actions)-1:       # Study selected
            self.menubar_listener.study_selected()
            self.study_selected_menu_activation()
        else:                                           # Dataset selected
            self.menubar_listener.change_dataset(index_selected)
            self.dataset_selected_menu_activation(study_exist=self.study_exist)

    """
    Help menu triggers
    """
    def help_trigger(self):
        self.menubar_listener.help_clicked()

    def about_trigger(self):
        self.menubar_listener.about_clicked()

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: menubarController
        """
        self.menubar_listener = listener
