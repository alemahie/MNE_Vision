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
    @abstractmethod
    def cancel_button_clicked(self):
        pass

    @abstractmethod
    def confirm_button_clicked(self, source_estimation_method, save_data, load_data, n_jobs):
        pass
