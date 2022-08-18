#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source Space Connectivity Listener
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sourceSpaceConnectivityListener(ABC):
    """
    Listener doing the connection between the controller and the view for computing the source space connectivity on the
    dataset.
    It retrieves the information from the view to send it to the controller.
    """

    @abstractmethod
    def cancel_button_clicked(self):
        pass

    @abstractmethod
    def confirm_button_clicked(self, connectivity_method, spectrum_estimation_method, source_estimation_method, save_data,
                               load_data, n_jobs, psi, fmin, fmax):
        pass

    @abstractmethod
    def additional_parameters_clicked(self):
        pass

    @abstractmethod
    def additional_parameters_information(self, export_path):
        pass
