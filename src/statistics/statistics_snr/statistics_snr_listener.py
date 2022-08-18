#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics SNR listener
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class statisticsSnrListener(ABC):
    """
    Listener doing the connection between the controller and the view for computing the statistics on SNR on the dataset.
    It retrieves the information from the view to send it to the controller.
    """

    @abstractmethod
    def cancel_button_clicked(self):
        pass

    @abstractmethod
    def confirm_button_clicked(self, snr_methods, source_method, read, write, picks, stats_first_variable, stats_second_variable):
        pass

    @abstractmethod
    def get_elements_selected(self, elements_selected, element_type):
        pass
