#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classify view
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QGridLayout, QCheckBox, \
    QDoubleSpinBox, QSpinBox

from utils.elements_selector.elements_selector_controller import multipleSelectorController

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class classifyView(QWidget):
    def __init__(self, number_of_channels):
        """
        Window displaying the parameters for performing the classification.
        :param number_of_channels: The number of channels in the dataset.
        :type number_of_channels: int
        """
        super().__init__()
        self.classify_listener = None
        self.number_of_channels = number_of_channels
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

        self.number_of_features = QSpinBox()
        self.number_of_features.setRange(1, self.number_of_channels)
        if self.number_of_channels >= 20:
            self.number_of_features.setValue(20)
        else:
            self.number_of_features.setValue(self.number_of_channels)

        self.hyper_tuning = QCheckBox()
        self.cross_validation_number = QDoubleSpinBox()
        self.cross_validation_number.setValue(5)
        self.cross_validation_number.setMinimum(1)
        self.cross_validation_number.setDecimals(0)

        self.grid_layout.addWidget(QLabel("Feature selection : "), 0, 0)
        self.grid_layout.addWidget(self.pipeline_selection_button, 0, 1)
        self.grid_layout.addWidget(QLabel("Feature selection : "), 1, 0)
        self.grid_layout.addWidget(self.feature_selection, 1, 1)
        self.grid_layout.addWidget(QLabel("Number of features to select : "), 2, 0)
        self.grid_layout.addWidget(self.number_of_features, 2, 1)
        self.grid_layout.addWidget(QLabel("Hyper-parameters tuning : "), 3, 0)
        self.grid_layout.addWidget(self.hyper_tuning, 3, 1)
        self.grid_layout.addWidget(QLabel("Cross-validation k-fold : "), 4, 0)
        self.grid_layout.addWidget(self.cross_validation_number, 4, 1)
        self.grid_widget.setLayout(self.grid_layout)

        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_classification_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_classification_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.grid_widget)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    """
    Plot
    """
    @staticmethod
    def plot_results(classifier):
        """
        Plot the classification results.
        :param classifier: The classifier that did the classification.
        :type classifier: ApplePyClassifier
        """
        classifier.show_results(4)

    """
    Triggers
    """
    def cancel_classification_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.classify_listener.cancel_button_clicked()

    def confirm_classification_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        feature_selection = self.feature_selection.isChecked()
        number_of_channels_to_select = self.number_of_features.value()
        hyper_tuning = self.hyper_tuning.isChecked()
        cross_val_number = int(self.cross_validation_number.value())
        self.classify_listener.confirm_button_clicked(self.pipeline_selected, feature_selection, number_of_channels_to_select,
                                                      hyper_tuning, cross_val_number)

    def pipeline_selection_trigger(self):
        """
        Open the multiple selector window.
        The user can select a multiple pipelines used for the classification.
        """
        title = "Select the pipelines used for the classification :"
        all_pipelines = ['XdawnCov', 'Xdawn', 'CSP', 'CSP2', 'cov', 'HankelCov', 'CSSP', 'PSD', 'MDM', 'FgMDM']
        # 'XdawnCovTSLR', 'Cosp'
        self.pipeline_selector_controller = multipleSelectorController(all_pipelines, title, box_checked=True)
        self.pipeline_selector_controller.set_listener(self.classify_listener)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: classifyController
        """
        self.classify_listener = listener

    def set_pipeline_selected(self, pipeline):
        """
        Set the pipeliens selected in the multiple selector window.
        :param pipeline: Pipelines selected
        :type pipeline: list of str
        """
        self.pipeline_selected = pipeline
