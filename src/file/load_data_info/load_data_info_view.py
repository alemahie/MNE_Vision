#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Load Data Info View
"""

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QComboBox, QLineEdit, QHBoxLayout, QVBoxLayout

from utils.elements_selector.elements_selector_controller import multipleSelectorController
from utils.view.separator import create_layout_separator


__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class loadDataInfoView(QWidget):
    def __init__(self, channel_names, tmin, tmax):
        """
        Window displaying the parameters for loading additional data information.
        :param channel_names: Channels' names
        :type channel_names: list of str
        :param tmin: Start time of the epoch or raw file
        :type tmin: float
        :param tmax: End time of the epoch or raw file
        :type tmax: float
        """
        super().__init__()
        self.load_data_listener = None

        self.all_channels_names = channel_names
        self.channels_selected = None
        self.channels_selector_controller = None

        self.setWindowTitle("Load Data Info")

        self.global_layout = QVBoxLayout()
        self.setLayout(self.global_layout)

        # Dataset Name
        self.dataset_name_widget = QWidget()
        self.dataset_name_layout = QHBoxLayout()
        self.dataset_name_line = QLineEdit()
        self.dataset_name_layout.addWidget(QLabel("Dataset name : "))
        self.dataset_name_layout.addWidget(self.dataset_name_line)
        self.dataset_name_widget.setLayout(self.dataset_name_layout)

        # Parameters
        self.parameters_widget = QWidget()
        self.grid_layout = QGridLayout()

        self.montage_box = QComboBox()
        self.montage_box.addItems(["default", "standard_1005", "standard_1020", "standard_alphabetic", "standard_postfixed",
                                   "standard_prefixed", "standard_primed", "biosemi16", "biosemi32", "biosemi64", "biosemi128",
                                   "biosemi160", "biosemi256", "easycap-M1", "easycap-M10", "EGI_256", "GSN-HydroCel-32",
                                   "GSN-HydroCel-64_1.0", "GSN-HydroCel-65_1.0", "GSN-HydroCel-128", "GSN-HydroCel-129",
                                   "GSN-HydroCel-256", "GSN-HydroCel-257", "mgh60", "mgh70", "artinis-octamon", "artinis-brite23"])

        self.channels_selection_button = QPushButton("&Channels ...", self)
        self.channels_selection_button.clicked.connect(self.channels_selection_trigger)

        self.data_start_line = QLineEdit(str(tmin))
        self.data_start_line.setValidator(QDoubleValidator())
        self.data_end_line = QLineEdit(str(tmax))
        self.data_end_line.setValidator(QDoubleValidator())

        self.grid_layout.addWidget(QLabel("Montage : "), 0, 0)
        self.grid_layout.addWidget(self.montage_box, 0, 1)
        self.grid_layout.addWidget(QLabel("Channels : "), 1, 0)
        self.grid_layout.addWidget(self.channels_selection_button, 1, 1)
        self.grid_layout.addWidget(QLabel("Data start time (sec) : "), 2, 0)
        self.grid_layout.addWidget(self.data_start_line, 2, 1)
        self.grid_layout.addWidget(QLabel("Data end time (sec) : "), 3, 0)
        self.grid_layout.addWidget(self.data_end_line, 3, 1)
        self.parameters_widget.setLayout(self.grid_layout)

        # Cancel Confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_load_data_info_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_load_data_info_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        # Layout
        self.global_layout.addWidget(self.dataset_name_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.parameters_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.cancel_confirm_widget)

    """
    Triggers
    """
    def cancel_load_data_info_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.load_data_listener.cancel_button_clicked()

    def confirm_load_data_info_trigger(self):
        """
        Retrieve the all the additional information and send the information to the controller.
        Check if the float input are in the acceptable range (between tmin and tmax).
        """
        montage = self.montage_box.currentText()

        channels_selected = self.channels_selected
        if channels_selected is None:   # The channel selection has not been opened, take all channels
            channels_selected = self.all_channels_names

        tmin = None
        tmax = None
        if self.data_start_line.hasAcceptableInput():
            tmin = self.data_start_line.text()
            tmin = float(tmin.replace(',', '.'))
        if self.data_end_line.hasAcceptableInput():
            tmax = self.data_end_line.text()
            tmax = float(tmax.replace(',', '.'))

        dataset_name = self.dataset_name_line.text()
        if len(dataset_name) == 0:  # No Name
            dataset_name = "No Name"

        self.load_data_listener.confirm_button_clicked(montage, channels_selected, tmin, tmax, dataset_name)

    def channels_selection_trigger(self):
        """
        Open the multiple selector window.
        The user can select multiple channels.
        """
        title = "Select the channels to be loaded :"
        self.channels_selector_controller = multipleSelectorController(self.all_channels_names, title, box_checked=True,
                                                                       unique_box=False)
        self.channels_selector_controller.set_listener(self.load_data_listener)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: loadDataInfoController
        """
        self.load_data_listener = listener

    def set_channels_selected(self, channels_selected):
        """
        Set the channel selected in the multiple selector window.
        :param channels_selected: Channels selected.
        :type channels_selected: list of str
        """
        self.channels_selected = channels_selected
