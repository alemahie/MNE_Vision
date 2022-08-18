#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics Time frequency (ERSP/ITC) view
"""

import numpy as np

from matplotlib import pyplot as plt

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QComboBox, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, \
    QButtonGroup, QScrollArea, QCheckBox
from matplotlib.colors import Normalize, LogNorm

from mne.stats import permutation_t_test
from mne.viz import tight_layout
from scipy.stats import ttest_ind, ttest_1samp

from utils.elements_selector.elements_selector_controller import multipleSelectorController
from utils.view.error_window import errorWindow
from utils.view.separator import create_layout_separator

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class statisticsErspItcView(QWidget):
    def __init__(self, all_channels_names, event_ids):
        """
        Window displaying the parameters for computing the ERPs on the dataset.
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        :param event_ids: The events' ids
        :type event_ids: dict
        """
        super().__init__()
        self.time_frequency_ersp_itc_listener = None

        self.all_channels_names = all_channels_names
        self.event_ids = event_ids

        self.channels_selector_controller = None

        self.min_frequency = None
        self.max_frequency = None
        self.channel_selected = None
        self.channels_selection_opened = False

        self.setWindowTitle("Statistics ERSP-ITC")

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

        # Channels
        self.channels_widget = QWidget()
        self.channels_layout = QHBoxLayout()
        self.channels_selection_button = QPushButton("&Channels ...", self)
        self.channels_selection_button.clicked.connect(self.channels_selection_trigger)
        self.channels_layout.addWidget(QLabel("Channels : "))
        self.channels_layout.addWidget(self.channels_selection_button)
        self.channels_widget.setLayout(self.channels_layout)

        # Lines
        self.lines_widget = QWidget()
        self.lines_layout = QGridLayout()
        self.method_box = QComboBox()
        self.method_box.addItems(["Morlet", "Multitaper", "Stockwell"])
        self.low_frequency_line = QLineEdit("6")
        self.low_frequency_line.setValidator(QDoubleValidator())
        self.high_frequency_line = QLineEdit("35")
        self.high_frequency_line.setValidator(QDoubleValidator())
        self.n_cycles_line = QLineEdit("5.0")
        self.n_cycles_line.setValidator(QDoubleValidator())

        self.lines_layout.addWidget(QLabel("Method for Time-frequency computation : "), 0, 0)
        self.lines_layout.addWidget(self.method_box, 0, 1)
        self.lines_layout.addWidget(QLabel("Minimum Frequency of interest (Hz) : "), 1, 0)
        self.lines_layout.addWidget(self.low_frequency_line, 1, 1)
        self.lines_layout.addWidget(QLabel("Maximum Frequency of interest (Hz) : "), 2, 0)
        self.lines_layout.addWidget(self.high_frequency_line, 2, 1)
        self.lines_layout.addWidget(QLabel("Number of cycles : "), 3, 0)
        self.lines_layout.addWidget(self.n_cycles_line, 3, 1)
        self.lines_widget.setLayout(self.lines_layout)

        # Cancel confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_time_frequency_ersp_itc_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_time_frequency_ersp_itc_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        # Layout
        self.global_layout.addWidget(self.statistics_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.channels_widget)
        self.global_layout.addWidget(self.lines_widget)
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
    def cancel_time_frequency_ersp_itc_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.time_frequency_ersp_itc_listener.cancel_button_clicked()

    def confirm_time_frequency_ersp_itc_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        if self.channels_selection_opened:      # Menu channel must have been opened if it exists.
            method_tfr = self.method_box.currentText()
            min_frequency = self.low_frequency_line.text()
            self.min_frequency = float(min_frequency.replace(',', '.'))
            max_frequency = self.high_frequency_line.text()
            self.max_frequency = float(max_frequency.replace(',', '.'))
            n_cycles = self.n_cycles_line.text()
            n_cycles = float(n_cycles.replace(',', '.'))

            stats_first_variable = self.get_first_independent_variable_selected()
            stats_second_variable = self.get_second_independent_variable_selected()

            self.time_frequency_ersp_itc_listener.confirm_button_clicked(method_tfr, self.channel_selected, self.min_frequency,
                                                                         self.max_frequency, n_cycles, stats_first_variable,
                                                                         stats_second_variable)
        else:
            error_message = "Please select a channel in the 'channel selection' menu before starting the computation."
            error_window = errorWindow(error_message)
            error_window.show()

    def channels_selection_trigger(self):
        """
        Open the multiple selector window.
        The user can select a single channel.
        """
        title = "Select the channel used for the Time-frequency computation :"
        self.channels_selector_controller = multipleSelectorController(self.all_channels_names, title,
                                                                       box_checked=False, unique_box=True)
        self.channels_selector_controller.set_listener(self.time_frequency_ersp_itc_listener)
        self.channels_selection_opened = True

    """
    Plots
    """
    def plot_ersp_itc(self, channel_selected, power_one, itc_one, power_two, itc_two):
        """
        Plot the time-frequency analysis.
        :param channel_selected: The channel selected for the time-frequency analysis.
        :type channel_selected: str
        :param power_one: "power" data of the time-frequency analysis computation of the first independent variable.
        :type power_one: MNE.AverageTFR
        :param itc_one: "itc" data of the time-frequency analysis computation of the first independent variable.
        :type itc_one: MNE.AverageTFR
        :param power_two: "power" data of the time-frequency analysis computation of the second independent variable.
        :type power_two: MNE.AverageTFR
        :param itc_two: "itc" data of the time-frequency analysis computation of the second independent variable.
        :type itc_two: MNE.AverageTFR
        """
        fig, axis = plt.subplots(3, 2)
        # First variable
        power_one.plot(axes=axis[0][0], show=False)
        axis[0][0].set_title("First variable - ERSP")
        itc_one.plot(axes=axis[0][1], show=False)
        axis[0][1].set_title("First variable - ITC")
        # Second variable
        power_two.plot(axes=axis[1][0], show=False)
        axis[1][0].set_title("Second variable - ERSP")
        itc_two.plot(axes=axis[1][1], show=False)
        axis[1][1].set_title("Second variable - ITC")

        # Stats
        power_one_data = power_one.data[0]
        power_two_data = power_two.data[0]
        itc_one_data = itc_one.data[0]
        itc_two_data = itc_two.data[0]

        try:
            all_power_t_values = []
            for i in range(len(power_one_data)):
                all_power_t_values.append([])
                for j in range(len(power_one_data[i])):
                    new_t_values, new_p_values = ttest_1samp(np.array([power_one_data[i][j], power_two_data[i][j]]),
                                                             popmean=0.0, nan_policy="omit")
                    # power_t_values, power_p_values, power_H0 = permutation_t_test(np.array([power_one_data[i], power_two_data[i]]))
                    all_power_t_values[-1].append(new_p_values)
            all_power_t_values = np.array(all_power_t_values)

            all_itc_t_values = []
            for i in range(len(itc_one_data)):
                all_itc_t_values.append([])
                for j in range(len(itc_two_data)):
                    new_t_values, new_p_values = ttest_1samp(np.array([itc_one_data[i][j], itc_two_data[i][j]]),
                                                             popmean=0.0, nan_policy="omit")
                    # itc_t_values, itc_p_values, itc_H0 = permutation_t_test(np.array([itc_one_data[i], itc_two_data[i]]))
                    all_itc_t_values[-1].append(new_p_values)
            all_itc_t_values = np.array(all_itc_t_values)

            # Plot
            x_ticks = axis[0][0].get_xticks()[1:]
            y_ticks = axis[0][0].get_yticks()

            normalization_power = LogNorm(vmin=np.min(all_power_t_values), vmax=np.max(all_power_t_values))
            color_mesh_one = axis[2][0].pcolormesh(all_power_t_values, norm=normalization_power)
            fig.colorbar(color_mesh_one, ax=axis[2][0])
            axis[2][0].set_title("P-values - ERSP")

            """
            axis[2][0].set_xticklabels(x_ticks)
            axis[2][0].set_xlim(x_ticks[0], x_ticks[-1])
            axis[2][0].set_yticklabels(y_ticks)
            axis[2][0].set_ylim(y_ticks[0], y_ticks[-1])
            """

            normalization_itc = LogNorm(vmin=np.min(all_itc_t_values), vmax=np.max(all_itc_t_values))
            color_mesh_two = axis[2][1].pcolormesh(all_itc_t_values, norm=normalization_itc)
            fig.colorbar(color_mesh_two, ax=axis[2][1])
            axis[2][1].set_title("P-values - ITC")

            fig.suptitle(f"Channel : {channel_selected[0]}")
            tight_layout()
            plt.show()
        except Exception as e:
            print(e)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: timeFrequencyErspItcController
        """
        self.time_frequency_ersp_itc_listener = listener

    def set_channels_selected(self, channel_selected):
        """
        Set the channel selected in the multiple selector window.
        :param channel_selected: The channel selected.
        :type channel_selected: str
        """
        self.channel_selected = channel_selected

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
