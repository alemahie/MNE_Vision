#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Study Edit Info View
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout

from utils.view.separator import create_layout_separator

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class studyEditInfoView(QWidget):
    def __init__(self, study):
        """
        Window displaying the parameters for loading additional data information.
        :param study: The current study created on the datasets.
        :type study: studyModel
        """
        super().__init__()
        self.study_listener = None

        self.setWindowTitle("Study Edit Info")

        self.global_layout = QVBoxLayout()
        self.setLayout(self.global_layout)

        # Dataset Name
        self.study_name_widget = QWidget()
        self.study_name_layout = QHBoxLayout()
        self.study_name_line = QLineEdit()
        self.study_name_line.setText(study.get_study_name())
        self.study_name_layout.addWidget(QLabel("Study name : "))
        self.study_name_layout.addWidget(self.study_name_line)
        self.study_name_widget.setLayout(self.study_name_layout)

        # Task Name
        self.task_name_widget = QWidget()
        self.task_name_layout = QHBoxLayout()
        self.task_name_line = QLineEdit()
        self.task_name_line.setText(study.get_task_name())
        self.task_name_layout.addWidget(QLabel("Task name : "))
        self.task_name_layout.addWidget(self.task_name_line)
        self.task_name_widget.setLayout(self.task_name_layout)

        # Datasets Grid
        self.datasets_widget = QWidget()
        self.datasets_layout = QGridLayout()
        self.all_dataset_lines = []
        dataset_names_labels = ["Dataset Filename", "Subject", "Session", "Run", "Condition", "Group"]
        for i in range(len(dataset_names_labels)):
            self.datasets_layout.addWidget(QLabel(dataset_names_labels[i]), 0, i)

        number_of_datasets = len(study.get_dataset_indexes())
        self.dataset_names = study.get_dataset_names()
        subjects = study.get_subjects()
        sessions = study.get_sessions()
        runs = study.get_runs()
        conditions = study.get_conditions()
        groups = study.get_groups()
        for i in range(number_of_datasets):       # Add lines
            self.all_dataset_lines.append([])
            dataset_line = QLineEdit(self.dataset_names[i])
            self.datasets_layout.addWidget(dataset_line, i+1, 0)
            self.all_dataset_lines[i].append(dataset_line)
            subject_line = QLineEdit(subjects[i])
            self.datasets_layout.addWidget(subject_line, i+1, 1)
            self.all_dataset_lines[i].append(subject_line)
            session_line = QLineEdit(sessions[i])
            self.datasets_layout.addWidget(session_line, i+1, 2)
            self.all_dataset_lines[i].append(session_line)
            run_line = QLineEdit(runs[i])
            self.datasets_layout.addWidget(run_line, i+1, 3)
            self.all_dataset_lines[i].append(run_line)
            condition_line = QLineEdit(conditions[i])
            self.datasets_layout.addWidget(condition_line, i+1, 4)
            self.all_dataset_lines[i].append(condition_line)
            group_line = QLineEdit(groups[i])
            self.datasets_layout.addWidget(group_line, i+1, 5)
            self.all_dataset_lines[i].append(group_line)
        self.datasets_widget.setLayout(self.datasets_layout)

        # Cancel Confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_study_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_study_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        # Layout
        self.global_layout.addWidget(self.study_name_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.datasets_widget)
        self.global_layout.addWidget(create_layout_separator())
        self.global_layout.addWidget(self.cancel_confirm_widget)

    """
    Triggers
    """
    def cancel_study_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.study_listener.cancel_button_clicked()

    def confirm_study_trigger(self):
        """
        Retrieve the all the additional information and send the information to the controller.
        """
        study_name = self.study_name_line.text()
        if study_name == "":
            study_name = "No Name"
        task_name = self.task_name_line.text()
        if task_name == "":
            task_name = "No Name"

        subjects = []
        sessions = []
        runs = []
        conditions = []
        groups = []
        for i in range(len(self.all_dataset_lines)):    # Each dataset
            subjects.append(self.all_dataset_lines[i][1].text())
            sessions.append(self.all_dataset_lines[i][2].text())
            runs.append(self.all_dataset_lines[i][3].text())
            conditions.append(self.all_dataset_lines[i][4].text())
            groups.append(self.all_dataset_lines[i][5].text())

        self.study_listener.confirm_button_clicked(study_name, task_name, subjects, sessions, runs, conditions, groups)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: loadDataInfoController
        """
        self.study_listener = listener
