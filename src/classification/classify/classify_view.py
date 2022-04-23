#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classify view
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from utils.elements_selector.elements_selector_controller import multipleSelectorController

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class classifyView(QWidget):
    def __init__(self):
        super().__init__()
        self.classify_listener = None

        self.pipeline_selector_controller = None
        self.pipeline_selected = None

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        self.pipeline_selection_widget = QWidget()
        self.pipeline_selection_layout = QHBoxLayout()
        self.pipeline_selection_button = QPushButton("&Pipelines ...", self)
        self.pipeline_selection_button.clicked.connect(self.pipeline_selection_trigger)
        self.pipeline_selection_layout.addWidget(QLabel("Pipelines : "))
        self.pipeline_selection_layout.addWidget(self.pipeline_selection_button)
        self.pipeline_selection_widget.setLayout(self.pipeline_selection_layout)

        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_channel_location_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_channel_location_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.pipeline_selection_widget)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    """
    Triggers
    """
    def cancel_channel_location_trigger(self):
        self.classify_listener.cancel_button_clicked()

    def confirm_channel_location_trigger(self):
        self.classify_listener.confirm_button_clicked(self.pipeline_selected)

    def pipeline_selection_trigger(self):
        title = "Select the pipelines used for the classification :"
        all_pipelines = ['XdawnCovTSLR', 'XdawnCov', 'Xdawn', 'CSP', 'CSP2', 'cov', 'Cosp', 'HankelCov', 'CSSP', 'PSD',
                         'MDM', 'FgMDM']
        self.pipeline_selector_controller = multipleSelectorController(all_pipelines, title, box_checked=True)
        self.pipeline_selector_controller.set_listener(self.classify_listener)

    """
    Setters
    """
    def set_listener(self, listener):
        self.classify_listener = listener

    def set_pipeline_selected(self, pipeline):
        self.pipeline_selected = pipeline
