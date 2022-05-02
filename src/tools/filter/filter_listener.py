#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Filter listener
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class filterListener(ABC):
    @abstractmethod
    def cancel_button_clicked(self):
        pass

    @abstractmethod
    def confirm_button_clicked(self, low_frequency, high_frequency, channels_selected):
        pass

    @abstractmethod
    def get_elements_selected(self, elements_selected):
        pass
