#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Channel location controller
"""

from classification.classify.classify_listener import classifyListener
from classification.classify.classify_view import classifyView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class classifyController(classifyListener):
    def __init__(self):
        self.main_listener = None
        self.classify_view = classifyView()
        self.classify_view.set_listener(self)

        self.classify_view.show()

    def cancel_button_clicked(self):
        self.classify_view.close()

    def confirm_button_clicked(self, pipeline_selected):
        self.classify_view.close()
        self.main_listener.classify_information(pipeline_selected)

    def plot_results(self, classifier):
        self.classify_view.plot_results(classifier)

    """
    Getters
    """
    def get_elements_selected(self, elements_selected):
        self.classify_view.set_pipeline_selected(elements_selected)

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
