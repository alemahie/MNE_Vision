#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main file launching the project.
"""

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"

import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen

from utils.file_path_search import get_image_folder
from utils.view.stylesheet import get_stylesheet

if __name__ == "__main__":
    """
    First create the application and create the splash screen.
    """
    try:
        app = QApplication(sys.argv)
        app.setStyleSheet(get_stylesheet())

        # pixmap = QPixmap(get_image_folder() + "mne_vision_logo.png")
        # splash_screen = QSplashScreen(pixmap)
        # splash_screen.show()

        app.processEvents()

        from main_controller import mainController

        # splash_screen.close()
        app.processEvents()

        screen_size = app.primaryScreen().size()
        main_controller = mainController(screen_size)

        # main_window = main_controller.get_main_view()
        # splash_screen.finish(main_window)

        main_controller.show()

        sys.exit(app.exec())
    except Exception as e:
        print(e)
        print(type(e))
