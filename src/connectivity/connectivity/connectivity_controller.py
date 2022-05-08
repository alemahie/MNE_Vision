#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Connectivity Controller
"""

from connectivity.connectivity.connectivity_listener import connectivityListener
from connectivity.connectivity.connectivity_view import connectivityView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class connectivityController(connectivityListener):
    def __init__(self):
        self.main_listener = None
        self.connectivity_view = connectivityView()
        self.connectivity_view.set_listener(self)

        self.connectivity_view.show()

    def cancel_button_clicked(self):
        self.connectivity_view.close()

    def confirm_button_clicked(self):
        self.connectivity_view.close()
        self.main_listener.connectivity_information()

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
