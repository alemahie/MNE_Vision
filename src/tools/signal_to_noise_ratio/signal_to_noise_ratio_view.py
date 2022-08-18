#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SNR view
"""

import numpy as np
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QButtonGroup, QCheckBox, \
    QGridLayout
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


class signalToNoiseRatioView(QWidget):
    def __init__(self, all_channels_names, event_values, event_ids):
        """
        Window displaying the parameters for computing the SNR on the dataset.
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

        self.setWindowTitle("Signal-To-Noise Ratio")

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

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

        # On what to compute
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
        self.vertical_layout.addWidget(self.snr_selection_widget)
        self.vertical_layout.addWidget(self.channels_selection_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.method_widget)
        self.vertical_layout.addWidget(self.save_load_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.trial_selection_widget)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

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
        if self.trials_selected is None:
            trials_selected = [i for i in range(len(self.event_values))]
        else:
            trials_selected = self.trials_selected
        self.snr_listener.confirm_button_clicked(self.snr_methods, source_method, read, write, self.channels_selected,
                                                 trials_selected)

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
    def plot_SNRs(SNRs, SNR_methods):
        """
        Plot the SNRs
        :param SNRs: SNRs
        :type SNRs: list of, list of float
        :param SNR_methods: SNR methods
        :type SNR_methods: list of str
        """
        res = []
        for i in range(len(SNRs)):
            res.append([])
            res[i].append(str(round(np.mean(SNRs[i]), 3)))
            res[i].append(str(round(np.std(SNRs[i]), 3)))
        fig, ax = plt.subplots()
        fig.patch.set_visible(False)  # hide axes
        ax.axis('off')
        ax.axis('tight')
        ax.table(cellText=res, rowLabels=SNR_methods, colLabels=['SNR mean value (dB)', 'SNR standard deviation (dB)'],
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
