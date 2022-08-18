#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Waiting while processing controller
"""

from utils.waiting_while_processing.waiting_while_processing_view import waitingWhileProcessingView
from utils.waiting_while_processing.waiting_while_processing_listener import waitingWhileProcessingListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class waitingWhileProcessingController(waitingWhileProcessingListener):
    def __init__(self, processing_title, finish_method=None):
        """
        Controller for the waiting window.
        Create a new window for the waiting time while the computation is done.
        :param processing_title: The title displayed on the window.
        :type processing_title: str
        :param finish_method: The method to call when the computation is finished.
        :type finish_method: function
        """
        self.main_listener = None

        self.finish_method = finish_method
        self.error = False

        self.waiting_while_processing_view = waitingWhileProcessingView(processing_title)
        self.waiting_while_processing_view.set_listener(self)

        self.waiting_while_processing_view.show()

    def stop_progress_bar(self, processing_title_finished, error=False):
        """
        Stop the progress bar of the waiting window.
        :param processing_title_finished: The title displayed on the window.
        :type processing_title_finished: str
        :param error: Set to True if an error occurred, avoid to call the finish method.
        :type error: bool
        """
        self.error = error
        self.waiting_while_processing_view.stop_progress_bar(processing_title_finished)

    def continue_button_clicked(self):
        """
        Close the window and send the information to the main controller if no error occurred and a method is provided.
        """
        self.waiting_while_processing_view.close()
        if not self.error and self.finish_method is not None:
            try:
                self.finish_method()
            except Exception as e:
                print(e)
                print(type(e))

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
