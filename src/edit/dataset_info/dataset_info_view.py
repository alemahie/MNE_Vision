#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dataset info view
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout

from utils.elements_selector.elements_selector_controller import multipleSelectorController
from utils.view.separator import create_layout_separator

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class datasetInfoView(QWidget):
    def __init__(self, all_channels_names):
        """
        Window displaying the dataset's information.
        """
        super().__init__()
        self.dataset_info_listener = None

        self.all_channels_names = all_channels_names
        self.channels_selected = None
        self.channels_selector_controller = None

        self.setWindowTitle("Dataset Information")

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        # Channels
        self.channels_selection_widget = QWidget()
        self.channels_selection_layout = QHBoxLayout()
        self.channels_selection_button = QPushButton("&Channels ...", self)
        self.channels_selection_button.clicked.connect(self.channels_selection_trigger)
        self.channels_selection_layout.addWidget(QLabel("Select a new reference : "))
        self.channels_selection_layout.addWidget(self.channels_selection_button)
        self.channels_selection_widget.setLayout(self.channels_selection_layout)

        # Cancel Confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_dataset_info_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.confirm.clicked.connect(self.confirm_dataset_info_trigger)

        self.vertical_layout.addWidget(self.channels_selection_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    """
    Triggers
    """
    def cancel_dataset_info_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.dataset_info_listener.cancel_button_clicked()

    def confirm_dataset_info_trigger(self):
        """
        Retrieve the channel name and location and send the information to the controller.
        """
        self.dataset_info_listener.confirm_button_clicked(self.channels_selected)

    def channels_selection_trigger(self):
        """
        Open the multiple selector window.
        The user can select multiple channels.
        """
        title = "Select the channels used for the reference :"
        self.channels_selector_controller = multipleSelectorController(self.all_channels_names, title, box_checked=True,
                                                                       element_type="channels")
        self.channels_selector_controller.set_listener(self.dataset_info_listener)

    """
    Utils
    """
    def check_element_type(self, elements_selected, element_type):
        if element_type == "channels":
            self.set_channel_selected(elements_selected)

    def set_channel_selected(self, channels_selected):
        """
        Set the channels selected in the multiple selector window.
        :param channels_selected: Channels selected.
        :type channels_selected: list of str
        """
        self.channels_selected = channels_selected

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: datasetInfoController
        """
        self.dataset_info_listener = listener
