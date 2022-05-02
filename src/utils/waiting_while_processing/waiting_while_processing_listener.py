#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Waiting while processing listener
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class waitingWhileProcessingListener(ABC):
    @abstractmethod
    def continue_button_clicked(self):
        pass
