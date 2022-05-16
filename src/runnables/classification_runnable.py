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


# Classify
class classifyWorkerSignals(QObject):
    """
    Contain the signals used by the classification runnable.
    """
    finished = pyqtSignal()


class classifyRunnable(QRunnable):
    def __init__(self, file_data, directory_path, pipeline_selected, feature_selection, hyper_tuning, cross_val_number):
        """
        Runnable for the computation of the classification of the dataset.
        Create the pipelines were the classification will be performed and launch the classification depending on the
        parameters.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param directory_path: Path to the directory of the file
        :type directory_path:
        :param pipeline_selected: The pipeline(s) used for the classification of the dataset.
        :type pipeline_selected: list of str
        :param feature_selection: Boolean telling if the computation of some feature selection techniques must be performed
        on the dataset.
        :type feature_selection: boolean
        :param hyper_tuning: Boolean telling if the computation of the tuning of the hyper-parameters of the pipelines must
        be performed on the dataset.
        :type hyper_tuning: boolean
        :param cross_val_number: Number of cross-validation fold used by the pipelines on the dataset.
        :type cross_val_number: int
        """
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
        """
        Create the classifier and launch the computation of the classification.
        Notifies the main model that the computation is finished.
        """
        self.classifier = ApplePyClassifier(used_pipelines=self.pipeline_selected)
        self.classifier.classify(self.file_data, dataset_path=self.directory_path, classify_test=False,
                                 independent_features_selection=self.feature_selection, tune_hypers=self.hyper_tuning,
                                 use_groups=False, cv_value=self.cross_val_number)
        self.signals.finished.emit()

    def get_classifier(self):
        """
        Get the classifier/pipelines on which the classification is performed.
        :return: The classifiers
        :rtype: ApplePyClassifier
        """
        return self.classifier
