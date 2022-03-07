#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Re-referencing controller
"""

from tools.re_referencing.re_referencing_view import reReferencingView
from tools.re_referencing.re_referencing_listener import reReferencingListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class reReferencingController(reReferencingListener):
    def __init__(self, reference, all_channels_names):
        self.main_listener = None
        self.re_referencing_view = reReferencingView(reference, all_channels_names)
        self.re_referencing_view.set_listener(self)

        self.re_referencing_view.show()

    def cancel_button_clicked(self):
        self.re_referencing_view.close()

    def confirm_button_clicked(self, references):
        self.main_listener.re_referencing_information(references)
        self.re_referencing_view.close()

    def get_channels_selected(self, channels_selected):
        self.re_referencing_view.set_channels_selected(channels_selected)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
