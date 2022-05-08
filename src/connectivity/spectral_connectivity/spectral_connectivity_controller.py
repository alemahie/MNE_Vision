#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Spectral Connectivity Controller
"""

from connectivity.spectral_connectivity.spectral_connectivity_listener import spectralConnectivityListener
from connectivity.spectral_connectivity.spectral_connectivity_view import spectralConnectivityView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class spectralConnectivityController(spectralConnectivityListener):
    def __init__(self):
        self.main_listener = None
        self.spectral_connectivity_view = spectralConnectivityView()
        self.spectral_connectivity_view.set_listener(self)

        self.spectral_connectivity_view.show()

    def cancel_button_clicked(self):
        self.spectral_connectivity_view.close()

    def confirm_button_clicked(self):
        self.spectral_connectivity_view.close()
        self.main_listener.spectral_connectivity_information()

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
