#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Load Data Info Listener
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class loadDataInfoListener(ABC):
    """
    Listener doing the connection between the controller and the view for loading the additional data information.
    It retrieves the information from the view to send it to the controller.
    """

    @abstractmethod
    def cancel_button_clicked(self):
        pass

    @abstractmethod
    def confirm_button_clicked(self, montage, channels_selected, tmin, tmax, dataset_name):
        pass

    @abstractmethod
    def get_elements_selected(self, elements_selected):
        pass
