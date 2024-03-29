#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Envelope Correlation Listener
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class envelopeCorrelationListener(ABC):
    """
    Listener doing the connection between the controller and the view for computing the envelope correlation on the dataset.
    It retrieves the information from the view to send it to the controller.
    """

    @abstractmethod
    def cancel_button_clicked(self):
        pass

    @abstractmethod
    def confirm_button_clicked(self, psi, fmin, fmax, connectivity_method, n_jobs):
        pass

    @abstractmethod
    def additional_parameters_clicked(self):
        pass

    @abstractmethod
    def additional_parameters_information(self, export_path):
        pass
