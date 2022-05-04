#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Topographies controller
"""

from plots.topographies.topographies_listener import topographiesListener
from plots.topographies.topographies_view import topographiesView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class topographiesController(topographiesListener):
    def __init__(self):
        self.main_listener = None
        self.topographies_view = topographiesView()
        self.topographies_view.set_listener(self)

        self.topographies_view.show()

    def cancel_button_clicked(self):
        self.topographies_view.close()

    def confirm_button_clicked(self, time_points, mode):
        self.topographies_view.close()
        self.main_listener.plot_topographies_information(time_points, mode)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        self.erp_view.set_channels_selected(elements_selected)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
