#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data Exportation Controller
"""

from utils.data_exportation.data_exportation_listener import dataExportationListener
from utils.data_exportation.data_exportation_view import dataExportationView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class dataExportationController(dataExportationListener):
    def __init__(self):
        """
        Controller for retrieving the path for data exportation of the computation.
        Create a new window for specifying some parameters.
        """
        self.main_listener = None
        self.data_exportation_view = dataExportationView()
        self.data_exportation_view.set_listener(self)

        self.data_exportation_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.data_exportation_view.close()

    def confirm_button_clicked(self, export_path):
        """
        Close the window and send the information to the controller.
        :param export_path: Path where the source estimation data will be stored.
        :type export_path: str
        """
        self.main_listener.additional_parameters_information(export_path)
        self.data_exportation_view.close()

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the main listener so that the controller is able to communicate with the other controller.
        :param listener: main listener
        :type listener: controller
        """
        self.main_listener = listener
