#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Files runnable
"""

from PyQt5.QtCore import QRunnable, pyqtSignal, QObject

from mne import read_epochs, find_events, events_from_annotations
from mne.channels import make_standard_montage
from mne.io import read_raw_fif, read_raw_eeglab, read_epochs_eeglab

from utils.cnt_reader.cnt_file_reader import get_raw_from_cnt
from utils.view.error_window import errorWindow

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
    error = pyqtSignal()


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
            self.signals.finished.emit()
        except TypeError as error:
            error_message = "An error has occurred"
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()

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
    error = pyqtSignal()


class openCntFileRunnable(QRunnable):
    def __init__(self, path_to_file):
        """
        Runnable for the opening of an ANT eego CNT file, getting the dataset's data.
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
        Launch the reading of the ANT eego CNT file.
        Notifies the main model that the computation is finished.
        """
        try:
            self.file_data = get_raw_from_cnt(self.path_to_file)
            self.file_type = "Raw"
            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error has occurred during the reading of the ANT eego CNT file."
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()

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
    error = pyqtSignal()


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
        self.read_events = None
        self.read_event_ids = None

    def run(self):
        """
        Launch the reading of the SET file.
        Notifies the main model that the computation is finished.
        """
        raw_read, epochs_read = False, False
        detailed_error = None
        try:
            self.file_data = read_raw_eeglab(self.path_to_file, preload=True)
            self.file_type = "Raw"
            raw_read = True
        except Exception as error:
            raw_read = False
            print(error)
            print(type(error))
            detailed_error = error

        if not raw_read:    # Raw reading failed, try epochs
            try:
                self.file_data = read_epochs_eeglab(self.path_to_file)
                self.file_type = "Epochs"
                epochs_read = True
            except Exception as error:
                epochs_read = False
                detailed_error = error
                print(error)
                print(type(error))

        if raw_read or epochs_read:
            self.signals.finished.emit()
        else:
            error_message = "An error has occurred during the reading of the SET file."
            error_window = errorWindow(error_message, detailed_message=str(detailed_error))
            error_window.show()
            self.signals.error.emit()

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
            try:
                montage = make_standard_montage(self.montage)
                self.file_data.set_montage(montage)
            except Exception as error:
                error_message = "The provided montage does not work with the data in the dataset, the default montage will " \
                                "be used."
                error_window = errorWindow(error_message)
                error_window.show()
        self.file_data = self.file_data.pick_channels(self.channels_selected)
        if self.tmin is not None and self.tmax is not None:
            if self.tmin is None:
                self.tmin = self.file_data.times[0]
            if self.tmax is None:
                self.tmax = self.file_data.times[-1]
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
        self.read_event_ids = None

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
        except Exception as error:
            if self.stim_channel is not None:
                error_message = "An error has occurred when trying to find the events on the given channel, please check the " \
                                "channel used for the computation."
                error_window = errorWindow(error_message, detailed_message=str(error))
                error_window.show()
                self.signals.error.emit()
            else:   # No stim channel was precised and computation failed, so try another method.
                try:
                    events, event_ids = events_from_annotations(self.file_data)
                    self.read_events = events
                    self.read_event_ids = event_ids
                    self.signals.finished.emit()
                except Exception as error:
                    error_message = "An error has occurred when trying to find the events."
                    error_window = errorWindow(error_message, detailed_message=str(error))
                    error_window.show()
                    self.signals.error.emit()

    def get_read_events(self):
        """
        Get the read events.
        :return: The events.
        :rtype: list of int
        """
        return self.read_events

    def get_read_event_ids(self):
        """
        Get the read event ids.
        :return: The event ids.
        :rtype: dict
        """
        return self.read_event_ids


# Export Data to CSV file
class exportDataCSVWorkerSignals(QObject):
    """
    Contain the signals used by the export data CSV runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class exportDataCSVRunnable(QRunnable):
    def __init__(self, file_data, path_to_file):
        """
        Runnable for exporting the data of the dataset into a CSV file.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param path_to_file: Path to the exportation file.
        :type path_to_file: str
        """
        super().__init__()
        self.signals = exportDataCSVWorkerSignals()

        self.file_data = file_data
        self.path_to_file = path_to_file

    def run(self):
        """
        Launch the exportation of the data of the dataset into a CSV file.
        Notifies the main model that the computation is finished.
        """
        try:
            data = self.file_data.get_data()
            time_points = self.file_data.times

            file = open(self.path_to_file + ".csv", "x")
            # Write header
            file.write("Time")
            for channel in self.file_data.ch_names:
                file.write(", " + channel)
            file.write("\n")
            # Write data
            for i in range(len(data)):  # Epoch
                for j in range(len(data[0][0])):   # Time
                    file.write(str(time_points[j]))
                    for k in range(len(data[0])):    # Channel
                        file.write(", " + str(data[i][i][j]))
                    file.write("\n")
            file.close()
            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error has occurred when exporting the data into a CSV file."
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()


# Export Data to SET file
class exportDataSETWorkerSignals(QObject):
    """
    Contain the signals used by the export data CSV runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class exportDataSETRunnable(QRunnable):
    def __init__(self, file_data, path_to_file):
        """
        Runnable for exporting the data of the dataset into a SET file.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param path_to_file: Path to the exportation file.
        :type path_to_file: str
        """
        super().__init__()
        self.signals = exportDataSETWorkerSignals()

        self.file_data = file_data
        self.path_to_file = path_to_file

    def run(self):
        """
        Launch the exportation of the data of the dataset into a SET file.
        Notifies the main model that the computation is finished.
        """
        try:
            self.file_data.export(self.path_to_file + ".set", fmt="eeglab")
            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error has occurred when exporting the data into a SET file."
            error_window = errorWindow(error_message=error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()


# Export Events to TXT file
class exportEventsTXTWorkerSignals(QObject):
    """
    Contain the signals used by the export events TXT runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class exportEventsTXTRunnable(QRunnable):
    def __init__(self, file_data, path_to_file):
        """
        Runnable for exporting the events of the dataset into a TXT file.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param path_to_file: Path to the exportation file.
        :type path_to_file: str
        """
        super().__init__()
        self.signals = exportEventsTXTWorkerSignals()

        self.file_data = file_data
        self.path_to_file = path_to_file

    def run(self):
        """
        Launch the exportation of the events of the dataset into a TXT file.
        Notifies the main model that the computation is finished.
        """
        try:
            event_values = self.file_data.events
            event_ids = self.file_data.event_id
            file = open(self.path_to_file + ".txt", "x")
            file.write("Number, Type, Latency \n")
            for i in range(len(event_values)):
                latency = event_values[i][0]
                event_id = event_values[i][2]
                file.write(str(i) + ", ")   # Event number
                for key in event_ids.keys():
                    if event_ids[key] == event_id:  # Find correct key / event name
                        file.write(key + ", ")
                        break
                file.write(str(latency) + "\n")
            file.close()
            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error has occurred during the exportation of the events into a TXT file."
            error_window = errorWindow(error_message=error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()
