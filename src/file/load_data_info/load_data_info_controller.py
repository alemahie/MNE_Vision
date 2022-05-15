#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Load Data Info Controller
"""

from file.load_data_info.load_data_info_listener import loadDataInfoListener
from file.load_data_info.load_data_info_view import loadDataInfoView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class loadDataInfoController(loadDataInfoListener):
    def __init__(self, channel_names, tmin, tmax):
        self.main_listener = None
        self.load_data_info_view = loadDataInfoView(channel_names, tmin, tmax)
        self.load_data_info_view.set_listener(self)

        self.load_data_info_view.show()

    def cancel_button_clicked(self):
        self.load_data_info_view.close()

    def confirm_button_clicked(self, montage, channels_selected, tmin, tmax):
        self.load_data_info_view.close()
        self.main_listener.load_data_info_information(montage, channels_selected, tmin, tmax)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        self.load_data_info_view.set_channels_selected(elements_selected)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
