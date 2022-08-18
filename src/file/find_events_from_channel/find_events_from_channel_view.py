#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Find Events From Channel View
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QHBoxLayout, QLabel

from utils.elements_selector.elements_selector_controller import multipleSelectorController

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class findEventsFromChannelView(QWidget):
    def __init__(self, all_channels_names):
        """
        Window displaying the parameters for finding events from a stimulation channel.
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        """
        super().__init__()
        self.find_events_from_channel_listener = None
        self.all_channels_names = all_channels_names
        self.channel_selected = None
        self.channels_selector_controller = None

        self.setWindowTitle("Find Events From Channel")

        self.vertical_layout = QGridLayout()
        self.setLayout(self.vertical_layout)

        self.channel_widget = QWidget()
        self.channel_layout = QHBoxLayout()
        self.channel_label = QLabel("Channels : ")
        self.channels_selection_button = QPushButton("&Channels ...", self)
        self.channels_selection_button.clicked.connect(self.channels_selection_trigger)
        self.channel_layout.addWidget(self.channel_label)
        self.channel_layout.addWidget(self.channels_selection_button)
        self.channel_widget.setLayout(self.channel_layout)

        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_find_events_from_channel_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_find_events_from_channel_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.channel_widget)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    """
    Triggers
    """
    def cancel_find_events_from_channel_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.find_events_from_channel_listener.cancel_button_clicked()

    def confirm_find_events_from_channel_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        stim_channel = self.channel_selected
        self.find_events_from_channel_listener.confirm_button_clicked(stim_channel)

    def channels_selection_trigger(self):
        """
        Open the multiple selector window.
        The user can select a single channel.
        """
        title = "Select the channels used for finding the events :"
        self.channels_selector_controller = multipleSelectorController(self.all_channels_names, title, box_checked=False,
                                                                       unique_box=True)
        self.channels_selector_controller.set_listener(self.find_events_from_channel_listener)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: findEventsFromChannelController
        """
        self.find_events_from_channel_listener = listener

    def set_channels_selected(self, channel_selected):
        """
        Set the channel selected in the multiple selector window.
        :param channel_selected: Channel selected.
        :type channel_selected: str
        """
        self.channel_selected = channel_selected
