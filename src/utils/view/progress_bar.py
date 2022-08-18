#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Progress bar
"""

from PyQt5.QtWidgets import QProgressBar

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class ProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)

    def stop(self):
        self.setMaximum(1)
        self.setValue(1)
