#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source Estimation Additional Parameters Controller
"""

from tools.source_estimation.additional_parameters.source_estimation_additional_parameters_listener import \
    sourceEstimationAdditionalParametersListener
from tools.source_estimation.additional_parameters.source_estimation_additional_parameters_view import \
    sourceEstimationAdditionalParametersView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sourceEstimationAdditionalParametersController(sourceEstimationAdditionalParametersListener):
    def __init__(self):
        """
        Controller for retrieving the additional information for the computation of the source estimation on the dataset.
        Create a new window for specifying some parameters.
        """
        self.main_listener = None
        self.source_estimation_additional_parameters_view = sourceEstimationAdditionalParametersView()
        self.source_estimation_additional_parameters_view.set_listener(self)

        self.source_estimation_additional_parameters_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.source_estimation_additional_parameters_view.close()

    def confirm_button_clicked(self, export_path):
        """
        Close the window and send the information to the source estimation controller.
        :param export_path: Path where the source estimation data will be stored.
        :type export_path: str
        """
        self.main_listener.additional_parameters_information(export_path)
        self.source_estimation_additional_parameters_view.close()

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the main listener so that the controller is able to communicate with the source estimation controller.
        :param listener: main listener
        :type listener: sourceEstimationController
        """
        self.main_listener = listener
