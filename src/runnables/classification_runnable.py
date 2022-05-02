#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classification runnable
"""

from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

from lib.applePy.classifier import ApplePyClassifier

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class classifyWorkerSignals(QObject):
    finished = pyqtSignal()


class classifyRunnable(QRunnable):
    def __init__(self, file_data, directory_path, pipeline_selected, feature_selection, hyper_tuning, cross_val_number):
        super().__init__()
        self.signals = classifyWorkerSignals()

        self.classifier = None
        self.file_data = file_data
        self.directory_path = directory_path
        self.pipeline_selected = pipeline_selected
        self.feature_selection = feature_selection
        self.hyper_tuning = hyper_tuning
        self.cross_val_number = cross_val_number

    def run(self):
        self.classifier = ApplePyClassifier(used_pipelines=self.pipeline_selected)
        self.classifier.classify(self.file_data, dataset_path=self.directory_path, classify_test=False,
                                 independent_features_selection=self.feature_selection, tune_hypers=self.hyper_tuning,
                                 use_groups=False, cv_value=self.cross_val_number)
        self.signals.finished.emit()

    def get_classifier(self):
        return self.classifier
