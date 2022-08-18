#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Re-referencing controller
"""

from tools.re_referencing.re_referencing_view import reReferencingView
from tools.re_referencing.re_referencing_listener import reReferencingListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class reReferencingController(reReferencingListener):
    def __init__(self, reference, all_channels_names):
        """
        Controller for computing the re-referencing on the dataset.
        Create a new window for specifying some parameters.
        :param reference: Current reference
        :type reference: str/list of str
        :param all_channels_names: All the channels names
        :type all_channels_names: list of str
        """
        self.main_listener = None
        self.re_referencing_view = reReferencingView(reference, all_channels_names)
        self.re_referencing_view.set_listener(self)

        self.re_referencing_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.re_referencing_view.close()

    def confirm_button_clicked(self, references, save_data, load_data, n_jobs):
        """
        Close the window and send the information to the main controller.
        :param references: References from which the data will be re-referenced. Can be a single or multiple channels;
        Can be an average of all channels; Can be a "point to infinity".
        :type references: list of str; str
        :param save_data: Boolean telling if the data computed must be saved into files.
        :type save_data: bool
        :param load_data: Boolean telling if the data used for the computation can be read from computer files.
        :type load_data: bool
        :param n_jobs: Number of parallel processes used to compute the re-referencing
        :type n_jobs: int
        """
        self.main_listener.re_referencing_information(references, save_data, load_data, n_jobs)
        self.re_referencing_view.close()

    def get_elements_selected(self, elements_selected):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :param elements_selected: Elements selected in the multiple elements' selector.
        :type elements_selected: list of str
        """
        self.re_referencing_view.set_channels_selected(elements_selected)

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
