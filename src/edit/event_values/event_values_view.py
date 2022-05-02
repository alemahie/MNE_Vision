#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Event Values View
"""
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class eventValuesView(QWidget):
    def __init__(self, event_values, event_ids):
        super().__init__()
        self.event_values_listener = None
        self.event_values = event_values
        self.event_ids = event_ids
        number_of_events = len(self.event_values)

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        self.event_name_line = QLineEdit()
        self.only_int_epoch_number = QIntValidator()
        self.epoch_number_line = QLineEdit()
        self.epoch_number_line.setValidator(self.only_int_epoch_number)

        self.info_widget = QWidget()
        self.info_grid_layout = QGridLayout()
        self.info_grid_layout.addWidget(QLabel("Events information : "), 0, 0)
        self.info_grid_layout.addWidget(QLabel("Event name : "), 1, 0)
        self.info_grid_layout.addWidget(QLabel("Epoch number : "), 2, 0)
        self.info_grid_layout.addWidget(self.event_name_line, 1, 1)
        self.info_grid_layout.addWidget(self.epoch_number_line, 2, 1)
        self.info_widget.setLayout(self.info_grid_layout)

        self.event_change_info_widget = QWidget()
        self.event_change_info_layout = QHBoxLayout()
        self.event_change_info_layout.addWidget(QLabel(f"Event number : (out of {number_of_events} events)"))
        self.event_change_info_widget.setLayout(self.event_change_info_layout)

        self.change_event_widget = QWidget()
        self.change_event_layout = QHBoxLayout()
        self.previous_button = QPushButton("&Previous", self)
        self.previous_button.clicked.connect(self.previous_button_trigger)
        self.next_button = QPushButton("&Next", self)
        self.next_button.clicked.connect(self.next_button_trigger)
        self.only_int_event_number = QIntValidator(1, number_of_events, self)
        self.event_number_line = QLineEdit()
        self.event_number_line.setValidator(self.only_int_event_number)
        self.event_number_line.editingFinished.connect(self.editing_finished_trigger)
        self.change_event_layout.addWidget(self.previous_button)
        self.change_event_layout.addWidget(self.event_number_line)
        self.change_event_layout.addWidget(self.next_button)
        self.change_event_widget.setLayout(self.change_event_layout)

        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_event_values_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_event_values_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.info_widget)
        self.vertical_layout.addWidget(self.event_change_info_widget)
        self.vertical_layout.addWidget(self.change_event_widget)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    """
    Triggers
    """
    def cancel_event_values_trigger(self):
        self.event_values_listener.cancel_button_clicked()

    def confirm_event_values_trigger(self):
        self.event_values_listener.confirm_button_clicked()

    def previous_button_trigger(self):
        self.event_values_listener.previous_button_clicked()

    def next_button_trigger(self):
        self.event_values_listener.next_button_clicked()

    def editing_finished_trigger(self):
        event_number = int(self.event_number_line.text())-1
        self.event_values_listener.editing_finished_clicked(event_number)

    """
    Updates
    """
    def update_event_displayed(self, event_number, event_name, epoch_number):
        self.event_number_line.setText(str(event_number + 1))
        self.event_name_line.setText(event_name)
        self.epoch_number_line.setText(str(epoch_number + 1))

    """
    Setters
    """
    def set_listener(self, listener):
        self.event_values_listener = listener
