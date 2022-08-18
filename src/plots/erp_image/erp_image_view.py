#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ERP image view
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel

from utils.elements_selector.elements_selector_controller import multipleSelectorController
from utils.view.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class erpImageView(QWidget):
    def __init__(self, all_channels_names):
        """
        Window displaying the parameters for computing an ERP image on the dataset.
        :param all_channels_names: All the channels' names
        :type all_channels_names: list of str
        """
        super().__init__()
        self.erp_image_listener = None
        self.all_channels_names = all_channels_names
        self.channels_selector_controller = None
        self.channel_selected = None
        self.channels_selection_opened = False

        self.setWindowTitle("Event Related Potentials Image")

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.channels_selection_button = QPushButton("&Channels ...", self)
        self.channels_selection_button.clicked.connect(self.channels_selection_trigger)

        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_erp_image_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_erp_image_trigger)

        self.grid_layout.addWidget(QLabel("Channels : "), 0, 0)
        self.grid_layout.addWidget(self.channels_selection_button, 0, 1)
        self.grid_layout.addWidget(self.cancel, 1, 0)
        self.grid_layout.addWidget(self.confirm, 1, 1)

    """
    Triggers
    """
    def cancel_erp_image_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.erp_image_listener.cancel_button_clicked()

    def confirm_erp_image_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        if self.channels_selection_opened:
            self.erp_image_listener.confirm_button_clicked(self.channel_selected)
        else:
            error_message = "Please select a channel in the 'channel selection' menu before starting the computation."
            error_window = errorWindow(error_message)
            error_window.show()

    def channels_selection_trigger(self):
        """
        Open the multiple selector window.
        The user can select a single channel.
        """
        title = "Select the channels used for the ERP image computation :"
        self.channels_selector_controller = multipleSelectorController(self.all_channels_names, title, box_checked=False,
                                                                       unique_box=True)
        self.channels_selector_controller.set_listener(self.erp_image_listener)
        self.channels_selection_opened = True

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: erpImageController
        """
        self.erp_image_listener = listener

    def set_channels_selected(self, channel_selected):
        """
        Set the channel selected in the multiple selector window.
        :param channel_selected: The channel selected.
        :type channel_selected: str
        """
        self.channel_selected = channel_selected
