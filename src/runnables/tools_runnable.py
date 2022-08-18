#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools runnable
"""

import numpy as np

from copy import deepcopy

from PyQt5.QtCore import QRunnable, pyqtSignal, QObject
from matplotlib import pyplot as plt

from mne import make_forward_solution, write_forward_solution, compute_covariance, setup_source_space, \
    write_source_spaces, make_bem_model, make_bem_solution, write_bem_solution, Epochs, read_source_spaces, \
    read_bem_solution, read_forward_solution, read_cov
from mne.minimum_norm import read_inverse_operator, make_inverse_operator, apply_inverse, \
    write_inverse_operator, apply_inverse_epochs
from mne.preprocessing import ICA
from mne.time_frequency import psd_welch
from mne.viz import plot_snr_estimate
from scipy.signal import welch

from utils.view.error_window import errorWindow
from utils.file_path_search import get_project_freesurfer_path

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


# Filter
class filterWorkerSignals(QObject):
    """
    Contain the signals used by the filter runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class filterRunnable(QRunnable):
    def __init__(self, low_frequency, high_frequency, channels_selected, file_data, filter_method):
        """
        Runnable for the computation of the filtering of the given data.
        :param low_frequency: Lowest frequency from where the data will be filtered.
        :type low_frequency: float
        :param high_frequency: Highest frequency from where the data will be filtered.
        :type high_frequency: float
        :param channels_selected: Channels on which the filtering will be performed.
        :type channels_selected: list of str
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param filter_method: Method used for the filtering, either FIR or IIR.
        :type filter_method: str
        """
        super().__init__()
        self.signals = filterWorkerSignals()

        self.low_frequency = low_frequency
        self.high_frequency = high_frequency
        self.channels_selected = channels_selected
        self.file_data = file_data
        self.filter_method = filter_method

    def run(self):
        """
        Launch the computation of the filtering on the given data.
        Notifies the main model that the computation is finished.
        """
        try:
            self.file_data.filter(l_freq=self.low_frequency, h_freq=self.high_frequency, picks=self.channels_selected,
                                  method=self.filter_method)
            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error has occurred during the filtering."
            error_window = errorWindow(error_message=error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()

    def get_file_data(self):
        """
        Get the file data.
        :return: MNE data of the dataset.
        :rtype: MNE.Epochs/MNE.Raw
        """
        return self.file_data

    def get_low_frequency(self):
        """
        Gets the low frequency used for the filtering.
        :return: The low frequency
        :rtype: float
        """
        return self.low_frequency

    def get_high_frequency(self):
        """
        Gets the high frequency used for the filtering.
        :return: The high frequency
        :rtype: float
        """
        return self.high_frequency

    def get_channels_selected(self):
        """
        Gets the channels used for the filtering.
        :return: The channels
        :rtype: list of str
        """
        return self.channels_selected

    def get_filter_method(self):
        """
        Gets the method used for the filtering.
        :return: The method used for the filtering, either FIR or IIR.
        :rtype: str
        """
        return self.filter_method


# Resampling
class resamplingWorkerSignals(QObject):
    """
    Contain the signals used by the resampling runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class resamplingRunnable(QRunnable):
    def __init__(self, frequency, file_data, events):
        """
        Runnable for the computation of the resampling of the given data.
        :param frequency: The new frequency at which the data will be resampled.
        :type frequency: int
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param events: The events.
        :type events: list of, list of int
        """
        super().__init__()
        self.signals = resamplingWorkerSignals()
        self.frequency = frequency
        self.file_data = file_data
        self.events = events

    def run(self):
        """
        Launch the computation of the resampling on the given data.
        Notifies the main model that the computation is finished.
        """
        try:
            old_frequency = self.file_data.info.get("sfreq")
            new_frequency = self.frequency
            self.file_data.resample(new_frequency)

            for i in range(0, len(self.events)):
                self.events[i][0] = self.events[i][0] * (new_frequency / old_frequency)

            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error has occurred during the resampling."
            error_window = errorWindow(error_message=error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()

    """
    Getters
    """
    def get_file_data(self):
        """
        Get the file data.
        :return: MNE data of the dataset.
        :rtype: MNE.Epochs/MNE.Raw
        """
        return self.file_data

    def get_events(self):
        """
        Get the events.
        :return: The events
        :rtype: list of, list of int
        """
        return self.events

    def get_frequency(self):
        """
        Get the frequency used for the resampling
        :return: The frequency
        :rtype: int
        """
        return self.frequency


# Re-referencing
class reReferencingWorkerSignals(QObject):
    """
    Contain the signals used by the re-referencing runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class reReferencingRunnable(QRunnable):
    def __init__(self, references, file_data, file_path, write_files, read_files, n_jobs):
        """
        Runnable for the computation of the re-referencing of the given data.
        :param references: References from which the data will be re-referenced. Can be a single or multiple channels;
        Can be an average of all channels; Can be a "point to infinity".
        :type references: list of str; str
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param file_path: The path to the file
        :type file_path: str
        :param write_files: Boolean telling if the data computed must be saved into files.
        :type write_files: bool
        :param read_files: Boolean telling if the data used for the computation can be read from computer files.
        :type read_files: bool
        :param n_jobs: Number of parallel processes used to compute the re-referencing
        :type n_jobs: int
        """
        super().__init__()
        self.signals = reReferencingWorkerSignals()

        self.references = references
        self.file_data = file_data
        self.file_path = file_path
        self.write_files = write_files
        self.read_files = read_files
        self.n_jobs = n_jobs

        self.subject = "fsaverage"
        self.subjects_dir = get_project_freesurfer_path()

    def run(self):
        """
        Launch the computation of the re-referencing on the given data.
        Compute the forward solution and the necessary information for the computation of the re-referencing to the point
        in infinity, which requires some information of the source space to be done.
        Notifies the main model that the computation is finished.
        """
        try:
            if self.references == "infinity":
                src = self.compute_source_space()
                bem = self.compute_bem_solution()
                fwd = self.compute_forward_solution(src, bem)
                self.file_data.set_eeg_reference('REST', forward=fwd)
            else:
                self.file_data.set_eeg_reference(ref_channels=self.references)
            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error has occurred during the computation of the re-referencing."
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()

    def compute_source_space(self):
        """
        Compute the source space of the "fsaverage" model.
        :return: The source space
        :rtype: MNE.SourceSpaces
        """
        print("Compute source space")
        if self.read_files:
            src = read_source_spaces(self.file_path + "-src.fif", verbose=False)
        else:
            src = setup_source_space(subject=self.subject, spacing='oct6', add_dist='patch', subjects_dir=self.subjects_dir,
                                     n_jobs=self.n_jobs, verbose=False)
        if self.write_files:
            write_source_spaces(self.file_path + "-src.fif", src, overwrite=True, verbose=False)
        return src

    def compute_bem_solution(self):
        """
        Compute the BEM solution of the "fsaverage" model.
        :return: The BEM solution.
        :rtype: MNE.ConductorModel
        """
        print("Compute bem solution")
        if self.read_files:
            bem = read_bem_solution(self.file_path + "-bem-sol.fif", verbose=False)
        else:
            conductivity = (0.3, 0.006, 0.3)  # for three layers
            model = make_bem_model(subject=self.subject, ico=4, conductivity=conductivity, subjects_dir=self.subjects_dir,
                                   verbose=False)
            bem = make_bem_solution(model, verbose=False)
        if self.write_files:
            write_bem_solution(self.file_path + "-bem-sol.fif", bem, overwrite=True, verbose=False)
        return bem

    def compute_forward_solution(self, src, bem):
        """
        Compute the forward solution of the given data, based on the source space model of the "fsaverage" model.
        :param src: The source space
        :type src: MNE.SourceSpaces
        :param bem: The BEM solution.
        :type bem: MNE.ConductorModel
        :return: The forward solution.
        :rtype: MNE.Forward
        """
        print("Compute forward solution")
        if self.read_files:
            fwd = read_forward_solution(self.file_path + "-fwd.fif", verbose=False)
        else:
            fwd = make_forward_solution(self.file_data.info, trans='fsaverage', src=src, bem=bem, meg=False, eeg=True,
                                        mindist=5.0, n_jobs=self.n_jobs, verbose=False)
        if self.write_files:
            write_forward_solution(self.file_path + "-fwd.fif", fwd, overwrite=True, verbose=False)
        return fwd

    """
    Getters
    """
    def get_file_data(self):
        """
        Get the file data.
        :return: MNE data of the dataset.
        :rtype: MNE.Epochs/MNE.Raw
        """
        return self.file_data

    def get_references(self):
        """
        Get the references on which the data has been re-referenced.
        :return: The references
        :rtype: str/list of str
        """
        return self.references

    def get_save_data(self):
        """
        Get the boolean indicating if the data must be saved.
        :return: True if the data must be saved, False otherwise.
        :rtype: bool
        """
        return self.write_files

    def get_load_data(self):
        """
        Get the boolean indicating if the data must be loaded.
        :return: True if the data must be loaded, False otherwise.
        :rtype: bool
        """
        return self.read_files

    def get_n_jobs(self):
        """
        Get the number of jobs used for the computation.
        :return: The number of jobs.
        :rtype: int
        """
        return self.n_jobs


# ICA Decomposition
class icaWorkerSignals(QObject):
    """
    Contain the signals used by the ICA Decomposition runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class icaRunnable(QRunnable):
    def __init__(self, ica_method, file_data):
        """
        Runnable for the computation of the ICA decomposition of the given data.
        :param ica_method: Method used for performing the ICA decomposition
        :type ica_method: str
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        """
        super().__init__()
        self.signals = icaWorkerSignals()
        self.ica_method = ica_method
        self.file_data = deepcopy(file_data)

    def run(self):
        """
        Launch the computation of the ICA decomposition on the given data.
        Notifies the main model that the computation is finished.
        """
        try:
            ica = ICA(method=self.ica_method)
            ica.fit(self.file_data)
            ica.apply(self.file_data)
            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error as occurred during the computation of the ICA."
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()

    """
    Getters
    """
    def get_file_data(self):
        """
        Get the file data.
        :return: MNE data of the dataset.
        :rtype: MNE.Epochs/MNE.Raw
        """
        return self.file_data

    def get_ica_method(self):
        """
        Gets the method used for the ICA decomposition.
        :return: Method used for performing the ICA decomposition
        :return: str
        """
        return self.ica_method


# Extract Epochs
class extractEpochsWorkerSignals(QObject):
    """
    Contain the signals used by the extract epochs runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class extractEpochsRunnable(QRunnable):
    def __init__(self, file_data, events, event_ids, tmin, tmax, trials_selected):
        """
        Runnable for the computation of the extraction of the epochs of the given data.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param events: The events from which the epochs will be extracted.
        :type events: list of, list of int
        :param event_ids: The event ids
        :type event_ids: dict
        :param tmin: Start time of the epoch to keep
        :type tmin: float
        :param tmax: End time of the epoch to keep
        :type tmax: float
        :param trials_selected: The indexes of the trials selected for the computation
        :type trials_selected: list of int
        """
        super().__init__()
        self.signals = extractEpochsWorkerSignals()

        self.file_data = file_data
        self.events = events
        self.event_ids = event_ids
        self.tmin = tmin
        self.tmax = tmax
        self.trials_selected = trials_selected

    def run(self):
        """
        Launch the computation of the extraction of the epochs on the given data.
        Notifies the main model that the computation is finished.
        """
        try:
            self.file_data = Epochs(self.file_data, events=self.events, event_id=self.event_ids, tmin=self.tmin,
                                    tmax=self.tmax, preload=True)
            self.transform_file_data_with_trials_selected()
            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error has occurred during the epoch extraction"
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()

    def transform_file_data_with_trials_selected(self):
        """
        Create a mask to know which trial to keep and which one to remove for the computation.
        Apply this mask on the data to keep only the trials/epochs selected by the user.
        """
        mask = [True for _ in range(len(self.file_data.events))]
        for i in self.trials_selected:
            mask[i] = False
        self.file_data.drop(mask)

    """
    Getters
    """
    def get_file_data(self):
        """
        Get the file data.
        :return: MNE data of the dataset.
        :rtype: MNE.Epochs/MNE.Raw
        """
        return self.file_data


# SNR
class signalToNoiseRatioWorkerSignals(QObject):
    """
    Contain the signals used by the source estimation runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class signalToNoiseRatioRunnable(QRunnable):
    def __init__(self, file_data, snr_methods, source_method, file_path, read_files, write_files, picks, trials_selected):
        """
        Runnable for the computation of the SNR of the given data.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param snr_methods:
        :type snr_methods:
        :param source_method: The method used to compute the source estimation
        :type source_method: str
        :param file_path: The path to the file
        :type file_path: str
        :param write_files: Boolean telling if the data computed must be saved into files.
        :type write_files: bool
        :param read_files: Boolean telling if the data used for the computation can be read from computer files.
        :type read_files: bool
        :param picks: The channels to take into account in the computation.
        :type picks: list of str
        :param trials_selected: The indexes of the trials selected for the computation
        :type trials_selected: list of int
        """
        super().__init__()
        self.signals = signalToNoiseRatioWorkerSignals()

        self.file_data = deepcopy(file_data)
        self.snr_methods = snr_methods
        self.source_method = source_method
        self.file_path = file_path
        self.read_files = read_files
        self.write_files = write_files
        self.picks = picks
        self.trials_selected = trials_selected
        self.subject = "fsaverage"
        self.subjects_dir = get_project_freesurfer_path()

        self.SNRs = []

    def run(self):
        """
        Launch the computation of the SNR
        Notifies the main model when the computation is finished.
        Notifies the main model when an error occurs.
        """
        try:
            mask = self.create_mask_from_indexes_to_keep()
            self.file_data = self.file_data.drop(mask)
            self.compute_all_SNRs()
            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error as occurred during the computation of the SNR."
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()

    def compute_all_SNRs(self):
        """
        Launch all the SNR methods selected by the user.
        """
        if "Mean-Std" in self.snr_methods:
            self.SNRs.append(self.SNR_mean_std())
        if "Sample Correlation Coefficient" in self.snr_methods:
            self.SNRs.append(self.SNR_sample_correlation_coefficient())
        if "Maximum Likelihood" in self.snr_methods:
            self.SNRs.append(self.SNR_maximum_likelihood_estimate())
        if "Amplitude" in self.snr_methods:
            self.SNRs.append(self.SNR_amplitude())
        if "Plus-Minus Averaging" in self.snr_methods:
            self.SNRs.append(self.SNR_plus_minus_averaging())
        if "Response Repetition" in self.snr_methods:
            self.SNRs.append(self.SNR_response_repetition())
        if "MNE Source" in self.snr_methods:
            self.SNRs.append(self.SNR_mne_source())
        if "MNE Frequency" in self.snr_methods:
            self.SNRs.append(self.SNR_mne_frequency())
        self.pretty_print_SNRs(self.SNRs)
        # for i in range(len(self.SNRs)):
        #    self.SNRs[i] = np.mean(self.SNRs[i])

    # Mean Std
    @staticmethod
    def SNR_mean_std_computation(a, axis=0, ddof=0):
        """
        This function comes from an old release of SciPy (version 0.14.0, currently version 1.7.1).
        It is not implemented anymore in Scipy.
        Link : https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.signaltonoise.html
        ---
        The signal-to-noise ratio of the input data.
        Returns the signal-to-noise ratio of 'a', here defined as the mean
        divided by the standard deviation.
        :param a: An ndarray object containing the sample data.
        :type a: ndarray
        :param axis: If axis is equal to None, the array is first ravel'd. If axis is an integer, this is the axis over
        which to operate. Default is 0.
        :type axis: int or None, optional
        :param ddof: Degrees of freedom correction for standard deviation. Default is 0.
        :type ddof: int, optional
        :return: s2n, The mean to standard deviation ratio(s) along `axis`, or 0 where the standard deviation is 0.
        :rtype: ndarray
        """
        m = a.mean(axis)
        sd = a.std(axis=axis, ddof=ddof)
        # ~ SNRs = np.where(sd == 0, 0, m/sd)
        SNRs = np.where(sd == 0, 0, 10 * np.log10((m ** 2) / (sd ** 2)))
        return SNRs

    def SNR_mean_std(self, axis=1, ddof=0):
        """
        Take the data from the Epoch file, average it and give the data to the computation.
        :param axis: If axis is equal to None, the array is first ravel'd. If axis is an integer, this is the axis over
        which to operate. Default is 0.
        :type axis: int or None, optional
        :param ddof: Degrees of freedom correction for standard deviation. Default is 0.
        :type ddof: int, optional
        :return: SNR_estimate
        :rtype: int
        """
        data = self.file_data.average().get_data(picks=self.picks)
        return self.SNR_mean_std_computation(data, axis=axis, ddof=ddof)

    # Correlation Coefficient
    @staticmethod
    def SNR_sample_correlation_coefficient_computation(a, b):
        """
        Paper : Signal to noise ratio and response variability measurements in single trial evoked potentials.
        Link : https://doi.org/10.1016/0013-4694(78)90267-5
        ---
        The signal-to-noise ratio of the input data based on the sample correlation between successive trials.
        Returns the signal-to-noise ratio of 'a' and 'b'
        :param a: An ndarray object containing the sample data.
        :type a: ndarray
        :param b: An ndarray object containing the sample data.
        :type b: ndarray
        :return: SNR_estimate
        :rtype: int
        """
        N = a.size
        r = (np.cov(a, b)[0][1]) / ((np.var(a) * np.var(b)) ** 0.5)
        A = np.exp(-2 / (N - 3))
        B = -0.5 * (1 - A)
        SNR_estimate = A * (r / (1 - r)) + B
        return SNR_estimate

    def SNR_sample_correlation_coefficient(self):
        """
        Compute the average of the SNR of epochs.
        :return: SNR_estimate
        :rtype: int
        """
        data = self.file_data.get_data(picks=self.picks)
        data_shape = data.shape
        SNRs = np.empty(data_shape[1])
        for i in range(data_shape[1]):  # Each channel
            snr = []
            for j in range(0, data_shape[0], 2):  # Pairs of trials
                if j + 1 < data_shape[0]:  # Avoid taking an element with no pair (end of the array).
                    snr.append(self.SNR_sample_correlation_coefficient_computation(data[j][i], data[j + 1][i]))
            SNRs[i] = np.mean(snr)
        return SNRs

    # Maximum Likelihood
    @staticmethod
    def SNR_maximum_likelihood_estimate_computation(a, b):
        """
        Paper : Signal to noise ratio and response variability measurements in single trial evoked potentials
        Link : https://doi.org/10.1016/0013-4694(78)90267-5
        ---
        The signal-to-noise ratio of the input data based on the maximum likelihood estimate between successive trials
        Returns the signal-to-noise ratio of 'a' and 'b'
        Parameters
        ----------
        :param a: An ndarray object containing the sample data.
        :type a: ndarray
        :param b: An ndarray object containing the sample data.
        :type b: ndarray
        :return: SNR_estimate
        :rtype: int
        """
        sum_of_squared_difference = np.sum(np.subtract(a, b) ** 2)
        SNR_estimate = 2 * np.dot(a, b) / sum_of_squared_difference
        return SNR_estimate

    def SNR_maximum_likelihood_estimate(self):
        """
        Take the data from the Epoch file, average it and give the data to the computation.
        :return: SNR_estimate
        :rtype: int
        """
        data = self.file_data.get_data(picks=self.picks)
        data_shape = data.shape
        SNRs = np.empty(data_shape[1])
        for i in range(data_shape[1]):  # Each channel
            snr = []
            for j in range(0, data_shape[0], 2):  # Pairs of trials
                if j + 1 < data_shape[0]:  # Avoid taking an element with no pair (end of the array).
                    snr.append(self.SNR_maximum_likelihood_estimate_computation(data[j][i], data[j + 1][i]))
            SNRs[i] = np.mean(snr)
        return SNRs

    # Amplitude
    @staticmethod
    def SNR_amplitude_computation(a, axis=0):
        """
        Link : https://www.sciencedirect.com/science/article/pii/S105381190901297X#
        :param a: An ndarray object containing the sample data.
        :type a: ndarray
        :param axis: If axis is equal to None, the array is first ravel'd. If axis is an integer, this is the axis over
        which to operate. Default is 0.
        :type axis: int or None, optional
        :return: SNR_estimate
        :rtype: int
        """
        data_shape = a.shape
        mean = np.mean(a, axis=axis)
        SNRs = np.empty(data_shape[0])
        for i in range(data_shape[0]):  # Each channel
            signal_amplitude = 0
            for j in range(data_shape[1]):  # Each time stamp
                value = abs(a[i][j] - mean[i])
                if value > signal_amplitude:
                    signal_amplitude = value
            noise = np.std(a[i])

            # ~ SNRs[i] = signal_amplitude/noise
            SNRs[i] = 10 * np.log10((signal_amplitude ** 2) / (noise ** 2))
        return SNRs

    def SNR_amplitude(self, axis=1):
        """
        Take the data from the Epoch file, average it and give the data to the computation.
        :param axis: If axis is equal to None, the array is first ravel'd. If axis is an integer, this is the axis over
        which to operate. Default is 0.
        :type axis: int or None, optional
        :return: SNR_estimate
        :rtype: int
        """
        evoked = self.file_data.average(picks=self.picks)
        data = evoked.data
        return self.SNR_amplitude_computation(data, axis=axis)

    # Plus Minus Averaging
    def SNR_plus_minus_averaging_computation(self, data, axis=0):
        """
        Links : https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/iet-spr.2016.0528
                https://link.springer.com/content/pdf/10.1007/BF02522949.pdf
        :param data: An ndarray object containing the sample data.
        :type data: ndarray
        :param axis: If axis is equal to None, the array is first ravel'd. If axis is an integer, this is the axis over
        which to operate. Default is 0.
        :type axis: int or None, optional
        :return: SNR_estimate
        :rtype: int
        """
        data_shape = data.shape
        signal_mean = np.mean(data, axis=axis)
        noise = data - signal_mean
        noise_mean = np.mean(noise, axis=axis)

        special_average = np.zeros((data_shape[1], data_shape[2]))
        for i in range(data_shape[0]):
            if i % 2 == 0:
                special_average += data[i]
            else:
                special_average -= data[i]
        special_average /= data_shape[0]

        signal_final = self.mean_squared(signal_mean, axis=axis + 1) - self.mean_squared(special_average, axis=axis + 1)
        noise_final = self.mean_squared(noise_mean, axis=axis + 1) - self.mean_squared(special_average, axis=axis + 1)

        SNR = signal_final / noise_final
        # ~ SNR = 10*np.log10((signal_final**2)/(noise_final**2))
        return SNR

    def SNR_plus_minus_averaging(self, axis=0):
        """
        Take the data from the Epoch file give it to the computation.
        :param axis: If axis is equal to None, the array is first ravel'd. If axis is an integer, this is the axis over
        which to operate. Default is 0.
        :type axis: int or None, optional
        :return: SNR_estimate
        :rtype: int
        """
        data = self.file_data.get_data(picks=self.picks)
        return self.SNR_plus_minus_averaging_computation(data, axis=axis)

    # Response Repetitions
    @staticmethod
    def SNR_response_repetition_computation(data, axis=0):
        """
        Link : https://github.com/nipy/nitime/blob/master/nitime/analysis/snr.py
        :param data: An ndarray object containing the sample data.
        :type data: ndarray
        :param axis: If axis is equal to None, the array is first ravel'd. If axis is an integer, this is the axis over
        which to operate. Default is 0.
        :type axis: int or None, optional
        :return: SNR_estimate
        :rtype: int
        """
        signal_mean = np.mean(data, axis=axis)
        noise = data - signal_mean

        frequencies, signal_mean_psd = welch(signal_mean, fs=100, nfft=2048, noverlap=0, nperseg=None,
                                             window='boxcar', scaling='spectrum')

        all_noise_psd = np.empty((noise.shape[0], noise.shape[1], signal_mean_psd.shape[1]))
        for i in range(noise.shape[0]):
            _, noise_psd = welch(noise[0], fs=100, nfft=2048, noverlap=0, nperseg=None,
                                 window='boxcar', scaling='spectrum')
            all_noise_psd[i] = noise_psd

        signal_psd = np.mean(signal_mean_psd, axis=1)
        noise_psd = np.mean(all_noise_psd, axis=(0, 2))
        SNRs = 10 * np.log10(signal_psd / noise_psd)
        return SNRs

    def SNR_response_repetition(self, axis=0):
        """
        Take the data from the Epoch file give it to the computation.
        :param axis: If axis is equal to None, the array is first ravel'd. If axis is an integer, this is the axis over
        which to operate. Default is 0.
        :type axis: int or None, optional
        :return: SNR_estimate
        :rtype: int
        """
        data = self.file_data.get_data(picks=self.picks)
        return self.SNR_response_repetition_computation(data, axis=axis)

    # MNE Frequency
    @staticmethod
    def SNR_mne_frequency_computation(psd, noise_n_neighbor_freqs=1, noise_skip_neighbor_freqs=1):
        """
        Link : https://mne.tools/stable/auto_tutorials/time-freq/50_ssvep.html#sphx-glr-auto-tutorials-time-freq-50-ssvep-py
        -----
        Compute SNR spectrum from PSD spectrum using convolution.
        ----------
        :param psd: Data object containing PSD values. Works with arrays as produced by
                MNE's PSD functions or channel/trial subsets.
        :type psd: ndarray, shape ([n_trials, n_channels,] n_frequency_bins)
        :param noise_n_neighbor_freqs: Number of neighboring frequencies used to compute noise level.
                increment by one to add one frequency bin ON BOTH SIDES
        :type noise_n_neighbor_freqs: int
        :param noise_skip_neighbor_freqs: set this >=1 if you want to exclude the immediately neighboring
                frequency bins in noise level calculation
        :type noise_skip_neighbor_freqs: int
        :return: Array containing SNR for all epochs, channels, frequency bins.
                NaN for frequencies on the edges, that do not have enough neighbors on
                one side to calculate SNR.
        :rtype: ndarray, shape ([n_trials, n_channels,] n_frequency_bins)
        """
        # Construct a kernel that calculates the mean of the neighboring
        # frequencies
        averaging_kernel = np.concatenate((np.ones(noise_n_neighbor_freqs),
                                           np.zeros(2 * noise_skip_neighbor_freqs + 1),
                                           np.ones(noise_n_neighbor_freqs)))
        averaging_kernel /= averaging_kernel.sum()

        # Calculate the mean of the neighboring frequencies by convolving with the
        # averaging kernel.
        mean_noise = np.apply_along_axis(
            lambda PSD_: np.convolve(PSD_, averaging_kernel, mode='valid'),
            axis=-1, arr=psd
        )

        # The mean is not defined on the edges so we will pad it with nas. The
        # padding needs to be done for the last dimension only so we set it to
        # (0, 0) for the other ones.
        edge_width = noise_n_neighbor_freqs + noise_skip_neighbor_freqs
        pad_width = [(0, 0)] * (mean_noise.ndim - 1) + [(edge_width, edge_width)]
        mean_noise = np.pad(mean_noise, pad_width=pad_width, constant_values=np.nan)

        return psd / mean_noise

    def SNR_mne_frequency(self):
        """
        Compute the power spectral density to give it to the SNR computation.
        :return: SNR_estimate
        :rtype: int
        """
        fmin = 1.
        fmax = 50.
        sfreq = self.file_data.info['sfreq']
        tmin = round(self.file_data.times[0], 3)
        tmax = round(self.file_data.times[-1], 3)

        PSDs, freqs = psd_welch(self.file_data, n_fft=int(sfreq * (tmax - tmin)), n_overlap=0, n_per_seg=None,
                                tmin=tmin, tmax=tmax, fmin=fmin, fmax=fmax, window='boxcar',
                                picks=self.picks, verbose=False)
        SNRs = self.SNR_mne_frequency_computation(PSDs)

        plot = False
        if plot:
            self.plot_SNR_mne_frequency(PSDs, freqs, SNRs, fmin, fmax)

        SNRs_without_NaN = SNRs[:, :, 2:-2]
        SNRs_mean = np.mean(SNRs_without_NaN, axis=(0, 2))

        return SNRs_mean

    @staticmethod
    def plot_SNR_mne_frequency(PSDs, freqs, SNRs, fmin, fmax):
        fig, axes = plt.subplots(2, 1, sharex='all', sharey='none', figsize=(8, 5))
        freq_range = range(np.where(np.floor(freqs) == 1.)[0][0],
                           np.where(np.ceil(freqs) == fmax - 1)[0][0])

        PSDs_plot = 10 * np.log10(PSDs)
        PSDs_mean = PSDs_plot.mean(axis=(0, 1))[freq_range]
        PSDs_std = PSDs_plot.std(axis=(0, 1))[freq_range]
        axes[0].plot(freqs[freq_range], PSDs_mean, color='b')
        axes[0].fill_between(
            freqs[freq_range], PSDs_mean - PSDs_std, PSDs_mean + PSDs_std,
            color='b', alpha=.2)
        axes[0].set(title="PSD spectrum", ylabel='Power Spectral Density [dB]')

        # SNR spectrum
        SNR_mean = SNRs.mean(axis=(0, 1))[freq_range]
        SNR_std = SNRs.std(axis=(0, 1))[freq_range]

        axes[1].plot(freqs[freq_range], SNR_mean, color='r')
        axes[1].fill_between(
            freqs[freq_range], SNR_mean - SNR_std, SNR_mean + SNR_std,
            color='r', alpha=.2)
        axes[1].set(
            title="SNR spectrum", xlabel='Frequency [Hz]',
            ylabel='SNR', ylim=[-2, 30], xlim=[fmin, fmax])
        fig.show()
        input("Press enter to continue.")

    # MNE source
    def SNR_mne_source(self):
        """
        Link : https://mne.tools/stable/auto_examples/inverse/source_space_snr.html
        Compute the source estimate to estimated the SNR from it.
        :return: SNR_estimate
        :rtype: int
        """
        self.file_data.apply_baseline()
        self.file_data.set_eeg_reference(projection=True)
        evoked = self.file_data.average()

        if self.write_files:
            inv = self.create_inverse()
        else:  # Read it
            inv = read_inverse_operator(self.file_path + "-inv.fif", verbose=False)

        plot = False
        if plot:
            plot_snr_estimate(evoked, inv, verbose=False)
        else:
            return self.compute_estimate_SNR(evoked, inv)

    def compute_estimate_SNR(self, evoked, inv):
        print("Compute estimate SNR")

        fwd = read_forward_solution(self.file_path + "-fwd.fif", verbose=False)
        noise_cov = read_cov(self.file_path + "-cov.fif", verbose=False)
        snr = 3.0
        lambda2 = 1.0 / snr ** 2
        stc = apply_inverse(evoked, inv, lambda2, method=self.source_method, pick_ori="normal", verbose=False)
        snr_stc = stc.estimate_snr(evoked.info, fwd, noise_cov, verbose=False)
        SNR_mean = np.mean(snr_stc.data)
        return SNR_mean

    def create_inverse(self):
        noise_cov = self.compute_noise_covariance()
        src = self.compute_source_space()
        bem = self.compute_bem_solution()
        fwd = self.compute_forward_solution(src, bem)
        inv = self.compute_inverse_operator(fwd, noise_cov)
        return inv

    def compute_noise_covariance(self):
        print("Compute noise covariance")
        noise_cov = compute_covariance(self.file_data, tmax=0., method=['shrunk', 'empirical'], verbose=False)
        if self.write_files:
            noise_cov.save(self.file_path + "-cov.fif")
        return noise_cov

    def compute_source_space(self):
        print("Compute source space")
        src = setup_source_space(self.subject, spacing='oct6', add_dist='patch', subjects_dir=self.subjects_dir, verbose=False)
        if self.write_files:
            write_source_spaces(self.file_path + "-src.fif", src, overwrite=True, verbose=False)
        return src

    def compute_bem_solution(self):
        print("Compute bem solution")
        conductivity = (0.3, 0.006, 0.3)  # for three layers
        model = make_bem_model(subject=self.subject, ico=4, conductivity=conductivity, subjects_dir=self.subjects_dir, verbose=False)
        bem = make_bem_solution(model, verbose=False)
        if self.write_files:
            write_bem_solution(self.file_path + "-bem-sol.fif", bem, overwrite=True, verbose=False)
        return bem

    def compute_forward_solution(self, src, bem):
        print("Compute forward solution")
        fwd = make_forward_solution(self.file_data.info, trans='fsaverage', src=src, bem=bem, meg=False, eeg=True, mindist=5.0, n_jobs=1,
                                    verbose=False)
        if self.write_files:
            write_forward_solution(self.file_path + "-fwd.fif", fwd, overwrite=True, verbose=False)
        return fwd

    def compute_inverse_operator(self, fwd, noise_cov):
        print("Compute inverse operator")
        inverse_operator = make_inverse_operator(self.file_data.info, fwd, noise_cov, loose=0.2, depth=0.8, verbose=False)
        if self.write_files:
            write_inverse_operator(self.file_path + "-inv.fif", inverse_operator, verbose=False)
        return inverse_operator

    """
    Utils
    """
    @staticmethod
    def mean_squared(data, axis=0):
        return np.mean(data ** 2, axis=axis)

    def root_mean_squared(self, data, axis=0):
        return np.sqrt(self.mean_squared(data, axis=axis))

    def create_mask_from_indexes_to_keep(self):
        """
        Create a mask to know which trial to keep and which one to remove for the computation.
        :return mask: Mask of trials to remove. True means remove, and False means keep.
        :rtype mask: list of boolean
        """
        mask = [True for _ in range(len(self.file_data.events))]
        for i in self.trials_selected:
            mask[i] = False
        return mask

    def pretty_print_SNRs(self, SNRs, all_methods=False, means=True):
        if all_methods:
            print("=====\nAll methods complete SNRs :\n")
            for i in range(len(SNRs)):
                print(self.snr_methods[i] + " SNRs : " + str(SNRs[i]), end="\n\n")
        if means:
            print("=====\nAll methods means :\n")
            for i in range(len(SNRs)):
                print(self.snr_methods[i] + " : " + str(np.mean(SNRs[i])))
        print("=====")

    def get_SNRs(self):
        """
        Get the SNRs computed over the data.
        :return: The SNRs computed over the data.
        :rtype: list of, list of float
        """
        return self.SNRs

    def get_SNR_methods(self):
        """
        Get the SNR methods used for the computation.
        :return: SNR methods
        :rtype: list of str
        """
        return self.snr_methods


# Source Estimation
class sourceEstimationWorkerSignals(QObject):
    """
    Contain the signals used by the source estimation runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class sourceEstimationRunnable(QRunnable):
    def __init__(self, source_estimation_method, file_data, file_path, write_files, read_files, epochs_method, trials_selected,
                 tmin, tmax, n_jobs, export_path):
        """
        Runnable for the computation of the source estimation of the given data.
        :param source_estimation_method: The method used to compute the source estimation
        :type source_estimation_method: str
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param file_path: The path to the file
        :type file_path: str
        :param write_files: Boolean telling if the data computed must be saved into files.
        :type write_files: bool
        :param read_files: Boolean telling if the data used for the computation can be read from computer files.
        :type read_files: bool
        :param epochs_method: On what data the source estimation will be computed. Can be three values :
        - "single trial" : Compute the source estimation on a single trial that is precised.
        - "evoked" : Compute the source estimation on the average of all the signals.
        - "averaged" : Compute the source estimation on every trial, and then compute the average of them.
        :type: str
        :param trials_selected: The indexes of the trials selected for the computation
        :type trials_selected: list of int
        :param tmin: Start time of the epoch or raw file
        :type tmin: float
        :param tmax: End time of the epoch or raw file
        :type tmax: float
        :param n_jobs: Number of processes used to compute the source estimation
        :type n_jobs: int
        :param export_path: Path where the source estimation data will be stored.
        :type export_path: str
        """
        super().__init__()
        self.signals = sourceEstimationWorkerSignals()
        self.source_estimation_method = source_estimation_method
        self.file_data = deepcopy(file_data)
        self.file_path = file_path
        self.read_files = read_files
        self.write_files = write_files
        self.epochs_method = epochs_method
        self.tmin = tmin
        self.tmax = tmax
        self.trials_selected = trials_selected
        self.n_jobs = n_jobs
        self.export_path = export_path
        self.subject = "fsaverage"
        self.subjects_dir = get_project_freesurfer_path()

        self.source_estimation_data = None

    def run(self):
        """
        Launch the computation of the source estimation.
        Notifies the main model when the computation is finished.
        If it is tried to load the source space information file, but that those file does not exist yet, an error message
        is displayed describing the error.
        If to extreme parameters are given and the computation fails, an error message is displayed describing the error.
        Notifies the main model when an error occurs.
        """
        try:
            self.source_estimation_data = self.mne_source_estimation_computation()
            self.check_data_export()
            self.signals.finished.emit()
        except FileNotFoundError as error:
            error_message = "An error as occurred during the computation of the source estimation. \n" \
                            "You can not load source estimation data if it has not been computed and saved earlier."
            detailed_message = str(error)
            error_window = errorWindow(error_message, detailed_message)
            error_window.show()
            self.signals.error.emit()
        except Exception as error:
            error_message = "An error as occurred during the computation of the source estimation."
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()

    """
    Source estimation methods
    """
    def mne_source_estimation_computation(self):
        """
        Launch the computation of the source space if it is not provided.
        Once the source space is computed, compute the source estimation on this source space and the given data.
        :return: The source estimation of the evoked response of the data.
        :rtype: MNE.SourceEstimate
        """
        self.file_data.apply_baseline()
        self.file_data.set_eeg_reference(projection=True)
        if self.tmin is not None and self.tmax is not None:
            if self.tmin is None:
                self.tmin = self.file_data.times[0]
            if self.tmax is None:
                self.tmax = self.file_data.times[-1]
            self.file_data = self.file_data.crop(tmin=self.tmin, tmax=self.tmax)

        if self.read_files:
            inv = read_inverse_operator(self.file_path + "-inv.fif", verbose=False)
        else:
            inv = self.create_inverse_operator()
        stc = self.compute_source_estimation_on_selected_data(inv)
        return stc

    def compute_source_estimation_on_selected_data(self, inv):
        """
        Call the correct method for applying the inverse operator on the desired signals of the given data.s
        :param inv: The inverse operator.
        :type inv: MNE.InverseOperator
        :return: The source estimation of the evoked response of the data.
        :rtype: MNE.SourceEstimate
        """
        stc = None
        if self.epochs_method == "single_trial":
            stc = self.compute_inverse_single_trial(inv)
        elif self.epochs_method == "evoked":
            stc = self.compute_inverse_evoked(inv)
        elif self.epochs_method == "averaged":
            stc = self.compute_inverse_averaged(inv)
        return stc

    def compute_inverse_single_trial(self, inv):
        """
        Apply the inverse operator on a single signal of the given data.
        :param inv: The inverse operator.
        :type inv: MNE.InverseOperator
        :return: The source estimation of the evoked response of the data.
        :rtype: MNE.SourceEstimate
        """
        print("Apply inverse on a single signal of data")
        epoch = self.file_data[self.trials_selected[0]]
        evoked = self.file_data.average()
        snr = 3.0
        lambda2 = 1.0 / snr ** 2
        stc = apply_inverse_epochs(epoch, inv, lambda2, method=self.source_estimation_method, pick_ori="normal",
                                   nave=evoked.nave, verbose=False)[0]
        return stc

    def compute_inverse_evoked(self, inv):
        """
        Apply the inverse operator on the evoked signal of the given data.
        :param inv: The inverse operator.
        :type inv: MNE.InverseOperator
        :return: The source estimation of the evoked response of the data.
        :rtype: MNE.SourceEstimate
        """
        print("Apply inverse on evoked data")
        mask = self.create_mask_from_indexes_to_keep()
        data = self.file_data.drop(mask)
        evoked = data.average()
        snr = 3.0
        lambda2 = 1.0 / snr ** 2
        stc = apply_inverse(evoked, inv, lambda2, method=self.source_estimation_method, pick_ori="normal", verbose=False)
        return stc

    def compute_inverse_averaged(self, inv):
        """
        Apply the inverse operator on all the signals of the given data and then average to give the final result.
        :param inv: The inverse operator.
        :type inv: MNE.InverseOperator
        :return: The source estimation of the evoked response of the data.
        :rtype: MNE.SourceEstimate
        """
        print("Apply inverse on all data averaged")
        mask = self.create_mask_from_indexes_to_keep()
        data = self.file_data.drop(mask)
        evoked = data.average()
        snr = 3.0
        lambda2 = 1.0 / snr ** 2
        stcs = apply_inverse_epochs(data, inv, lambda2, method=self.source_estimation_method, pick_ori="normal",
                                    nave=evoked.nave, verbose=False)
        mean_stc = sum(stcs) / len(stcs)
        return mean_stc

    def create_inverse_operator(self):
        """
        Launch all the necessary computation to compute the inverse operator.
        :return: The inverse operator.
        :rtype: MNE.InverseOperator
        """
        print("Compute all data necessary for creating inverse\n===============================================")
        noise_cov = self.compute_noise_covariance()
        src = self.compute_source_space()
        bem = self.compute_bem_solution()
        fwd = self.compute_forward_solution(src, bem)
        inv = self.compute_inverse_operator(fwd, noise_cov)
        return inv

    def compute_noise_covariance(self):
        """
        Compute the noise covariance of the given data.
        :return: The noise covariance.
        :rtype: MNE.Covariance
        """
        print("Compute noise covariance")
        noise_cov = compute_covariance(self.file_data, tmax=0., method=['shrunk', 'empirical'], n_jobs=self.n_jobs, verbose=False)
        if self.write_files:
            noise_cov.save(self.file_path + "-cov.fif")
        return noise_cov

    def compute_source_space(self):
        """
        Compute the source space of the "fsaverage" model.
        :return: The source space
        :rtype: MNE.SourceSpaces
        """
        print("Compute source space")
        src = setup_source_space(subject=self.subject, spacing='oct6', add_dist='patch', subjects_dir=self.subjects_dir,
                                 n_jobs=self.n_jobs, verbose=False)
        if self.write_files:
            write_source_spaces(self.file_path + "-src.fif", src, overwrite=True, verbose=False)
        return src

    def compute_bem_solution(self):
        """
        Compute the BEM solution of the "fsaverage" model.
        :return: The BEM solution.
        :rtype: MNE.ConductorModel
        """
        print("Compute bem solution")
        conductivity = (0.3, 0.006, 0.3)  # for three layers
        model = make_bem_model(subject=self.subject, ico=4, conductivity=conductivity, subjects_dir=self.subjects_dir,
                               verbose=False)
        bem = make_bem_solution(model, verbose=False)
        if self.write_files:
            write_bem_solution(self.file_path + "-bem-sol.fif", bem, overwrite=True, verbose=False)
        return bem

    def compute_forward_solution(self, src, bem):
        """
        Compute the forward solution of the given data, based on the source space model of the "fsaverage" model.
        :param src: The source space
        :type src: MNE.SourceSpaces
        :param bem: The BEM solution.
        :type bem: MNE.ConductorModel
        :return: The forward solution.
        :rtype: MNE.Forward
        """
        print("Compute forward solution")
        fwd = make_forward_solution(self.file_data.info, trans='fsaverage', src=src, bem=bem, meg=False, eeg=True,
                                    mindist=5.0, n_jobs=self.n_jobs, verbose=False)
        if self.write_files:
            write_forward_solution(self.file_path + "-fwd.fif", fwd, overwrite=True, verbose=False)
        return fwd

    def compute_inverse_operator(self, fwd, noise_cov):
        """
        Compute the inverse operator of the given data, based on the forward solution and the noise covariance previously
        computed.
        :param fwd: The forward solution.
        :type fwd: MNE.Forward
        :param noise_cov: The noise covariance.
        :type noise_cov: MNE.Covariance
        :return: The inverse operator.
        :rtype: MNE.InverseOperator
        """
        print("Compute inverse operator")
        inverse_operator = make_inverse_operator(self.file_data.info, fwd, noise_cov, loose=0.2, depth=0.8,
                                                 verbose=False)
        if self.write_files:
            write_inverse_operator(self.file_path + "-inv.fif", inverse_operator, verbose=False)
        return inverse_operator

    """
    Others
    """
    def create_mask_from_indexes_to_keep(self):
        """
        Create a mask to know which trial to keep and which one to remove for the computation.
        :return mask: Mask of trials to remove. True means remove, and False means keep.
        :rtype mask: list of boolean
        """
        mask = [True for _ in range(len(self.file_data.events))]
        for i in self.trials_selected:
            mask[i] = False
        return mask

    def check_data_export(self):
        """
        Check if the source estimation data must be exported.
        If it is the case, create the file and write the data in it.
        """
        if self.export_path is not None:
            data = self.source_estimation_data.data
            times = self.source_estimation_data.times

            file = open(self.export_path + ".txt", "x")
            # Write header
            file.write("Time")
            for i in range(len(data)):
                file.write(", Dipole " + str(i+1))
            file.write("\n")
            # Write data
            for i in range(len(times)):     # Times
                file.write(str(times[i]))
                for j in range(len(data)):  # Dipoles
                    file.write(", " + str(data[j][i]))
                file.write("\n")
            file.close()

    """
    Getters
    """
    def get_source_estimation_data(self):
        """
        Get the source estimation data.
        :return: The source estimation of the evoked response of the data.
        :rtype: MNE.SourceEstimate
        """
        return self.source_estimation_data
