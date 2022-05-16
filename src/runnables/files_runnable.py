#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Files runnable
"""

from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

from mne import read_epochs, find_events
from mne.channels import make_standard_montage
from mne.io import read_raw_fif, read_raw_eeglab, read_epochs_eeglab

from utils import cnt_file_reader

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


# Open FIF File
class openFifFileWorkerSignals(QObject):
    """
    Contain the signals used by the open FIF file runnable.
    """
    finished = pyqtSignal()


class openFifFileRunnable(QRunnable):
    def __init__(self, path_to_file):
        """
        Runnable for the opening of a FIF file, getting the dataset's data.
        :param path_to_file: The path to the file.
        :type path_to_file: str
        """
        super().__init__()
        self.signals = openFifFileWorkerSignals()

        self.path_to_file = path_to_file
        self.file_data = None
        self.file_type = None

    def run(self):
        """
        Launch the reading of the FIF file.
        Notifies the main model that the computation is finished.
        """
        try:
            if self.path_to_file[-7:-4] == "raw":
                self.file_type = "Raw"
                self.file_data = read_raw_fif(self.path_to_file, preload=True)
            else:
                self.file_type = "Epochs"
                self.file_data = read_epochs(self.path_to_file, preload=True)
        except TypeError:
            print("Error")
        self.signals.finished.emit()

    def get_file_data(self):
        """
        Get the file data.
        :return: MNE data of the dataset.
        :rtype: MNE.Epochs/MNE.Raw
        """
        return self.file_data

    def get_file_type(self):
        """
        Get the file type.
        :return: The file type.
        :rtype: str
        """
        return self.file_type

    def get_path_to_file(self):
        """
        Get the path to the file.
        :return: The path to the file.
        :rtype: str
        """
        return self.path_to_file


# Open CNT File
class openCntFileWorkerSignals(QObject):
    """
    Contain the signals used by the open CNT file runnable.
    """
    finished = pyqtSignal()


class openCntFileRunnable(QRunnable):
    def __init__(self, path_to_file):
        """
        Runnable for the opening of a CNT file, getting the dataset's data.
        :param path_to_file: The path to the file.
        :type path_to_file: str
        """
        super().__init__()
        self.signals = openCntFileWorkerSignals()

        self.path_to_file = path_to_file
        self.file_data = None
        self.file_type = None

    def run(self):
        """
        Launch the reading of the CNT file.
        Notifies the main model that the computation is finished.
        """
        try:
            self.file_data = cnt_file_reader.get_raw_from_cnt(self.path_to_file)
            self.file_type = "Raw"
        except TypeError:
            print("Error")
        self.signals.finished.emit()

    def get_file_data(self):
        """
        Get the file data.
        :return: MNE data of the dataset.
        :rtype: MNE.Epochs/MNE.Raw
        """
        return self.file_data

    def get_file_type(self):
        """
        Get the file type.
        :return: The file type.
        :rtype: str
        """
        return self.file_type

    def get_path_to_file(self):
        """
        Get the path to the file.
        :return: The path to the file.
        :rtype: str
        """
        return self.path_to_file


# Open Set File
class openSetFileWorkerSignals(QObject):
    """
    Contain the signals used by the open SET file runnable.
    """
    finished = pyqtSignal()


class openSetFileRunnable(QRunnable):
    def __init__(self, path_to_file):
        """
        Runnable for the opening of a SET file, getting the dataset's data.
        :param path_to_file: The path to the file.
        :type path_to_file: str
        """
        super().__init__()
        self.signals = openSetFileWorkerSignals()

        self.path_to_file = path_to_file
        self.file_data = None
        self.file_type = None

    def run(self):
        """
        Launch the reading of the SET file.
        Notifies the main model that the computation is finished.
        """
        try:
            self.file_data = read_raw_eeglab(self.path_to_file, preload=True)
            self.file_type = "Raw"
        except TypeError:
            self.file_data = read_epochs_eeglab(self.path_to_file)
            self.file_type = "Epochs"
        except FileNotFoundError:
            self.file_data = None
            self.file_type = None
        self.signals.finished.emit()

    def get_file_data(self):
        """
        Get the file data.
        :return: MNE data of the dataset.
        :rtype: MNE.Epochs/MNE.Raw
        """
        return self.file_data

    def get_file_type(self):
        """
        Get the file type.
        :return: The file type.
        :rtype: str
        """
        return self.file_type

    def get_path_to_file(self):
        """
        Get the path to the file.
        :return: The path to the file.
        :rtype: str
        """
        return self.path_to_file


# Load Data Info
class loadDataInfoWorkerSignals(QObject):
    """
    Contain the signals used by the load data info runnable.
    """
    finished = pyqtSignal()


class loadDataInfoRunnable(QRunnable):
    def __init__(self, file_data, montage, channels_selected, tmin, tmax):
        """
        Runnable for the loading of the additional information of the dataset.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param montage: Montage of the headset
        :type montage: str
        :param channels_selected: Channels selected
        :type channels_selected: list of str
        :param tmin: Start time of the epoch or raw file to keep
        :type tmin: float
        :param tmax: End time of the epoch or raw file to keep
        :type tmax: float
        """
        super().__init__()
        self.signals = loadDataInfoWorkerSignals()

        self.file_data = file_data
        self.montage = montage
        self.channels_selected = channels_selected
        self.tmin = tmin
        self.tmax = tmax

    def run(self):
        """
        Launch the loading of the additional information of the dataset.
        Notifies the main model that the computation is finished.
        """
        if self.montage != "default":
            montage = make_standard_montage(self.montage)
            self.file_data.set_montage(montage)
        self.file_data = self.file_data.pick_channels(self.channels_selected)
        self.file_data = self.file_data.crop(tmin=self.tmin, tmax=self.tmax)
        self.signals.finished.emit()

    def get_file_data(self):
        return self.file_data


# Find Events From Channel
class findEventsFromChannelWorkerSignals(QObject):
    """
    Contain the signals used by the find events from channel runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class findEventsFromChannelRunnable(QRunnable):
    def __init__(self, file_data, stim_channel):
        """
        Runnable for finding the events from a stimulation channel of the dataset.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param stim_channel: The stimulation channel.
        :type stim_channel: str
        """
        super().__init__()
        self.signals = findEventsFromChannelWorkerSignals()

        self.file_data = file_data
        self.stim_channel = stim_channel
        self.read_events = None

    def run(self):
        """
        Launch the reading of the events based on the stimulation channel of the given data.
        Notifies the main model that the computation is finished.
        If no events can be found in the dataset or if the stimulation channel does not contain any information, an error
        message is displayed describing the error.
        Notifies the main model when an error occurs.
        """
        try:
            self.read_events = find_events(self.file_data, stim_channel=self.stim_channel)
            self.signals.finished.emit()
        except Exception as e:
            print(e)
            self.signals.error.emit()

    def get_read_events(self):
        """
        Get the read events.
        :return: The events.
        :rtype: list of int
        """
        return self.read_events
