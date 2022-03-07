#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ICA decomposition controller
"""

from tools.ICA_decomposition.ICA_decomposition_view import icaDecompositionView
from tools.ICA_decomposition.ICA_decomposition_listener import icaDecompositionListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class icaDecompositionController(icaDecompositionListener):
    def __init__(self):
        self.main_listener = None
        self.ica_decomposition_view = icaDecompositionView()
        self.ica_decomposition_view.set_listener(self)

        self.ica_decomposition_view.show()

    def cancel_button_clicked(self):
        self.ica_decomposition_view.close()

    def confirm_button_clicked(self, ica_method):
        self.ica_decomposition_view.close()
        self.main_listener.ica_decomposition_information(ica_method)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
