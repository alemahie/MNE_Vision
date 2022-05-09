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
    @abstractmethod
    def cancel_button_clicked(self):
        pass

    @abstractmethod
    def confirm_button_clicked(self, connectivity_method, spectrum_estimation_method, source_estimation_method, save_data,
                               load_data, n_jobs):
        pass
