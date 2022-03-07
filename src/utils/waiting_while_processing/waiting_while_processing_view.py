#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Waiting while processing view
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from utils.progress_bar import ProgressBar

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class waitingWhileProcessingView(QWidget):
    def __init__(self, processing_title):
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
        self.progress_bar.stop()
        self.continue_button.setEnabled(True)
        self.processing_title.setText(processing_title_finished)
        self.setWindowTitle("Process finished.")

    """
    Triggers
    """
    def continue_button_trigger(self):
        self.waiting_while_processing_listener.continue_button_clicked()

    """
    Setters
    """
    def set_listener(self, listener):
        self.waiting_while_processing_listener = listener
