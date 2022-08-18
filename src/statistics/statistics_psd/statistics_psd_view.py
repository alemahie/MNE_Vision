#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics PSD View
"""
import numpy as np
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, \
    QButtonGroup, QScrollArea, QCheckBox
from matplotlib import pyplot as plt
from mne.stats import permutation_t_test, ttest_1samp_no_p, ttest_ind_no_p
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


class statisticsPsdView(QWidget):
    def __init__(self, minimum_time, maximum_time, event_ids, all_channels_names):
        """
        Window displaying the parameters for computing the power spectral density on the dataset.
        :param minimum_time: Minimum time of the epochs from which the power spectral density can be computed.
        :type minimum_time: float
        :param maximum_time: Maximum time of the epochs from which the power spectral density can be computed.
        :type maximum_time: float
        :param event_ids: The events' ids
        :type event_ids: dict
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        """
        super().__init__()
        self.power_spectral_density_listener = None

        self.channels_selector_controller = None

        self.channels_selection_opened = False
        self.channels_selected = None

        self.all_channels_names = all_channels_names
        self.event_ids = event_ids

        self.setWindowTitle("Statistics PSD")

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

        # Lines
        self.lines_widget = QWidget()
        self.lines_layout = QGridLayout()

        self.minimum_frequency_line = QLineEdit("2,0")
        self.minimum_frequency_line.setValidator(QDoubleValidator())
        self.maximum_frequency_line = QLineEdit("25,0")
        self.maximum_frequency_line.setValidator(QDoubleValidator())
        self.minimum_time_line = QLineEdit(str(minimum_time))
        self.minimum_time_line.setValidator(QDoubleValidator(minimum_time, maximum_time, 3))
        self.maximum_time_line = QLineEdit(str(maximum_time))
        self.maximum_time_line.setValidator(QDoubleValidator(minimum_time, maximum_time, 3))
        self.time_points_line = QLineEdit("6 10 22")

        self.lines_layout.addWidget(QLabel("Minimum frequency of interest (Hz) : "), 0, 0)
        self.lines_layout.addWidget(self.minimum_frequency_line, 0, 1)
        self.lines_layout.addWidget(QLabel("Maximum frequency of interest (Hz) : "), 1, 0)
        self.lines_layout.addWidget(self.maximum_frequency_line, 1, 1)
        self.lines_layout.addWidget(QLabel("Minimum time of interest (sec) : "), 2, 0)
        self.lines_layout.addWidget(self.minimum_time_line, 2, 1)
        self.lines_layout.addWidget(QLabel("Maximum time of interest (sec) : "), 3, 0)
        self.lines_layout.addWidget(self.maximum_time_line, 3, 1)
        self.lines_layout.addWidget(QLabel("Time points for the topographies to plot (sec) : "), 4, 0)
        self.lines_layout.addWidget(self.time_points_line, 4, 1)
        self.lines_widget.setLayout(self.lines_layout)

        # Cancel confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_power_spectral_density_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_power_spectral_density_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        # Layout
        self.global_layout.addWidget(self.statistics_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.channels_selection_widget)
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
    def cancel_power_spectral_density_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.power_spectral_density_listener.cancel_button_clicked()

    def confirm_power_spectral_density_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        try:
            if self.channels_selection_opened:
                if len(self.channels_selected) >= 1:
                    minimum_frequency = None
                    maximum_frequency = None
                    if self.minimum_frequency_line.hasAcceptableInput():
                        minimum_frequency = float(self.minimum_frequency_line.text().replace(',', '.'))
                    if self.maximum_frequency_line.hasAcceptableInput():
                        maximum_frequency = float(self.maximum_frequency_line.text().replace(',', '.'))
                    minimum_time = float(self.minimum_time_line.text().replace(',', '.'))
                    maximum_time = float(self.maximum_time_line.text().replace(',', '.'))
                    topo_time_points = self.create_array_from_time_points()

                    stats_first_variable = self.get_first_independent_variable_selected()
                    stats_second_variable = self.get_second_independent_variable_selected()

                    self.power_spectral_density_listener.confirm_button_clicked(minimum_frequency, maximum_frequency, minimum_time,
                                                                                maximum_time, topo_time_points, self.channels_selected,
                                                                                stats_first_variable, stats_second_variable)
                else:
                    error_message = "Please select at least 1 channel in the 'channel selection' menu before starting the computation."
                    error_window = errorWindow(error_message)
                    error_window.show()
            else:
                error_message = "Please select a channel in the 'channel selection' menu before starting the computation."
                error_window = errorWindow(error_message)
                error_window.show()
        except Exception as e:
            print(e)

    def channels_selection_trigger(self):
        """
        Open the multiple selector window.
        The user can select multiple channels.
        """
        title = "Select the channel used for the PSD computation :"
        self.channels_selector_controller = multipleSelectorController(self.all_channels_names, title, box_checked=True, unique_box=True)
        self.channels_selector_controller.set_listener(self.power_spectral_density_listener)
        self.channels_selection_opened = True

    """
    Plots
    """
    @staticmethod
    def plot_psd(psd_fig_one, topo_fig_one, psd_fig_two, topo_fig_two):
        """
        Plot the power spectral density.
        :param psd_fig_one: The figure of the actual power spectral density's data computed on the first independent variable
        :type psd_fig_one: matplotlib.Figure
        :param topo_fig_one: The figure of the topographies of the actual power spectral density's data computed on the first independent variable
        :type topo_fig_one: matplotlib.Figure
        :param psd_fig_two: The figure of the actual power spectral density's data computed on the second independent variable
        :type psd_fig_two: matplotlib.Figure
        :param topo_fig_two: The figure of the topographies of the actual power spectral density's data computed on the second independent variable
        :type topo_fig_two: matplotlib.Figure
        """
        try:
            # First Variable
            psd_fig_one.axes[0].set_title("Power spectral density - First independent variable")
            psd_fig_one.show()
            topo_fig_one.suptitle("PSD Topographies - First independent variable")
            topo_fig_one.show()
            # Second variable
            psd_fig_two.axes[0].set_title("Power spectral density - Second independent variable")
            psd_fig_two.show()
            topo_fig_two.suptitle("PSD Topographies - Second independent variable")
            topo_fig_two.show()

            # Stats
            psd_one_data = psd_fig_one.axes[0].lines[2].get_ydata()
            psd_two_data = psd_fig_two.axes[0].lines[2].get_ydata()
            # Get the first axis corresponding to the main plot, then the line 2 is the plotted psd data (0 and 1 are the axis).

            # t_values = ttest_ind_no_p(psd_one_data, psd_two_data)
            # t_values = ttest_1samp_no_p(np.array([psd_one_data, psd_two_data]))

            p_values = []
            for i in range(len(psd_one_data)):
                new_t_values, new_p_values = ttest_1samp(np.array([psd_one_data[i], psd_two_data[i]]), popmean=0.0, nan_policy="omit")
                p_values.append(new_p_values)

            print(p_values)

            x = psd_fig_one.axes[0].lines[2].get_xdata()
            # Plot
            fig, ax = plt.subplots()
            ax.plot(x, p_values)
            ax.set_title("P-values for PSD")

            ax.set_ylim([0.001, 1.0])
            ax.set_yscale("log")

            fig.show()
        except Exception as error:
            error_message = "An error has occurred during the computation of the PSD"
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()

    """
    Utils
    """
    def create_array_from_time_points(self):
        """
        Create an array of time points depending on the time points given.
        :return: The time points for the topomaps.
        :rtype: list of float
        """
        try:
            time_points = self.time_points_line.text()
            if time_points == "":
                return [6.0, 10.0, 22.0]
            else:
                split_time_points = time_points.split()
                float_time_points = []
                for time_point in split_time_points:
                    float_time_points.append(float(time_point.replace(',', '.')))
                return float_time_points
        except Exception as error:
            error_message = "The time points provided are not following the right format, please use integer separated " \
                            "by spaces."
            error_window = errorWindow(error_message)
            error_window.show()

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: powerSpectralDensityController
        """
        self.power_spectral_density_listener = listener

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
        for i in range(1, self.second_independent_variable_layout.count()):     # Being at 1 because of the label
            check_box = self.second_independent_variable_layout.itemAt(i).widget()
            if check_box.isChecked():
                return check_box.text()
