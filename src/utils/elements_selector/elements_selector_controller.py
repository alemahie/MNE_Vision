#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Multiple selector controller
"""

from utils.elements_selector.elements_selector_view import multipleSelectorView
from utils.elements_selector.elements_selector_listener import multipleSelectorListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class multipleSelectorController(multipleSelectorListener):
    def __init__(self, all_elements_names, title, box_checked=True, unique_box=False):
        self.main_listener = None
        self.multiple_selector_view = multipleSelectorView(all_elements_names, title, box_checked, unique_box)
        self.multiple_selector_view.set_listener(self)

        self.multiple_selector_view.show()

    def cancel_button_clicked(self):
        self.multiple_selector_view.close()

    def confirm_button_clicked(self, elements_selected):
        self.main_listener.get_elements_selected(elements_selected)
        self.multiple_selector_view.close()

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
