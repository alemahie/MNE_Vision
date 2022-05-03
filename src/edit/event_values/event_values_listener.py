#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Event Values Listener
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class eventValuesListener(ABC):
    @abstractmethod
    def cancel_button_clicked(self):
        pass

    @abstractmethod
    def confirm_button_clicked(self, event_name, latency):
        pass

    @abstractmethod
    def previous_button_clicked(self, event_name, latency):
        pass

    @abstractmethod
    def next_button_clicked(self, event_name, latency):
        pass

    @abstractmethod
    def delete_button_clicked(self):
        pass

    @abstractmethod
    def insert_button_clicked(self, event_name, latency):
        pass

    @abstractmethod
    def editing_finished_clicked(self, event_number):
        pass
