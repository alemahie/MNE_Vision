#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Extract Epochs View
"""

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QGridLayout, QLabel, QHBoxLayout, QVBoxLayout

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"

from utils.elements_selector.elements_selector_controller import multipleSelectorController
from utils.view.separator import create_layout_separator


class extractEpochsView(QWidget):
    def __init__(self, event_values, event_ids):
        """
        Window displaying the parameters for extracting epochs from the dataset.
        :param event_values: Event_id associated to each epoch/trial.
        :type event_values: list of, list of int
        :param event_ids: Name of the events associated to their id.
        :type event_ids: dict
        """
        super().__init__()
        self.extract_epochs_listener = None

        self.events_selector_controller = None
        self.event_values = event_values
        self.event_ids = event_ids
        self.trials_selected = None

        self.setWindowTitle("Extract Epochs")

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.tmin_line = QLineEdit("-1,0")
        self.tmin_line.setValidator(QDoubleValidator())
        self.tmax_line = QLineEdit("1,0")
        self.tmax_line.setValidator(QDoubleValidator())
        self.grid_layout.addWidget(QLabel("Epoch start (sec) : "), 0, 0)
        self.grid_layout.addWidget(self.tmin_line, 0, 1)
        self.grid_layout.addWidget(QLabel("Epoch end (sec) : "), 1, 0)
        self.grid_layout.addWidget(self.tmax_line, 1, 1)
        self.grid_widget.setLayout(self.grid_layout)

        # Trial selection
        self.trial_selection_widget = QWidget()
        self.trial_selection_layout = QGridLayout()
        self.trial_selection_label = QLabel("Events indexes to extract (default : all) :")
        self.trial_selection_indexes = QPushButton("Select by event indexes")
        self.trial_selection_indexes.clicked.connect(self.event_selection_indexes_trigger)
        self.trial_selection_events = QPushButton("Select by events type")
        self.trial_selection_events.clicked.connect(self.selection_events_trigger)
        self.trial_selection_layout.addWidget(self.trial_selection_label, 0, 0)
        self.trial_selection_layout.addWidget(self.trial_selection_indexes, 0, 1)
        self.trial_selection_layout.addWidget(self.trial_selection_events, 1, 1)
        self.trial_selection_widget.setLayout(self.trial_selection_layout)

        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_extract_epochs_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_extract_epochs_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.grid_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.trial_selection_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    """
    Triggers
    """
    def cancel_extract_epochs_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.extract_epochs_listener.cancel_button_clicked()

    def confirm_extract_epochs_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        tmin = None
        tmax = None
        if self.tmin_line.hasAcceptableInput():
            tmin = self.tmin_line.text()
            tmin = float(tmin.replace(',', '.'))
        if self.tmin_line.hasAcceptableInput():
            tmax = self.tmax_line.text()
            tmax = float(tmax.replace(',', '.'))

        if self.trials_selected is None:
            trials_selected = [i for i in range(len(self.event_values))]
        else:
            trials_selected = self.trials_selected

        self.extract_epochs_listener.confirm_button_clicked(tmin, tmax, trials_selected)

    def event_selection_indexes_trigger(self):
        """
        Open the multiple selector window.
        The user can select the event indexes he wants the extraction to be computed on.
        """
        title = "Select the trial's events used for computing the source estimation:"
        indexes_list = [str(i+1) for i in range(len(self.event_values))]
        self.events_selector_controller = multipleSelectorController(indexes_list, title, box_checked=True,
                                                                     element_type="indexes")
        self.events_selector_controller.set_listener(self.extract_epochs_listener)

    def selection_events_trigger(self):
        """
        Open the multiple selector window.
        The user can select the events type he wants the extraction to be computed on.
        """
        title = "Select the trial's events used for computing the source estimation:"
        events_ids_list = list(self.event_ids.keys())
        self.events_selector_controller = multipleSelectorController(events_ids_list, title, box_checked=True,
                                                                     element_type="events")
        self.events_selector_controller.set_listener(self.extract_epochs_listener)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: extractEpochsController
        """
        self.extract_epochs_listener = listener

    def set_trials_selected(self, elements_selected, element_type):
        """
        Set the channels selected in the multiple selector window.
        :param elements_selected: Trials or Events selected.
        :type elements_selected: list of str
        :param element_type: Type of the element selected, used in case multiple element selector windows can be open in
        a window. Can thus distinguish the returned elements.
        :type element_type: str
        """
        trials_to_use = []
        if element_type == "indexes":
            for trial in elements_selected:
                trials_to_use.append(int(trial)-1)  # -1 To get index in the list, not "position"
        elif element_type == "events":
            # Get ids of the events selected
            event_ids_selected = []
            for event in elements_selected:
                event_ids_selected.append(self.event_ids[event])
            # Get indexes of the trials if their event is selected.
            for i in range(len(self.event_values)):
                if self.event_values[i][2] in event_ids_selected:
                    trials_to_use.append(i)
        self.trials_selected = trials_to_use
