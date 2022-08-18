#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Separator
"""

from PyQt5.QtWidgets import QFrame

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


def create_layout_separator():
    h_line = QFrame()
    h_line.setFrameShape(QFrame.Shape.HLine)
    h_line.setFrameShadow(QFrame.Shadow.Sunken)
    return h_line
