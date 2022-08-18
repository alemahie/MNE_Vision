#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Spectro-Temporal Connectivity Controller
"""

from connectivity.spectro_temporal_connectivity.spectro_temporal_connectivity_listener import \
    spectroTemporalConnectivityListener
from connectivity.spectro_temporal_connectivity.spectro_temporal_connectivity_view import \
    spectroTemporalConnectivityView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class spectroTemporalConnectivityController(spectroTemporalConnectivityListener):
    def __init__(self):
        self.main_listener = None
        self.spectro_temporal_connectivity_view = spectroTemporalConnectivityView()
        self.spectro_temporal_connectivity_view.set_listener(self)

        self.spectro_temporal_connectivity_view.show()

    def cancel_button_clicked(self):
        self.spectro_temporal_connectivity_view.close()

    def confirm_button_clicked(self):
        self.spectro_temporal_connectivity_view.close()
        self.main_listener.spectro_temporal_connectivity_information()

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
