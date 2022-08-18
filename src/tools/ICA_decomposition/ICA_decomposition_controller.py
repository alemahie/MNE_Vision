#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ICA decomposition controller
"""

from tools.ICA_decomposition.ICA_decomposition_view import icaDecompositionView
from tools.ICA_decomposition.ICA_decomposition_listener import icaDecompositionListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class icaDecompositionController(icaDecompositionListener):
    def __init__(self):
        """
        Controller for computing the ICA decomposition on the dataset.
        Create a new window for specifying some parameters.
        """
        self.main_listener = None
        self.ica_decomposition_view = icaDecompositionView()
        self.ica_decomposition_view.set_listener(self)

        self.ica_decomposition_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.ica_decomposition_view.close()

    def confirm_button_clicked(self, ica_method):
        """
        Close the window and send the information to the main controller.
        :param ica_method: Method used for performing the ICA decomposition
        :type ica_method: str
        """
        self.ica_decomposition_view.close()
        self.main_listener.ica_decomposition_information(ica_method)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the main listener so that the controller is able to communicate with the main controller.
        :param listener: main listener
        :type listener: mainController
        """
        self.main_listener = listener
