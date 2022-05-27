#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main file launching the project.
"""

import sys

from PyQt5.QtWidgets import QApplication

from main_controller import mainController

from utils.stylesheet import get_stylesheet

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(get_stylesheet())

    # splash_screen = splashScreen()
    # splash_screen.show()
    # app.processEvents()     # Allow the splash screen to be displayed while loading the main window

    screen_size = app.primaryScreen().size()
    main_controller = mainController(screen_size)
    sys.exit(app.exec())
