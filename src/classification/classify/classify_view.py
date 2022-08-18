#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Classify view
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QGridLayout, QCheckBox, \
    QDoubleSpinBox, QSpinBox

from utils.elements_selector.elements_selector_controller import multipleSelectorController
from utils.view.separator import create_layout_separator

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class classifyView(QWidget):
    def __init__(self, number_of_channels, event_values, event_ids):
        """
        Window displaying the parameters for performing the classification.
        :param number_of_channels: The number of channels in the dataset.
        :type number_of_channels: int
        :param event_values: Event_id associated to each epoch/trial.
        :type event_values: list of, list of int
        :param event_ids: Name of the events associated to their id.
        :type event_ids: dict
        """
        super().__init__()
        self.classify_listener = None
        self.number_of_channels = number_of_channels
        self.event_values = event_values
        self.event_ids = event_ids

        self.pipeline_selector_controller = None
        self.pipeline_selected = None
        self.events_selector_controller = None
        self.trials_selected = None

        self.setWindowTitle("Classification")

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        # Parameters
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.pipeline_selection_button = QPushButton("&Pipelines ...", self)
        self.pipeline_selection_button.clicked.connect(self.pipeline_selection_trigger)
        self.feature_selection = QCheckBox()
        self.number_of_features = QSpinBox()
        self.number_of_features.setRange(1, self.number_of_channels)
        if self.number_of_channels >= 20:
            self.number_of_features.setValue(20)
        else:
            self.number_of_features.setValue(self.number_of_channels)
        self.hyper_tuning = QCheckBox()
        self.cross_validation_number = QDoubleSpinBox()
        self.cross_validation_number.setValue(5)
        self.cross_validation_number.setMinimum(1)
        self.cross_validation_number.setDecimals(0)
        # Layout of parameters
        self.grid_layout.addWidget(QLabel("Pipeline selection : "), 0, 0)
        self.grid_layout.addWidget(self.pipeline_selection_button, 0, 1)
        self.grid_layout.addWidget(QLabel("Feature selection : "), 1, 0)
        self.grid_layout.addWidget(self.feature_selection, 1, 1)
        self.grid_layout.addWidget(QLabel("Number of features to select : "), 2, 0)
        self.grid_layout.addWidget(self.number_of_features, 2, 1)
        self.grid_layout.addWidget(QLabel("Hyper-parameters tuning : "), 3, 0)
        self.grid_layout.addWidget(self.hyper_tuning, 3, 1)
        self.grid_layout.addWidget(QLabel("Cross-validation k-fold : "), 4, 0)
        self.grid_layout.addWidget(self.cross_validation_number, 4, 1)
        self.grid_widget.setLayout(self.grid_layout)

        # Trial selection
        self.trial_selection_widget = QWidget()
        self.trial_selection_layout = QGridLayout()
        self.trial_selection_label = QLabel("Trials indexes to compute (default : all) :")
        self.trial_selection_indexes = QPushButton("Select by trials indexes")
        self.trial_selection_indexes.clicked.connect(self.trial_selection_indexes_trigger)
        self.trial_selection_events = QPushButton("Select by events")
        self.trial_selection_events.clicked.connect(self.trial_selection_events_trigger)
        self.trial_selection_layout.addWidget(self.trial_selection_label, 0, 0)
        self.trial_selection_layout.addWidget(self.trial_selection_indexes, 0, 1)
        self.trial_selection_layout.addWidget(self.trial_selection_events, 1, 1)
        self.trial_selection_widget.setLayout(self.trial_selection_layout)

        # Cancel Confirm
        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_classification_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_classification_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.grid_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.trial_selection_widget)
        self.vertical_layout.addWidget(create_layout_separator())
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    """
    Plot
    """
    @staticmethod
    def plot_results(classifier):
        """
        Plot the classification results.
        :param classifier: The classifier that did the classification.
        :type classifier: ApplePyClassifier
        """
        classifier.show_results(4)

    """
    Triggers
    """
    def cancel_classification_trigger(self):
        """
        Send the information to the controller that the computation is cancelled.
        """
        self.classify_listener.cancel_button_clicked()

    def confirm_classification_trigger(self):
        """
        Retrieve the parameters and send the information to the controller.
        """
        feature_selection = self.feature_selection.isChecked()
        number_of_channels_to_select = self.number_of_features.value()
        hyper_tuning = self.hyper_tuning.isChecked()
        cross_val_number = int(self.cross_validation_number.value())
        if self.trials_selected is None:
            trials_selected = [i for i in range(len(self.event_values))]
        else:
            trials_selected = self.trials_selected
        self.classify_listener.confirm_button_clicked(self.pipeline_selected, feature_selection, number_of_channels_to_select,
                                                      hyper_tuning, cross_val_number, trials_selected)

    def pipeline_selection_trigger(self):
        """
        Open the multiple selector window.
        The user can select a multiple pipelines used for the classification.
        """
        title = "Select the pipelines used for the classification :"
        all_pipelines = ['XdawnCov', 'Xdawn', 'CSP', 'CSP2', 'cov', 'HankelCov', 'CSSP', 'PSD', 'MDM', 'FgMDM']
        # 'XdawnCovTSLR', 'Cosp'
        self.pipeline_selector_controller = multipleSelectorController(all_pipelines, title, box_checked=True,
                                                                       element_type="pipeline")
        self.pipeline_selector_controller.set_listener(self.classify_listener)

    def trial_selection_indexes_trigger(self):
        """
        Open the multiple selector window.
        The user can select the trials indexes he wants the source estimation to be computed on.
        """
        title = "Select the trial's events used for computing the source estimation:"
        indexes_list = [str(i+1) for i in range(len(self.event_values))]
        self.events_selector_controller = multipleSelectorController(indexes_list, title, box_checked=True,
                                                                     element_type="indexes")
        self.events_selector_controller.set_listener(self.classify_listener)

    def trial_selection_events_trigger(self):
        """
        Open the multiple selector window.
        The user can select the events he wants the source estimation to be computed on.
        """
        title = "Select the trial's events used for computing the source estimation:"
        events_ids_list = list(self.event_ids.keys())
        self.events_selector_controller = multipleSelectorController(events_ids_list, title, box_checked=True,
                                                                     element_type="events")
        self.events_selector_controller.set_listener(self.classify_listener)

    """
    Utils
    """
    def check_element_type(self, elements_selected, element_type):
        if element_type == "pipeline":
            self.set_pipeline_selected(elements_selected)
        elif element_type == "indexes" or element_type == "events":
            self.set_trials_selected(elements_selected, element_type)

    """
    Setters
    """
    def set_listener(self, listener):
        """
        Set the listener to the controller.
        :param listener: Listener to the controller.
        :type listener: classifyController
        """
        self.classify_listener = listener

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

    def set_pipeline_selected(self, pipeline):
        """
        Set the pipeliens selected in the multiple selector window.
        :param pipeline: Pipelines selected
        :type pipeline: list of str
        """
        self.pipeline_selected = pipeline
