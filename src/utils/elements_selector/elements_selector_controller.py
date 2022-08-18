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
    def __init__(self, all_elements_names, title, box_checked=True, unique_box=False, element_type=None):
        """
        Controller for the multiple selector.
        Create a new window where we can select some elements.
        :param all_elements_names: All the elements' names
        :type all_elements_names: list of str
        :param title: Title for the multiple selector window.
        :type title: str
        :param box_checked: All the elements are selected by default.
        :type box_checked: bool
        :param unique_box: Can only check a single element from all the elements.
        :type unique_box: bool
        :param element_type: Type of the element selected, used in case multiple element selector windows can be open in
        a window. Can thus distinguish the returned elements.
        :type element_type: str
        """
        self.main_listener = None
        self.multiple_selector_view = multipleSelectorView(all_elements_names, title, box_checked, unique_box)
        self.multiple_selector_view.set_listener(self)

        self.element_type = element_type

        self.multiple_selector_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.multiple_selector_view.close()

    def confirm_button_clicked(self, elements_selected):
        """
        Close the window and send the information to the controller that opened the multiple elements window.
        :param elements_selected: All the elements selected.
        :type elements_selected: list of str
        """
        if self.element_type is None:
            self.main_listener.get_elements_selected(elements_selected)
        else:
            self.main_listener.get_elements_selected(elements_selected, self.element_type)
        self.multiple_selector_view.close()

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener so that the controller is able to communicate with the controller that opened the multiple
        elements window.
        :param listener: Listener linked to the view that opened the multiple elements window.
        :type listener: listener
        """
        self.main_listener = listener
