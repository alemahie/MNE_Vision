#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ERP controller
"""

from plots.erp.erp_listener import erpListener
from plots.erp.erp_view import erpView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class erpController(erpListener):
    def __init__(self, all_channels_names):
        self.main_listener = None
        self.erp_view = erpView(all_channels_names)
        self.erp_view.set_listener(self)

        self.erp_view.show()

    def cancel_button_clicked(self):
        self.erp_view.close()

    def confirm_button_clicked(self, channels_selected):
        self.main_listener.plot_ERP_image_information(channels_selected)
        self.erp_view.close()

    """
    Getters
    """
    def get_channels_selected(self, channels_selected):
        self.erp_view.set_channels_selected(channels_selected)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
