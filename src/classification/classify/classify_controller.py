#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classify Controller
"""

from classification.classify.classify_listener import classifyListener
from classification.classify.classify_view import classifyView

from utils.view.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class classifyController(classifyListener):
    def __init__(self, number_of_channels, event_values, event_ids):
        """
        Controller for computing the classification on the dataset.
        Create a new window for specifying some parameters.
        :param number_of_channels: The number of channels in the dataset.
        :type number_of_channels: int
        :param event_values: Event_id associated to each epoch/trial.
        :type event_values: list of, list of int
        :param event_ids: Name of the events associated to their id.
        :type event_ids: dict
        """
        self.main_listener = None
        self.classify_view = classifyView(number_of_channels, event_values, event_ids)
        self.classify_view.set_listener(self)

        self.classify_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.classify_view.close()

    def confirm_button_clicked(self, pipeline_selected, feature_selection, number_of_channels_to_select, hyper_tuning,
                               cross_val_number, trials_selected):
        """
        Close the window and send the information to the main controller.
        :param pipeline_selected: The pipeline(s) used for the classification of the dataset.
        :type pipeline_selected: list of str
        :param feature_selection: Boolean telling if the computation of some feature selection techniques must be performed
        on the dataset.
        :type feature_selection: boolean
        :param number_of_channels_to_select: Number of channels to select for the feature selection.
        :type number_of_channels_to_select: int
        :param hyper_tuning: Boolean telling if the computation of the tuning of the hyper-parameters of the pipelines must
        be performed on the dataset.
        :type hyper_tuning: boolean
        :param cross_val_number: Number of cross-validation fold used by the pipelines on the dataset.
        :type cross_val_number: int
        :param trials_selected: The indexes of the trials selected for the computation
        :type trials_selected: list of int
        """
        self.classify_view.close()
        self.main_listener.classify_information(pipeline_selected, feature_selection, number_of_channels_to_select, hyper_tuning,
                                                cross_val_number, trials_selected)

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
    def get_elements_selected(self, elements_selected, element_type):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :param elements_selected: Elements selected in the multiple elements' selector.
        :type elements_selected: list of str
        :param element_type: Type of the element selected, used in case multiple element selector windows can be open in
        a window. Can thus distinguish the returned elements.
        :type element_type: str
        """
        if len(elements_selected) == 0:
            error_message = "Please select at least one element in the list. \n The source estimation can not be " \
                            "computed on 0 trials"
            error_window = errorWindow(error_message)
            error_window.show()
        else:
            self.classify_view.check_element_type(elements_selected, element_type)

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
