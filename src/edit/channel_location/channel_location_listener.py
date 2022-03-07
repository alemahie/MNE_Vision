#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Channel location listener
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class channelLocationListener(ABC):
    @abstractmethod
    def cancel_button_clicked(self):
        pass

    @abstractmethod
    def confirm_button_clicked(self):
        pass

    @abstractmethod
    def previous_button_clicked(self):
        pass

    @abstractmethod
    def next_button_clicked(self):
        pass

    @abstractmethod
    def editing_finished_clicked(self, channel_number):
        pass
