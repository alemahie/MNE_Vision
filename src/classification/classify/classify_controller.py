#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Channel location controller
"""

from classification.classify.classify_listener import classifyListener
from classification.classify.classify_view import classifyView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class classifyController(classifyListener):
    def __init__(self):
        """
        Controller for computing the classification on the dataset.
        Create a new window for specifying some parameters.
        """
        self.main_listener = None
        self.classify_view = classifyView()
        self.classify_view.set_listener(self)

        self.classify_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.classify_view.close()

    def confirm_button_clicked(self, pipeline_selected, feature_selection, hyper_tuning, cross_val_number):
        """
        Close the window and send the information to the main controller.
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
        self.classify_view.close()
        self.main_listener.classify_information(pipeline_selected, feature_selection, hyper_tuning, cross_val_number)

    def plot_results(self, classifier):
        """
        Plot the classification results.
        :param classifier: The classifier that did the classification.
        :type classifier: ApplePyClassifier
        """
        self.classify_view.plot_results(classifier)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :param elements_selected: Elements selected in the multiple elements' selector.
        :type elements_selected: list of str
        """
        self.classify_view.set_pipeline_selected(elements_selected)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the main listener so that the controller is able to communicate with the main controller.
        :param listener: main listener
        :type listener: mainController
        """
        self.main_listener = listener
