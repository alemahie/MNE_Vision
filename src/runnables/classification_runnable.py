#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classification runnable
"""

from copy import deepcopy

from PyQt5.QtCore import QRunnable, pyqtSignal, QObject

from classification.applePy.classifier import ApplePyClassifier

from utils.view.error_window import errorWindow


__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class classifyWorkerSignals(QObject):
    """
    Contain the signals used by the classification runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class classifyRunnable(QRunnable):
    def __init__(self, file_data, directory_path, pipeline_selected, feature_selection, number_of_channels_to_select,
                 hyper_tuning, cross_val_number, trials_selected):
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
        :type feature_selection: bool
        :param number_of_channels_to_select: Number of channels to select for the feature selection.
        :type number_of_channels_to_select: int
        :param hyper_tuning: Boolean telling if the computation of the tuning of the hyper-parameters of the pipelines must
        be performed on the dataset.
        :type hyper_tuning: bool
        :param cross_val_number: Number of cross-validation fold used by the pipelines on the dataset.
        :type cross_val_number: int
        :param trials_selected: The indexes of the trials selected for the computation
        :type trials_selected: list of int
        """
        super().__init__()
        self.signals = classifyWorkerSignals()

        self.classifier = None
        self.file_data = deepcopy(file_data)
        self.directory_path = directory_path
        self.pipeline_selected = pipeline_selected
        self.feature_selection = feature_selection
        self.number_of_channels_to_select = number_of_channels_to_select
        self.hyper_tuning = hyper_tuning
        self.cross_val_number = cross_val_number
        self.trials_selected = trials_selected

    def run(self):
        """
        Create the classifier and launch the computation of the classification.
        Notifies the main model that the computation is finished.
        """
        try:
            self.transform_file_data_with_trials_selected()
            self.classifier = ApplePyClassifier(used_pipelines=self.pipeline_selected)
            self.classifier.classify(self.file_data, dataset_path=self.directory_path, classify_test=False, test_dataset_size=5,
                                     independent_features_selection=self.feature_selection, channels_to_select=self.number_of_channels_to_select,
                                     tune_hypers=self.hyper_tuning, use_groups=False, cv_value=self.cross_val_number)
            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error as occurred during the computation of the classification."
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()

    def transform_file_data_with_trials_selected(self):
        """
        Create a mask to know which trial to keep and which one to remove for the computation.
        Apply this mask on the data to keep only the trials/epochs selected by the user.
        """
        mask = [True for _ in range(len(self.file_data.events))]
        for i in self.trials_selected:
            mask[i] = False
        self.file_data.drop(mask)

    def get_classifier(self):
        """
        Get the classifier/pipelines on which the classification is performed.
        :return: The classifiers
        :rtype: ApplePyClassifier
        """
        return self.classifier
