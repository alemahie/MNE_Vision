#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classify view
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QGridLayout, QCheckBox, \
    QDoubleSpinBox

from utils.elements_selector.elements_selector_controller import multipleSelectorController

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class classifyView(QWidget):
    def __init__(self):
        super().__init__()
        self.classify_listener = None
        self.pipeline_selector_controller = None
        self.pipeline_selected = None

        self.setWindowTitle("Classification")

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout()

        self.pipeline_selection_button = QPushButton("&Pipelines ...", self)
        self.pipeline_selection_button.clicked.connect(self.pipeline_selection_trigger)
        self.feature_selection = QCheckBox()
        self.hyper_tuning = QCheckBox()
        self.cross_validation_number = QDoubleSpinBox()
        self.cross_validation_number.setValue(5)
        self.cross_validation_number.setMinimum(1)
        self.cross_validation_number.setDecimals(0)

        self.grid_layout.addWidget(QLabel("Feature selection : "), 0, 0)
        self.grid_layout.addWidget(self.pipeline_selection_button, 0, 1)
        self.grid_layout.addWidget(QLabel("Feature selection : "), 1, 0)
        self.grid_layout.addWidget(self.feature_selection, 1, 1)
        self.grid_layout.addWidget(QLabel("Hyper-parameters tuning : "), 2, 0)
        self.grid_layout.addWidget(self.hyper_tuning, 2, 1)
        self.grid_layout.addWidget(QLabel("Cross-validation k-fold : "), 3, 0)
        self.grid_layout.addWidget(self.cross_validation_number, 3, 1)
        self.grid_widget.setLayout(self.grid_layout)

        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_channel_location_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_channel_location_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.grid_widget)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    """
    Plot
    """
    def plot_results(self, classifier):
        classifier.show_results(4)

    """
    Triggers
    """
    def cancel_channel_location_trigger(self):
        self.classify_listener.cancel_button_clicked()

    def confirm_channel_location_trigger(self):
        feature_selection = self.feature_selection.isChecked()
        hyper_tuning = self.hyper_tuning.isChecked()
        cross_val_number = int(self.cross_validation_number.value())
        self.classify_listener.confirm_button_clicked(self.pipeline_selected, feature_selection, hyper_tuning,
                                                      cross_val_number)

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
