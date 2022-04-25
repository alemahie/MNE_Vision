#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classification runnable
"""

from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

from lib.applePy.classifier import ApplePyClassifier

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class classifyWorkerSignals(QObject):
    finished = pyqtSignal()


class classifyRunnable(QRunnable):
    def __init__(self, pipeline_selected, file_data, directory_path):
        super().__init__()
        self.signals = classifyWorkerSignals()

        self.classifier = None
        self.pipeline_selected = pipeline_selected
        self.file_data = file_data
        self.directory_path = directory_path

    def run(self):
        self.classifier = ApplePyClassifier(used_pipelines=self.pipeline_selected)
        self.classifier.classify(self.file_data, dataset_path=self.directory_path, names=[0, 1], classify_test=False, tune_hypers=False, use_groups=False,
                                 cv_value=2)
        self.signals.finished.emit()

    def get_classifier(self):
        return self.classifier
