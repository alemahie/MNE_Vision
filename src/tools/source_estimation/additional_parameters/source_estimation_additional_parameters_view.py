#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Source estimation additional parameters
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QCheckBox, QLabel, QLineEdit, QFileDialog

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class sourceEstimationAdditionalParametersView(QWidget):
    def __init__(self):
        """

        """
        super().__init__()
        self.source_estimation_additional_parameters_listener = None
        self.export_data_path = None

        self.global_layout = QVBoxLayout()
        self.setLayout(self.global_layout)

        # Exportation
        self.export_data_widget = QWidget()
        self.export_data_layout = QVBoxLayout()
        self.export_data_check_box = QCheckBox()
        self.export_data_check_box.setText("Export the source estimation data into a TXT file after the computation : ")
        self.export_data_layout.addWidget(self.export_data_check_box)
        self.export_data_widget.setLayout(self.export_data_layout)

        self.export_data_path_widget = QWidget()
        self.export_data_path_layout = QHBoxLayout()
        self.export_data_path_label = QLabel("Export file path : ")
        self.export_data_path_line = QLineEdit()
        self.export_data_path_button = QPushButton("...")
        self.export_data_path_button.clicked.connect(self.export_data_path_clicked)
        self.export_data_path_layout.addWidget(self.export_data_path_label)
        self.export_data_path_layout.addWidget(self.export_data_path_line)
        self.export_data_path_layout.addWidget(self.export_data_path_button)
        self.export_data_path_widget.setLayout(self.export_data_path_layout)

        # Cancel Confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_source_estimation_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_source_estimation_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.global_layout.addWidget(self.export_data_widget)
        self.global_layout.addWidget(self.export_data_path_widget)
        self.global_layout.addWidget(self.cancel_confirm_widget)

    """
    Triggers
    """
    def cancel_source_estimation_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.source_estimation_additional_parameters_listener.cancel_button_clicked()

    def confirm_source_estimation_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        if self.export_data_check_box.isChecked():
            export_path = self.export_data_path
        else:
            export_path = None
        self.source_estimation_additional_parameters_listener.confirm_button_clicked(export_path)

    def export_data_path_clicked(self):
        """
        Get the path to the file when wanting to export the source estimation data.
        """
        path_to_file = QFileDialog().getSaveFileName(self, "Export source estimation data to TXT file")
        self.export_data_path = path_to_file[0]
        self.export_data_path_line.setText(self.export_data_path)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: sourceEstimationAdditionalParametersController
        """
        self.source_estimation_additional_parameters_listener = listener
