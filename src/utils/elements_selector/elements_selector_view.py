#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Multiple selector View
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QLabel, QCheckBox, QButtonGroup

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class multipleSelectorView(QWidget):
    def __init__(self, all_elements_names, title, box_checked, unique_box):
        """
        Window displaying the multiple elements from which we can select some elements.
        :param all_elements_names: All the elements' names
        :type all_elements_names: list of str
        :param title: Title for the multiple selector window.
        :type title: str
        :param box_checked: All the elements are selected by default.
        :type box_checked: bool
        :param unique_box: Can only check a single element from all the elements.
        :type unique_box: bool
        """
        super().__init__()
        self.multiple_selector_listener = None
        self.unique_box = unique_box

        self.select_unselect_widget = None
        self.select_unselect_hbox_layout = None
        self.select_all_elements = None
        self.unselect_all_elements = None

        self.setWindowTitle("Selection")

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        # Elements
        self.elements_widget = QWidget()
        self.elements_vbox_layout = QVBoxLayout()

        self.elements_button = QButtonGroup()
        if not unique_box:
            self.create_select_unselect_buttons()
        self.create_check_boxes(all_elements_names, box_checked, unique_box)
        self.elements_widget.setLayout(self.elements_vbox_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.elements_widget)

        # Cancel & Confirm buttons
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(QLabel(title))
        self.vertical_layout.addWidget(self.scroll_area)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    def create_select_unselect_buttons(self):
        self.select_unselect_widget = QWidget()
        self.select_unselect_hbox_layout = QHBoxLayout()
        self.select_all_elements = QPushButton("&Select All", self)
        self.select_all_elements.clicked.connect(self.select_all_elements_trigger)
        self.unselect_all_elements = QPushButton("&Unselect All", self)
        self.unselect_all_elements.clicked.connect(self.unselect_all_elements_trigger)
        self.select_unselect_hbox_layout.addWidget(self.select_all_elements)
        self.select_unselect_hbox_layout.addWidget(self.unselect_all_elements)
        self.select_unselect_widget.setLayout(self.select_unselect_hbox_layout)
        self.elements_vbox_layout.addWidget(self.select_unselect_widget)

    def create_check_boxes(self, all_elements_names, box_checked, unique_box):
        unique_box_not_checked = True
        if not unique_box:
            self.elements_button.setExclusive(False)
        for i, element in enumerate(all_elements_names):
            check_box = QCheckBox()
            check_box.setText(element)
            if box_checked and not unique_box:
                check_box.setChecked(box_checked)
            elif unique_box_not_checked:
                check_box.setChecked(True)
                unique_box_not_checked = False
            self.elements_vbox_layout.addWidget(check_box)
            self.elements_button.addButton(check_box, i)

    """
    Triggers
    """
    def cancel_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.multiple_selector_listener.cancel_button_clicked()

    def confirm_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        elements_selected = self.get_all_elements_selected()
        self.multiple_selector_listener.confirm_button_clicked(elements_selected)

    def select_all_elements_trigger(self):
        """
        Select all the elements of the window.
        """
        for i in range(1, self.elements_vbox_layout.count()):
            check_box = self.elements_vbox_layout.itemAt(i).widget()
            check_box.setChecked(True)

    def unselect_all_elements_trigger(self):
        """
        Unselect all the elements of the window.
        """
        for i in range(1, self.elements_vbox_layout.count()):
            check_box = self.elements_vbox_layout.itemAt(i).widget()
            check_box.setChecked(False)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: elementsSelectorController
        """
        self.multiple_selector_listener = listener

    """
    Getters
    """
    def get_all_elements_selected(self):
        """
        Get the elements selected by the user in the multiple elements' selector.
        :return: Elements selected in the multiple elements' selector.
        :rtype: str/list of str
        """
        all_elements = []
        start_idx = 0
        if not self.unique_box:
            start_idx = 1       # Because we have the select and unselect buttons.
        for i in range(start_idx, self.elements_vbox_layout.count()):
            check_box = self.elements_vbox_layout.itemAt(i).widget()
            if check_box.isChecked():
                all_elements.append(check_box.text())
        return all_elements
