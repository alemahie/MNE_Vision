#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics SNR view
"""

import numpy as np
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QButtonGroup, QCheckBox, \
    QScrollArea
from matplotlib import pyplot as plt

from utils.elements_selector.elements_selector_controller import multipleSelectorController
from utils.view.separator import create_layout_separator

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class statisticsSnrView(QWidget):
    def __init__(self, all_channels_names, event_values, event_ids):
        """
        Window displaying the parameters for computing the SNR on the dataset.
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        :param event_values: The events' information. Each event is represented by a list of 3 elements: First the latency time of
        the event; Second a "0" for MNE backwards compatibility; Third the event id.
        :type event_values:  list of, list of int
        :param event_ids: The events' ids
        :type event_ids: dict
        """
        super().__init__()
        self.snr_listener = None

        self.all_channels_names = all_channels_names
        self.event_values = event_values
        self.event_ids = event_ids
        self.channels_selected = None
        self.snr_methods = None
        self.trials_selected = None

        self.snr_selector_controller = None
        self.channels_selector_controller = None
        self.events_selector_controller = None

        self.setWindowTitle("Statistics and Signal-To-Noise Ratio")

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        # Statistics and on what to compute
        self.statistics_widget = QWidget()
        self.statistics_global_layout = QVBoxLayout()
        self.statistics_title_label = QLabel("Select the two independent variables to compute the statistics on :")

        # Independent variables
        self.statistics_independent_variables_widget = QWidget()
        self.statistics_independent_variables_layout = QHBoxLayout()

        # First independent variable
        self.first_independent_variable_widget = QWidget()
        self.first_independent_variable_layout = QVBoxLayout()
        self.first_independent_variable_label = QLabel("First independent variable :")
        self.first_independent_variable_layout.addWidget(self.first_independent_variable_label)
        self.first_independent_variable_button = QButtonGroup()
        self.create_first_independent_variable_check_boxes()
        self.first_independent_variable_widget.setLayout(self.first_independent_variable_layout)
        self.first_independent_variable_scroll_area = QScrollArea()
        self.first_independent_variable_scroll_area.setWidgetResizable(True)
        self.first_independent_variable_scroll_area.setWidget(self.first_independent_variable_widget)
        self.statistics_independent_variables_layout.addWidget(self.first_independent_variable_scroll_area)

        # Second independent variable
        self.second_independent_variable_widget = QWidget()
        self.second_independent_variable_layout = QVBoxLayout()
        self.second_independent_variable_label = QLabel("Second independent variable :")
        self.second_independent_variable_layout.addWidget(self.second_independent_variable_label)
        self.second_independent_variable_button = QButtonGroup()
        self.create_second_independent_variable_check_boxes()
        self.second_independent_variable_widget.setLayout(self.second_independent_variable_layout)
        self.second_independent_variable_scroll_area = QScrollArea()
        self.second_independent_variable_scroll_area.setWidgetResizable(True)
        self.second_independent_variable_scroll_area.setWidget(self.second_independent_variable_widget)
        self.statistics_independent_variables_layout.addWidget(self.second_independent_variable_scroll_area)

        self.statistics_independent_variables_widget.setLayout(self.statistics_independent_variables_layout)
        self.statistics_global_layout.addWidget(self.statistics_title_label)
        self.statistics_global_layout.addWidget(self.statistics_independent_variables_widget)
        self.statistics_widget.setLayout(self.statistics_global_layout)

        # SNR Methods
        self.snr_selection_widget = QWidget()
        self.snr_selection_layout = QHBoxLayout()
        self.snr_selection_button = QPushButton("&SNR methods ...", self)
        self.snr_selection_button.clicked.connect(self.snr_selection_trigger)
        self.snr_selection_layout.addWidget(QLabel("SNR Methods selection : "))
        self.snr_selection_layout.addWidget(self.snr_selection_button)
        self.snr_selection_widget.setLayout(self.snr_selection_layout)

        # Channels
        self.channels_selection_widget = QWidget()
        self.channels_selection_layout = QHBoxLayout()
        self.channels_selection_button = QPushButton("&Channels ...", self)
        self.channels_selection_button.clicked.connect(self.channels_selection_trigger)
        self.channels_selection_layout.addWidget(QLabel("Channels : "))
        self.channels_selection_layout.addWidget(self.channels_selection_button)
        self.channels_selection_widget.setLayout(self.channels_selection_layout)

        # Source Method
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

        # Cancel confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_snr_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_snr_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        # Layout
        self.vertical_layout.addWidget(self.statistics_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.snr_selection_widget)
        self.vertical_layout.addWidget(self.channels_selection_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.method_widget)
        self.vertical_layout.addWidget(self.save_load_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    def create_first_independent_variable_check_boxes(self):
        event_ids = self.event_ids
        self.first_independent_variable_button.setExclusive(True)
        for i, event_id in enumerate(event_ids):
            check_box = QCheckBox()
            check_box.setText(event_id)
            if i == 0:
                check_box.setChecked(True)
            self.first_independent_variable_layout.addWidget(check_box)
            self.first_independent_variable_button.addButton(check_box, i)

    def create_second_independent_variable_check_boxes(self):
        event_ids = self.event_ids
        self.second_independent_variable_button.setExclusive(True)
        for i, event_id in enumerate(event_ids):
            check_box = QCheckBox()
            check_box.setText(event_id)
            if i == 0:
                check_box.setChecked(True)
            self.second_independent_variable_layout.addWidget(check_box)
            self.second_independent_variable_button.addButton(check_box, i)

    """
    Triggers
    """
    def cancel_snr_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.snr_listener.cancel_button_clicked()

    def confirm_snr_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        source_method = self.method_box.currentText()
        write, read = self.get_save_load_button_checked()
        if self.snr_methods is None:
            self.snr_methods = ['Mean-Std', "Sample Correlation Coefficient", "Maximum Likelihood", "Amplitude",
                                "Plus-Minus Averaging", "Response Repetition", "MNE Source", "MNE Frequency"]
        if self.channels_selected is None:
            self.channels_selected = self.all_channels_names

        stats_first_variable = self.get_first_independent_variable_selected()
        stats_second_variable = self.get_second_independent_variable_selected()

        self.snr_listener.confirm_button_clicked(self.snr_methods, source_method, read, write, self.channels_selected,
                                                 stats_first_variable, stats_second_variable)

    def snr_selection_trigger(self):
        """
        Open the multiple selector window.
        The user can select a multiple pipelines used for the classification.
        """
        title = "Select the SNR methods used for the computation :"
        all_snr_methods = ['Mean-Std', "Sample Correlation Coefficient", "Maximum Likelihood", "Amplitude",
                           "Plus-Minus Averaging", "Response Repetition", "MNE Source", "MNE Frequency"]
        self.snr_selector_controller = multipleSelectorController(all_snr_methods, title, box_checked=True,
                                                                  element_type="snr")
        self.snr_selector_controller.set_listener(self.snr_listener)

    def channels_selection_trigger(self):
        """
        Open the multiple selector window.
        The user can select multiple channels.
        """
        title = "Select the channels used for the SNR computation :"
        self.channels_selector_controller = multipleSelectorController(self.all_channels_names, title, box_checked=True,
                                                                       element_type="channels")
        self.channels_selector_controller.set_listener(self.snr_listener)

    def trial_selection_indexes_trigger(self):
        """
        Open the multiple selector window.
        The user can select the trials indexes he wants the source estimation to be computed on.
        """
        title = "Select the trial's events used for computing the source estimation:"
        indexes_list = [str(i+1) for i in range(len(self.event_values))]
        self.events_selector_controller = multipleSelectorController(indexes_list, title, box_checked=True,
                                                                     element_type="indexes")
        self.events_selector_controller.set_listener(self.snr_listener)

    def trial_selection_events_trigger(self):
        """
        Open the multiple selector window.
        The user can select the events he wants the source estimation to be computed on.
        """
        title = "Select the trial's events used for computing the source estimation:"
        events_ids_list = list(self.event_ids.keys())
        self.events_selector_controller = multipleSelectorController(events_ids_list, title, box_checked=True,
                                                                     element_type="events")
        self.events_selector_controller.set_listener(self.snr_listener)

    """
    Plots
    """
    # noinspection PyTypeChecker
    @staticmethod
    def plot_SNRs(first_SNRs, second_SNRs, t_values, SNR_methods):
        """
        Plot the SNRs
        :param first_SNRs: The SNRs computed over the first independent variable.
        :type first_SNRs: list of, list of float
        :param second_SNRs: The SNRs computed over the second independent variable.
        :type second_SNRs: list of, list of float
        :param t_values: T-values computed over the SNRs of the two independent variables.
        :type t_values: list of float
        :param SNR_methods: SNR methods
        :type SNR_methods: list of str
        """
        res = []
        for i in range(len(first_SNRs)):
            res.append([])
            res[i].append(str(round(np.mean(first_SNRs[i]), 3)))
            res[i].append(str(round(np.std(first_SNRs[i]), 3)))
            res[i].append(str(round(np.mean(second_SNRs[i]), 3)))
            res[i].append(str(round(np.std(second_SNRs[i]), 3)))
            res[i].append(str(round(t_values[i], 3)))
        for i in range(len(SNR_methods)):
            if SNR_methods[i] == "Sample Correlation Coefficient":
                SNR_methods[i] = "Sample Correlation\nCoefficient"

        fig, ax = plt.subplots()
        fig.patch.set_visible(False)  # hide axes
        ax.axis('off')
        ax.axis('tight')
        ax.table(cellText=res, rowLabels=SNR_methods,
                 colLabels=['First variable\nSNR mean\nvalue (dB)', 'First variable\nSNR standard\ndeviation (dB)',
                            'Second variable\nSNR mean\nvalue (dB)', 'Second variable\nSNR standard\ndeviation (dB)',
                            'P-values'],
                 cellLoc='center', rowLoc='center', colLoc='center', loc='center')
        fig.tight_layout()
        plt.show()

    """
    Utils
    """
    def check_element_type(self, elements_selected, element_type):
        if element_type == "snr":
            self.set_snr_methods_selected(elements_selected)
        elif element_type == "channels":
            self.set_channels_selected(elements_selected)
        elif element_type == "indexes" or element_type == "events":
            self.set_trials_selected(elements_selected, element_type)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: signalToNoiseRatioController
        """
        self.snr_listener = listener

    def set_snr_methods_selected(self, snr_methods):
        """
        Set the SNR methods selected in the multiple selector window.
        :param snr_methods: SNR methods selected
        :type snr_methods: list of str
        """
        self.snr_methods = snr_methods

    def set_channels_selected(self, channels_selected):
        """
        Set the channels selected in the multiple selector window.
        :param channels_selected: Channels selected.
        :type channels_selected: list of str
        """
        self.channels_selected = channels_selected

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
                trials_to_use.append(int(trial) - 1)  # -1 To get index in the list, not "position"
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

    def get_first_independent_variable_selected(self):
        """
        Get the first independent variable selected by the user.
        :return: First independent variable selected
        :rtype: str
        """
        for i in range(1, self.first_independent_variable_layout.count()):  # Being at 1 because of the label
            check_box = self.first_independent_variable_layout.itemAt(i).widget()
            if check_box.isChecked():
                return check_box.text()

    def get_second_independent_variable_selected(self):
        """
        Get the second independent variable selected by the user.
        :return: Second independent variable selected
        :rtype: str
        """
        for i in range(1, self.second_independent_variable_layout.count()): # Being at 1 because of the label
            check_box = self.second_independent_variable_layout.itemAt(i).widget()
            if check_box.isChecked():
                return check_box.text()
