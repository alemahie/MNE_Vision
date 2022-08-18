#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Splash Screen
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from utils.file_path_search import get_image_folder

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class splashScreen(QWidget):
    def __init__(self):
        """
        Window displaying the splash screen at the launch of the software.
        Displays the "MNE Vision" logo.
        """
        super().__init__()
        self.setWindowTitle('MNE VISION')
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        self.logo = QLabel("hello", self)
        self.logo.setPixmap(QPixmap(get_image_folder()+"mne_vision_logo.png"))
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vertical_layout.addWidget(self.logo)
        self.center()

    def center(self):
        """
        Move the window to the center of the screen.
        """
        coord = self.screen().availableGeometry().getCoords()
        x = coord[2]//2 - 545   # 545 : Half width of logo
        if x < 0:
            x = 0
        y = coord[3]//2 - 63    # 63 : Half height of logo
        if y < 0:
            y = 0
        self.move(x, y)
