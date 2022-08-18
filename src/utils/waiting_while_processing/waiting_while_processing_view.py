#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Waiting while processing view
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from utils.view.progress_bar import ProgressBar

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class waitingWhileProcessingView(QWidget):
    def __init__(self, processing_title):
        """
        Window displaying a waiting screen and a progress bar that runs while the computation is done.
        :param processing_title: The title displayed on the window.
        :type processing_title: str
        """
        super().__init__()
        self.waiting_while_processing_listener = None

        self.setWindowTitle("Process running.")
        self.resize(300, 100)
        self.vbox = QVBoxLayout()

        self.processing_title = QLabel(processing_title)
        self.progress_bar = ProgressBar(self, minimum=0, maximum=0, textVisible=False, objectName="BlueProgressBar")
        self.continue_button = QPushButton("&Continue")
        self.continue_button.setEnabled(False)
        self.continue_button.clicked.connect(self.continue_button_trigger)

        self.vbox.addWidget(self.processing_title)
        self.vbox.addWidget(self.progress_bar)
        self.vbox.addWidget(self.continue_button)

        self.setLayout(self.vbox)

    def stop_progress_bar(self, processing_title_finished):
        """
        Stop the progress bar of the waiting window.
        :param processing_title_finished: The title displayed on the window.
        :type processing_title_finished: str
        """
        self.progress_bar.stop()
        self.continue_button.setEnabled(True)
        self.processing_title.setText(processing_title_finished)
        self.setWindowTitle("Process finished.")

    """
    Triggers
    """
    def continue_button_trigger(self):
        """
        Close the window.
        """
        self.waiting_while_processing_listener.continue_button_clicked()

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: controller
        """
        self.waiting_while_processing_listener = listener
