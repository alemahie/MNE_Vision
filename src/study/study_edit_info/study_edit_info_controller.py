#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Study Edit Info Controller
"""

from study.study_edit_info.study_edit_info_listener import studyEditInfoListener
from study.study_edit_info.study_edit_info_view import studyEditInfoView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class studyEditInfoController(studyEditInfoListener):
    def __init__(self, study):
        """
        Controller for editing the info of the study.
        Create a new window for displaying the information.
        :param study: The current study created on the datasets.
        :type study: studyModel
        """
        self.main_listener = None
        self.study_edit_info_view = studyEditInfoView(study)
        self.study_edit_info_view.set_listener(self)

        self.study_edit_info_view.show()

    def cancel_button_clicked(self):
        """
        Close the window.
        """
        self.study_edit_info_view.close()

    def confirm_button_clicked(self, study_name, task_name, subjects, sessions, runs, conditions, groups):
        """
        Close the window and send the information to the main controller
        :param study_name: The name of the study_creation
        :type study_name: str
        :param task_name: The name of the task linked to the study_creation
        :type task_name: str
        :param subjects: The subjects assigned to each dataset in the study_creation
        :type subjects: list of str
        :param sessions: The sessions assigned to each dataset in the study_creation
        :type sessions: list of str
        :param runs: The runs assigned to each dataset in the study_creation
        :type runs: list of str
        :param conditions: The conditions assigned to each dataset in the study_creation
        :type conditions: list of str
        :param groups: The groups assigned to each dataset in the study_creation
        :type groups: list of str
        """
        self.study_edit_info_view.close()
        self.main_listener.edit_study_information(study_name, task_name, subjects, sessions, runs, conditions, groups)

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
