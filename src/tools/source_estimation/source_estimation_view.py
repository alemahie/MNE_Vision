#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source estimation view
"""

from multiprocessing import cpu_count

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QLabel, QCheckBox, QButtonGroup, QVBoxLayout, \
    QHBoxLayout, QSlider, QGridLayout, QSpinBox, QLineEdit
from PyQt5.QtCore import Qt

from mne.viz import plot_source_estimates

from utils.elements_selector.elements_selector_controller import multipleSelectorController
from utils.file_path_search import get_project_freesurfer_path
from utils.view.separator import create_layout_separator

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sourceEstimationView(QWidget):
    def __init__(self, number_of_epochs, event_values, event_ids, tmin, tmax, title=None):
        """
        Window displaying the parameters for computing the source estimation on the dataset.
        :param number_of_epochs: Number of epochs in the dataset.
        :type number_of_epochs: int
        :param event_values: Event_id associated to each epoch/trial.
        :type event_values: list of, list of int
        :param event_ids: Name of the events associated to their id.
        :type event_ids: dict
        :param tmin: Start time of the epoch or raw file
        :type tmin: float
        :param tmax: End time of the epoch or raw file
        :type tmax: float
        :param title: Title of window
        :type title: str
        """
        super().__init__()
        self.source_estimation_listener = None
        self.subject = "fsaverage"
        self.subjects_dir = get_project_freesurfer_path()
        self.event_values = event_values
        self.event_ids = event_ids

        self.events_selector_controller = None
        self.trials_selected = None

        if title is None:
            self.setWindowTitle("Source Estimation")
        else:
            self.setWindowTitle(title)

        self.global_layout = QVBoxLayout()
        self.setLayout(self.global_layout)

        # Method
        self.method_widget = QWidget()
        self.method_layout = QHBoxLayout()
        self.method_box = QComboBox()
        self.method_box.addItems(["MNE", "dSPM", "sLORETA", "eLORETA"])
        self.method_layout.addWidget(QLabel("Source estimation method : "))
        self.method_layout.addWidget(self.method_box)
        self.method_widget.setLayout(self.method_layout)

        # How to compute
        self.save_load_widget = QWidget()
        self.check_box_layout = QVBoxLayout()
        self.save_load_buttons = QButtonGroup()
        self.check_box_compute_from_scratch = QCheckBox()
        self.check_box_compute_from_scratch.setText("Compute source estimation from scratch and don't save")
        self.check_box_compute_from_scratch.setChecked(True)
        self.save_load_buttons.addButton(self.check_box_compute_from_scratch, 0)    # Button with ID 0
        self.check_box_save = QCheckBox()
        self.check_box_save.setText("Save source estimation files")
        self.save_load_buttons.addButton(self.check_box_save, 1)   # Button with ID 1
        self.check_box_load = QCheckBox()
        self.check_box_load.setText("Load source estimation files")
        self.save_load_buttons.addButton(self.check_box_load, 2)  # Button with ID 2
        self.check_box_layout.addWidget(self.check_box_compute_from_scratch)
        self.check_box_layout.addWidget(self.check_box_save)
        self.check_box_layout.addWidget(self.check_box_load)
        self.save_load_widget.setLayout(self.check_box_layout)

        # What to compute
        self.epochs_trial_average_widget = QWidget()
        self.epochs_trial_average_check_box_layout = QGridLayout()
        self.epochs_trial_average_buttons = QButtonGroup()

        self.check_box_single_trial = QCheckBox()
        self.check_box_single_trial.setText("Compute source estimation on a single trial (select trial number) : ")
        self.epochs_trial_average_buttons.addButton(self.check_box_single_trial, 0)    # Button with ID 0
        self.trial_number_single_trial = QSpinBox()
        self.trial_number_single_trial.setMinimum(1)
        self.trial_number_single_trial.setMaximum(number_of_epochs)
        self.trial_number_single_trial.setValue(1)

        self.check_box_evoked = QCheckBox()
        self.check_box_evoked.setChecked(True)
        self.check_box_evoked.setText("Compute source estimation on the evoked signal")
        self.epochs_trial_average_buttons.addButton(self.check_box_evoked, 1)   # Button with ID 1

        self.check_box_all_trials_averaged = QCheckBox()
        self.check_box_all_trials_averaged.setText("Compute source estimation on all trials averaged")
        self.epochs_trial_average_buttons.addButton(self.check_box_all_trials_averaged, 2)  # Button with ID 2

        self.epochs_trial_average_check_box_layout.addWidget(self.check_box_single_trial, 0, 0)
        self.epochs_trial_average_check_box_layout.addWidget(self.trial_number_single_trial, 0, 1)
        self.epochs_trial_average_check_box_layout.addWidget(self.check_box_evoked, 1, 0)
        self.epochs_trial_average_check_box_layout.addWidget(self.check_box_all_trials_averaged, 2, 0)
        self.epochs_trial_average_widget.setLayout(self.epochs_trial_average_check_box_layout)

        # Trials events and indexes
        self.trial_selection_widget = QWidget()
        self.trial_selection_layout = QGridLayout()
        self.trial_selection_label = QLabel("Trials indexes to compute (default : all) :")
        self.trial_selection_indexes = QPushButton("Select by trials indexes")
        self.trial_selection_indexes.clicked.connect(self.trial_selection_indexes_trigger)
        self.trial_selection_events = QPushButton("Select by events")
        self.trial_selection_events.clicked.connect(self.trial_selection_events_trigger)
        self.trial_selection_layout.addWidget(self.trial_selection_label, 0, 0)
        self.trial_selection_layout.addWidget(self.trial_selection_indexes, 0, 1)
        self.trial_selection_layout.addWidget(self.trial_selection_events, 1, 1)
        self.trial_selection_widget.setLayout(self.trial_selection_layout)

        # Data start and end
        self.data_start_widget = QWidget()
        self.data_start_layout = QGridLayout()
        self.data_start_end_validator = QDoubleValidator()
        self.data_start_end_validator.setRange(tmin, tmax)
        self.data_start_line = QLineEdit(str(tmin))
        self.data_start_line.setValidator(self.data_start_end_validator)
        self.data_end_line = QLineEdit(str(tmax))
        self.data_end_line.setValidator(self.data_start_end_validator)
        self.data_start_layout.addWidget(QLabel("Data start time (sec) : "), 0, 0)
        self.data_start_layout.addWidget(self.data_start_line, 0, 1)
        self.data_start_layout.addWidget(QLabel("Data end time (sec) : "), 1, 0)
        self.data_start_layout.addWidget(self.data_end_line, 1, 1)
        self.data_start_widget.setLayout(self.data_start_layout)

        # Number of Jobs Slider
        self.n_jobs_widget = QWidget()
        self.n_jobs_layout = QHBoxLayout()
        self.n_jobs_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.n_jobs_slider.setMinimum(1)
        self.n_jobs_slider.setMaximum(cpu_count())
        self.n_jobs_slider.setValue(1)
        self.n_jobs_slider.setSingleStep(1)
        self.n_jobs_slider.valueChanged.connect(self.slider_value_changed_trigger)
        self.n_jobs_label = QLabel("1")
        self.n_jobs_layout.addWidget(QLabel("Number of parallel jobs : "))
        self.n_jobs_layout.addWidget(self.n_jobs_slider)
        self.n_jobs_layout.addWidget(self.n_jobs_label)
        self.n_jobs_widget.setLayout(self.n_jobs_layout)

        # Exportation
        self.data_exportation_widget = QWidget()
        self.data_exportation_layout = QHBoxLayout()
        self.data_exportation_button = QPushButton("Data exportation")
        self.data_exportation_button.clicked.connect(self.data_exportation_trigger)
        self.data_exportation_layout.addWidget(self.data_exportation_button)
        self.data_exportation_widget.setLayout(self.data_exportation_layout)

        # Cancel confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_source_estimation_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_source_estimation_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        # Layout
        self.global_layout.addWidget(self.method_widget)
        self.global_layout.addWidget(self.save_load_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.epochs_trial_average_widget)
        self.global_layout.addWidget(self.trial_selection_widget)
        self.global_layout.addWidget(self.data_start_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.n_jobs_widget)
        self.global_layout.addWidget(self.data_exportation_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.cancel_confirm_widget)

    def plot_source_estimation(self, source_estimation_data):
        """
        Plot the source estimation.
        :param source_estimation_data: The source estimation's data.
        :type source_estimation_data: MNE.SourceEstimation
        """
        try:
            print("plot source estimates")
            plot_source_estimates(source_estimation_data, subject=self.subject, subjects_dir=self.subjects_dir,
                                  hemi="both", backend="pyvistaqt", time_viewer=True, smoothing_steps=7)
        except Exception as e:
            print(type(e))
            print(e)

    """
    Triggers
    """
    def cancel_source_estimation_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.source_estimation_listener.cancel_button_clicked()

    def confirm_source_estimation_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        source_estimation_method = self.method_box.currentText()
        save_data, load_data = self.get_save_load_button_checked()
        epochs_method = self.get_epochs_trial_average_method()
        n_jobs = self.n_jobs_slider.value()
        if epochs_method == "single_trial":
            trials_selected = [self.trial_number_single_trial.value()]
        else:
            if self.trials_selected is None:
                trials_selected = [i for i in range(len(self.event_values))]
            else:
                trials_selected = self.trials_selected
        tmin = None
        tmax = None
        if self.data_start_line.hasAcceptableInput():
            tmin = self.data_start_line.text()
            tmin = float(tmin.replace(',', '.'))
        if self.data_end_line.hasAcceptableInput():
            tmax = self.data_end_line.text()
            tmax = float(tmax.replace(',', '.'))
        self.source_estimation_listener.confirm_button_clicked(source_estimation_method, save_data, load_data, epochs_method,
                                                               trials_selected, tmin, tmax, n_jobs)

    def trial_selection_indexes_trigger(self):
        """
        Open the multiple selector window.
        The user can select the trials indexes he wants the source estimation to be computed on.
        """
        title = "Select the trial's events used for computing the source estimation:"
        indexes_list = [str(i+1) for i in range(len(self.event_values))]
        self.events_selector_controller = multipleSelectorController(indexes_list, title, box_checked=True,
                                                                     element_type="indexes")
        self.events_selector_controller.set_listener(self.source_estimation_listener)

    def trial_selection_events_trigger(self):
        """
        Open the multiple selector window.
        The user can select the events he wants the source estimation to be computed on.
        """
        title = "Select the trial's events used for computing the source estimation:"
        events_ids_list = list(self.event_ids.keys())
        self.events_selector_controller = multipleSelectorController(events_ids_list, title, box_checked=True,
                                                                     element_type="events")
        self.events_selector_controller.set_listener(self.source_estimation_listener)

    def data_exportation_trigger(self):
        """
        Open a new window asking for the path for the exportation of the source estimation computation data/
        """
        self.source_estimation_listener.additional_parameters_clicked()

    def slider_value_changed_trigger(self):
        """
        Change the value of the slider displayed on the window when the actual slider is moved.
        """
        slider_value = self.n_jobs_slider.value()
        self.n_jobs_label.setText(str(slider_value))

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: sourceEstimationController
        """
        self.source_estimation_listener = listener

    def set_trials_selected(self, elements_selected, element_type):
        """
        Set the channels selected in the multiple selector window.
        :param elements_selected: Trials or Events selected.
        :type elements_selected: list of str
        :param element_type: Type of the element selected, used in case multiple element selector windows can be open in
        a window. Can thus distinguish the returned elements.
        :type element_type: str
        """
        trials_to_use = []
        if element_type == "indexes":
            for trial in elements_selected:
                trials_to_use.append(int(trial)-1)  # -1 To get index in the list, not "position"
        elif element_type == "events":
            # Get ids of the events selected
            event_ids_selected = []
            for event in elements_selected:
                event_ids_selected.append(self.event_ids[event])
            # Get indexes of the trials if their event is selected.
            for i in range(len(self.event_values)):
                if self.event_values[i][2] in event_ids_selected:
                    trials_to_use.append(i)
        self.trials_selected = trials_to_use

    """
    Getters
    """
    def get_save_load_button_checked(self):
        """
        Get the values of the save and load buttons.
        :return: save_data: True if the data must be saved. Otherwise, False.
        load_data: True if the data must be loaded. Otherwise, False.
        :rtype: boolean, boolean
        """
        checked_button = self.save_load_buttons.checkedButton()
        button_id = self.save_load_buttons.id(checked_button)
        save_data = None
        load_data = None
        if button_id == 0:
            save_data = False
            load_data = False
        elif button_id == 1:
            save_data = True
            load_data = False
        elif button_id == 2:
            save_data = False
            load_data = True
        return save_data, load_data

    def get_epochs_trial_average_method(self):
        checked_button = self.epochs_trial_average_buttons.checkedButton()
        button_id = self.epochs_trial_average_buttons.id(checked_button)
        method = None
        if button_id == 0:
            method = "single_trial"
        elif button_id == 1:
            method = "evoked"
        elif button_id == 2:
            method = "averaged"
        return method
