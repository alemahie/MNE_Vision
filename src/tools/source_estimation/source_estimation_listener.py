#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source estimation listener
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sourceEstimationListener(ABC):
    """
    Listener doing the connection between the controller and the view for computing the source estimation on the dataset.
    It retrieves the information from the view to send it to the controller.
    """

    @abstractmethod
    def cancel_button_clicked(self):
        pass

    @abstractmethod
    def confirm_button_clicked(self, source_estimation_method, save_data, load_data, epochs_method, trials_selected, tmin,
                               tmax, n_jobs):
        pass

    @abstractmethod
    def additional_parameters_clicked(self):
        pass

    @abstractmethod
    def additional_parameters_information(self, export_path):
        pass

    @abstractmethod
    def get_elements_selected(self, elements_selected, element_type):
        pass
