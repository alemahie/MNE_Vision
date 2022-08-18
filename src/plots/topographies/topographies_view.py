#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Topographies view
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QButtonGroup, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class topographiesView(QWidget):
    def __init__(self):
        """
        Window displaying the parameters for computing topographies on the dataset.
        """
        super().__init__()
        self.topographies_listener = None

        self.setWindowTitle("Topographies")

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        self.time_points_widget = QWidget()
        self.time_points_layout = QHBoxLayout()
        self.time_points_layout.addWidget(QLabel("Time points to plot (sec) : "))
        self.time_points_line = QLineEdit()
        self.time_points_layout.addWidget(self.time_points_line)
        self.time_points_widget.setLayout(self.time_points_layout)

        self.topographies_mode_widget = QWidget()
        self.topographies_mode_layout = QVBoxLayout()
        self.topographies_mode_buttons = QButtonGroup()
        self.separated_check_box = QCheckBox()
        self.separated_check_box.setChecked(True)
        self.separated_check_box.setText("Separated topographies")
        self.topographies_mode_buttons.addButton(self.separated_check_box, 1)   # Button with ID 1
        self.animated_check_box = QCheckBox()
        self.animated_check_box.setText("Animated topographies")
        self.topographies_mode_buttons.addButton(self.animated_check_box, 2)  # Button with ID 2
        self.topographies_mode_layout.addWidget(self.separated_check_box)
        self.topographies_mode_layout.addWidget(self.animated_check_box)
        self.topographies_mode_widget.setLayout(self.topographies_mode_layout)

        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_topographies_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_topographies_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.time_points_widget)
        self.vertical_layout.addWidget(self.topographies_mode_widget)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    """
    Triggers
    """
    def cancel_topographies_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.topographies_listener.cancel_button_clicked()

    def confirm_topographies_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        mode = None
        checked_button = self.topographies_mode_buttons.checkedButton()
        button_id = self.topographies_mode_buttons.id(checked_button)
        if button_id == 1:      # Separated topographies
            mode = "separated"
        elif button_id == 2:    # Animated topographies
            mode = "animated"
        time_points = self.create_array_from_time_points(mode)

        self.topographies_listener.confirm_button_clicked(time_points, mode)

    """
    Others
    """
    def create_array_from_time_points(self, mode):
        """
        Create an array of time points depending on the time points given.
        :param mode: Mode used for plotting the topographies.
        :type mode: str
        :return: "auto" if no time points are set. Will create an evenly dispersed time points to display.
        :rtype: str/None/list of float
        """
        time_points = self.time_points_line.text()
        if time_points == "":
            if mode == "separated":
                return "auto"
            elif mode == "animated":
                return None
        else:
            splitted_time_points = time_points.split()
            float_time_points = []
            for time_point in splitted_time_points:
                float_time_points.append(float(time_point.replace(',', '.')))
            return float_time_points

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: topographiesController
        """
        self.topographies_listener = listener
