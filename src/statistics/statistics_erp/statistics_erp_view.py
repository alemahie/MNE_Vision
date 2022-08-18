#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics ERP view
"""

import numpy as np
from matplotlib import pyplot as plt

from copy import deepcopy

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QButtonGroup, QScrollArea, QCheckBox
from matplotlib.scale import LogScale
from mne import combine_evoked
from mne.stats import ttest_ind_no_p, permutation_t_test, ttest_1samp_no_p
from scipy.stats import ttest_ind

from utils.view.separator import create_layout_separator
from utils.elements_selector.elements_selector_controller import multipleSelectorController
from utils.view.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class statisticsErpView(QWidget):
    def __init__(self, all_channels_names, event_ids):
        """
        Window displaying the parameters for computing the ERPs on the dataset.
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        :param event_ids: The events' ids
        :type event_ids: dict
        """
        super().__init__()
        self.erp_listener = None

        self.all_channels_names = all_channels_names
        self.event_ids = event_ids

        self.channels_selector_controller = None
        self.channels_selected = None
        self.channels_selection_opened = False

        self.setWindowTitle("Statistics ERP")

        self.global_layout = QVBoxLayout()
        self.setLayout(self.global_layout)

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

        # Buttons
        self.channels_selection_widget = QWidget()
        self.channels_selection_layout = QHBoxLayout()
        self.channels_selection_button = QPushButton("&Channels ...", self)
        self.channels_selection_button.clicked.connect(self.channels_selection_trigger)
        self.channels_selection_layout.addWidget(QLabel("Channels : "))
        self.channels_selection_layout.addWidget(self.channels_selection_button)
        self.channels_selection_widget.setLayout(self.channels_selection_layout)

        # Cancel confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_erp_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_erp_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.global_layout.addWidget(self.statistics_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.channels_selection_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.cancel_confirm_widget)

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
    def cancel_erp_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.erp_listener.cancel_button_clicked()

    def confirm_erp_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        if self.channels_selection_opened:
            if len(self.channels_selected) >= 1:
                # Need at least 1 channels, because with 0 we have no info.

                stats_first_variable = self.get_first_independent_variable_selected()
                stats_second_variable = self.get_second_independent_variable_selected()

                self.erp_listener.confirm_button_clicked(self.channels_selected, stats_first_variable, stats_second_variable)
            else:
                error_message = "Please select at least 1 channel in the 'channel selection' menu before starting the computation."
                error_window = errorWindow(error_message)
                error_window.show()
        else:
            error_message = "Please select a channel in the 'channel selection' menu before starting the computation."
            error_window = errorWindow(error_message)
            error_window.show()

    def channels_selection_trigger(self):
        """
        Open the multiple selector window.
        The user can select multiple channels.
        """
        title = "Select the channel used for the ERP computation :"
        self.channels_selector_controller = multipleSelectorController(self.all_channels_names, title, box_checked=True, unique_box=True)
        self.channels_selector_controller.set_listener(self.erp_listener)
        self.channels_selection_opened = True

    """
    Plots
    """
    def plot_erps(self, channels_selected, file_data, stats_first_variable, stats_second_variable):
        """
        Plot the ERPs and the statistics.
        :param channels_selected: The channels selected for the computation
        :type channels_selected: list of str
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        # First variable
        file_data_one = deepcopy(file_data)
        mask = self.create_mask_from_variable_to_keep(file_data_one, stats_first_variable)
        file_data_one = file_data_one.drop(mask)
        erps_first = file_data_one.average(picks=channels_selected, )
        # Second variable
        file_data_two = deepcopy(file_data)
        mask = self.create_mask_from_variable_to_keep(file_data_two, stats_second_variable)
        file_data_two = file_data_two.drop(mask)
        erps_second = file_data_two.average(picks=channels_selected)
        # Stats
        try:
            p_values = []

            data_first = file_data_one.get_data(picks=channels_selected)
            data_second = file_data_two.get_data(picks=channels_selected)

            for i in range(len(data_first[0, 0])):
                new_t_values, new_p_values = ttest_ind(data_first[:, 0, i], data_second[:, 0, i])
                p_values.append(new_p_values)

            fig_one = erps_first.plot(show=False)
            fig_two = erps_second.plot(show=False)

            fig_one.show()
            fig_two.show()

            fig, ax = plt.subplots()
            ax.plot(file_data.times, p_values)
            ax.set_title("P-values for ERP")

            ax.set_ylim([0.001, 1.0])
            ax.set_yscale("log")

            fig.show()
        except Exception as e:
            print(e)

    """
    Utils
    """
    @staticmethod
    def create_mask_from_variable_to_keep(file_data, stats_variable):
        """
        Create a mask to know which trial to keep and which one to remove for the computation.
        :return mask: Mask of trials to remove. True means remove, and False means keep.
        :rtype mask: list of boolean
        """
        mask = [True for _ in range(len(file_data.events))]
        event_ids = file_data.event_id
        event_id_to_keep = event_ids[stats_variable]
        for i, event in enumerate(file_data.events):
            if event[2] == event_id_to_keep:        # 2 is the event id in the events
                mask[i] = False
        return mask

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: erpController
        """
        self.erp_listener = listener

    def set_channels_selected(self, channels_selected):
        """
        Set the channels selected in the multiple selector window.
        :param channels_selected: Channels selected.
        :type channels_selected: list of str
        """
        self.channels_selected = channels_selected

    """
    Getters
    """
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
