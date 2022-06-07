#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source estimation view
"""

from multiprocessing import cpu_count

from PyQt5.QtWidgets import QWidget, QComboBox, QPushButton, QLabel, QCheckBox, QButtonGroup, QVBoxLayout, \
    QHBoxLayout, QSlider, QGridLayout, QSpinBox
from PyQt5.QtCore import Qt

from mne.viz import plot_source_estimates

from utils.file_path_search import get_project_freesurfer_path

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sourceEstimationView(QWidget):
    def __init__(self, number_of_epochs, title=None):
        """
        Window displaying the parameters for computing the source estimation on the dataset.
        :param number_of_epochs: Number of epochs in the dataset.
        :type number_of_epochs: int
        :param title: Title of window
        :type title: str
        """
        super().__init__()
        self.source_estimation_listener = None
        self.subject = "fsaverage"
        self.subjects_dir = get_project_freesurfer_path()

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

        # N Jobs Slider
        self.n_jobs_widget = QWidget()
        self.n_jobs_layout = QHBoxLayout()
        self.n_jobs_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.n_jobs_slider.setMinimum(1)
        self.n_jobs_slider.setMaximum(cpu_count())
        self.n_jobs_slider.setValue(1)
        self.n_jobs_slider.setSingleStep(1)
        self.n_jobs_slider.valueChanged.connect(self.slider_value_changed_trigger)
        self.n_jobs_label = QLabel("1")
        self.n_jobs_layout.addWidget(QLabel("Number of threads : "))
        self.n_jobs_layout.addWidget(self.n_jobs_slider)
        self.n_jobs_layout.addWidget(self.n_jobs_label)
        self.n_jobs_widget.setLayout(self.n_jobs_layout)

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
        self.global_layout.addWidget(self.epochs_trial_average_widget)
        self.global_layout.addWidget(self.n_jobs_widget)
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
                                  hemi="both", backend="pyvistaqt", time_viewer=True,  smoothing_steps=7)
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
        trial_number = self.trial_number_single_trial.value()-1
        n_jobs = self.n_jobs_slider.value()
        self.source_estimation_listener.confirm_button_clicked(source_estimation_method, save_data, load_data, epochs_method,
                                                               trial_number, n_jobs)

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
