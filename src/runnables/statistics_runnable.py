#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Statistics runnable
"""

import numpy as np

from copy import deepcopy

from PyQt5.QtCore import QRunnable, pyqtSignal, QObject
from matplotlib import pyplot as plt

from mne import make_forward_solution, write_forward_solution, compute_covariance, setup_source_space, \
    write_source_spaces, make_bem_model, make_bem_solution, write_bem_solution, read_forward_solution, read_cov
from mne.minimum_norm import read_inverse_operator, make_inverse_operator, apply_inverse, write_inverse_operator
from mne.stats import ttest_ind_no_p
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


# SNR
class statisticsSnrSignals(QObject):
    """
    Contain the signals used by the source estimation runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class statisticsSnrRunnable(QRunnable):
    def __init__(self, file_data, snr_methods, source_method, file_path, read_files, write_files, picks, stats_first_variable,
                 stats_second_variable):
        """
        Runnable for the computation of the SNR and the statistics of the given data.
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
        :param stats_first_variable: The first independent variable on which the statistics must be computed (an event id)
        :type stats_first_variable: str
        :param stats_second_variable: The second independent variable on which the statistics must be computed (an event id)
        :type stats_second_variable: str
        """
        super().__init__()
        self.signals = statisticsSnrSignals()

        self.file_data = deepcopy(file_data)
        self.snr_methods = snr_methods
        self.source_method = source_method
        self.file_path = file_path
        self.read_files = read_files
        self.write_files = write_files
        self.picks = picks
        self.stats_first_variable = stats_first_variable
        self.stats_second_variable = stats_second_variable
        self.subject = "fsaverage"
        self.subjects_dir = get_project_freesurfer_path()

        self.SNRs = []
        self.first_SNRs = None
        self.second_SNRs = None
        self.t_values = []

    def run(self):
        """
        Launch the computation of the SNR
        Notifies the main model when the computation is finished.
        Notifies the main model when an error occurs.
        """
        try:
            # First independent variable
            file_data_save = deepcopy(self.file_data)
            mask = self.create_mask_from_variable_to_keep(self.stats_first_variable)
            self.file_data = self.file_data.drop(mask)
            self.compute_all_SNRs()
            self.first_SNRs = deepcopy(self.SNRs)
            # Second independent variable
            self.SNRs = []
            self.file_data = deepcopy(file_data_save)
            mask = self.create_mask_from_variable_to_keep(self.stats_second_variable)
            self.file_data = self.file_data.drop(mask)
            self.compute_all_SNRs()
            self.second_SNRs = deepcopy(self.SNRs)
            # Statistics
            for i in range(len(self.first_SNRs)):
                self.t_values.append(ttest_ind_no_p(self.first_SNRs[i], self.second_SNRs[i]))
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

    def create_mask_from_variable_to_keep(self, stats_variable):
        """
        Create a mask to know which trial to keep and which one to remove for the computation.
        :return mask: Mask of trials to remove. True means remove, and False means keep.
        :rtype mask: list of boolean
        """
        mask = [True for _ in range(len(self.file_data.events))]
        event_ids = self.file_data.event_id
        event_id_to_keep = event_ids[stats_variable]
        for i, event in enumerate(self.file_data.events):
            if event[2] == event_id_to_keep:        # 2 is the event id in the events
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

    def get_first_SNRs(self):
        """
        Get the SNRs computed over the first independent variable.
        :return: The SNRs computed over the first independent variable.
        :rtype: list of, list of float
        """
        return self.first_SNRs

    def get_second_SNRs(self):
        """
        Get the SNRs computed over the second independent variable.
        :return: The SNRs computed over the second independent variable.
        :rtype: list of, list of float
        """
        return self.second_SNRs

    def get_t_values(self):
        """
        Get the T-values computed over the SNRs of the two independent variables.
        :return: T-values computed over the SNRs of the two independent variables.
        :rtype: list of float
        """
        return self.t_values

    def get_SNR_methods(self):
        """
        Get the SNR methods used for the computation.
        :return: SNR methods
        :rtype: list of str
        """
        return self.snr_methods

