#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source Estimation Controller
"""

from tools.source_estimation.source_estimation_view import sourceEstimationView
from tools.source_estimation.source_estimation_listener import sourceEstimationListener

from utils.data_exportation.data_exportation_controller import dataExportationController
from utils.view.error_window import errorWindow

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sourceEstimationController(sourceEstimationListener):
    def __init__(self, number_of_epochs, event_values, event_ids, tmin, tmax, title=None):
        """
        Controller for computing the source estimation on the dataset.
        Create a new window for specifying some parameters.
        :param number_of_epochs: Number of epochs in the dataset.
        :type number_of_epochs: int
        :param event_values: Event_id associated to each epoch/trial.
        :type event_values: list of, list of int
        :param event_ids: Name of the events associated to their id.
        :type event_ids: dict
        :param tmin: Start time of the epoch or raw file
        :type tmin: float
        :param tmax: End time of the epoch or raw file
        :type tmax: float
        :param title: Title of window
        :type title: str
        """
        self.main_listener = None
        self.source_estimation_view = sourceEstimationView(number_of_epochs, event_values, event_ids, tmin, tmax, title)
        self.source_estimation_view.set_listener(self)

        self.export_data_controller = None
        self.export_path = None

        self.source_estimation_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.source_estimation_view.close()

    def confirm_button_clicked(self, source_estimation_method, save_data, load_data, epochs_method, trials_selected, tmin,
                               tmax,  n_jobs):
        """
        Close the window and send the information to the main controller.
        :param source_estimation_method: The method used to compute the source estimation
        :type source_estimation_method: str
        :param save_data: Boolean telling if the data computed must be saved into files.
        :type save_data: bool
        :param load_data: Boolean telling if the data used for the computation can be read from computer files.
        :type load_data: bool
        :param epochs_method: On what data the source estimation will be computed. Can be three values :
        - "single trial" : Compute the source estimation on a single trial that is precised.
        - "evoked" : Compute the source estimation on the average of all the signals.
        - "averaged" : Compute the source estimation on every trial, and then compute the average of them.
        :type: str
        :param trials_selected: The indexes of the trials selected for the computation
        :type trials_selected: list of int
        :param tmin: Start time of the epoch or raw file
        :type tmin: float
        :param tmax: End time of the epoch or raw file
        :type tmax: float
        :param n_jobs: Number of processes used to compute the source estimation
        :type n_jobs: int
        """
        self.source_estimation_view.close()
        self.main_listener.source_estimation_information(source_estimation_method, save_data, load_data, epochs_method,
                                                         trials_selected, tmin, tmax,  n_jobs, self.export_path)

    def additional_parameters_clicked(self):
        """
        Create a new window for specifying some additional parameters for the computation of the source estimation.
        """
        self.export_data_controller = dataExportationController()
        self.export_data_controller.set_listener(self)

    def additional_parameters_information(self, export_path):
        """
        Retrieve the exportation path for the source estimation data computed.
        :param export_path: Path where the source estimation data will be stored.
        :type export_path: str
        """
        self.export_path = export_path

    def plot_source_estimation(self, source_estimation_data):
        """
        Send the information to the view for plotting the source estimation.
        :param source_estimation_data: The source estimation's data.
        :type source_estimation_data: MNE.SourceEstimation
        """
        self.source_estimation_view.plot_source_estimation(source_estimation_data)

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
            self.source_estimation_view.set_trials_selected(elements_selected, element_type)

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
