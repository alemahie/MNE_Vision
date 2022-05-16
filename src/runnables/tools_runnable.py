#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools runnable
"""

from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

from mne import make_forward_solution, write_forward_solution, compute_covariance, setup_source_space, \
    write_source_spaces, make_bem_model, make_bem_solution, write_bem_solution, Epochs
from mne.minimum_norm import read_inverse_operator, make_inverse_operator, apply_inverse, \
                             write_inverse_operator
from mne.preprocessing import ICA

from utils.error_window import errorWindow
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


class filterRunnable(QRunnable):
    def __init__(self, low_frequency, high_frequency, channels_selected, file_data):
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
        """
        super().__init__()
        self.signals = filterWorkerSignals()
        self.low_frequency = low_frequency
        self.high_frequency = high_frequency
        self.channels_selected = channels_selected
        self.file_data = file_data

    def run(self):
        """
        Launch the computation of the filtering on the given data.
        Notifies the main model that the computation is finished.
        """
        self.file_data.filter(l_freq=self.low_frequency, h_freq=self.high_frequency, picks=self.channels_selected)
        self.signals.finished.emit()

    def get_file_data(self):
        """
        Get the file data.
        :return: MNE data of the dataset.
        :rtype: MNE.Epochs/MNE.Raw
        """
        return self.file_data


# Resampling
class resamplingWorkerSignals(QObject):
    """
    Contain the signals used by the resampling runnable.
    """
    finished = pyqtSignal()


class resamplingRunnable(QRunnable):
    def __init__(self, frequency, file_data):
        """
        Runnable for the computation of the resampling of the given data.
        :param frequency: The new frequency at which the data will be resampled.
        :type frequency: int
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        """
        super().__init__()
        self.signals = filterWorkerSignals()
        self.frequency = frequency
        self.file_data = file_data

    def run(self):
        """
        Launch the computation of the resampling on the given data.
        Notifies the main model that the computation is finished.
        """
        old_frequency = self.file_data.info.get("sfreq")
        new_frequency = self.frequency
        self.file_data.resample(new_frequency)

        number_of_frames = len(self.file_data.times)
        self.file_data.events[0][0] *= (new_frequency/old_frequency)
        for i in range(1, len(self.file_data.events)):
            self.file_data.events[i][0] = self.file_data.events[i-1][0] + number_of_frames

        self.signals.finished.emit()

    def get_file_data(self):
        """
        Get the file data.
        :return: MNE data of the dataset.
        :rtype: MNE.Epochs/MNE.Raw
        """
        return self.file_data


# Re-referencing
class reReferencingWorkerSignals(QObject):
    """
    Contain the signals used by the re-referencing runnable.
    """
    finished = pyqtSignal()


class reReferencingRunnable(QRunnable):
    def __init__(self, references, file_data, n_jobs):
        """
        Runnable for the computation of the re-referencing of the given data.
        :param references: References from which the data will be re-referenced. Can be a single or multiple channels;
        Can be an average of all channels; Can be a "point to infinity".
        :type references: list of str; str
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param n_jobs: Number of parallel processes used to compute the re-referencing
        :type n_jobs: int
        """
        super().__init__()
        self.signals = filterWorkerSignals()
        self.references = references
        self.file_data = file_data
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
        if self.references == "infinity":
            src = self.compute_source_space()
            bem = self.compute_bem_solution()
            fwd = self.compute_forward_solution(src, bem)
            self.file_data.set_eeg_reference('REST', forward=fwd)
        else:
            self.file_data.set_eeg_reference(ref_channels=self.references)
        self.signals.finished.emit()

    def compute_source_space(self):
        """
        Compute the source space of the "fsaverage" model.
        :return: The source space
        :rtype: MNE.SourceSpaces
        """
        print("Compute source space")
        src = setup_source_space(subject=self.subject, spacing='oct6', add_dist='patch', subjects_dir=self.subjects_dir,
                                 n_jobs=self.n_jobs, verbose=False)
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


# ICA Decomposition
class icaWorkerSignals(QObject):
    """
    Contain the signals used by the ICA Decomposition runnable.
    """
    finished = pyqtSignal()


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
        self.file_data = file_data

    def run(self):
        """
        Launch the computation of the ICA decomposition on the given data.
        Notifies the main model that the computation is finished.
        """
        ica = ICA(method=self.ica_method)
        ica.fit(self.file_data)
        self.signals.finished.emit()

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


# Extract Epochs
class extractEpochsWorkerSignals(QObject):
    """
    Contain the signals used by the extract epochs runnable.
    """
    finished = pyqtSignal()


class extractEpochsRunnable(QRunnable):
    def __init__(self, file_data, events, tmin, tmax):
        """
        Runnable for the computation of the extraction of the epochs of the given data.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param events: The events from which the epochs will be extracted.
        :type events: list of, list of int
        :param tmin: Start time of the epoch to keep
        :type tmin: float
        :param tmax: End time of the epoch to keep
        :type tmax: float
        """
        super().__init__()
        self.signals = extractEpochsWorkerSignals()

        self.file_data = file_data
        self.events = events
        self.tmin = tmin
        self.tmax = tmax

    def run(self):
        """
        Launch the computation of the extraction of the epochs on the given data.
        Notifies the main model that the computation is finished.
        """
        self.file_data = Epochs(self.file_data, self.events, tmin=self.tmin, tmax=self.tmax, preload=True)
        self.signals.finished.emit()

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


# Source Estimation
class sourceEstimationWorkerSignals(QObject):
    """
    Contain the signals used by the source estimation runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


class sourceEstimationRunnable(QRunnable):
    def __init__(self, source_estimation_method, file_data, file_path, write_files, read_files, n_jobs):
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
        :param n_jobs: Number of processes used to computed the source estimation
        :type n_jobs: int
        """
        super().__init__()
        self.signals = sourceEstimationWorkerSignals()
        self.source_estimation_method = source_estimation_method
        self.file_data = file_data
        self.file_path = file_path
        self.read_files = read_files
        self.write_files = write_files
        self.n_jobs = n_jobs
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
            detailed_message = str(error)
            error_window = errorWindow(error_message, detailed_message)
            error_window.show()
            self.signals.error.emit()

    def mne_source_estimation_computation(self):
        """
        Launch the computation of the source space if it is not provided.
        Once the source space is computed, compute the source estimation on this source space and the given data.
        :return: The source estimation of the evoked response of the data.
        :rtype: MNE.SourceEstimate
        """
        self.file_data.apply_baseline()
        self.file_data.set_eeg_reference(projection=True)
        if self.read_files:
            inv = read_inverse_operator(self.file_path + "-inv.fif", verbose=False)
        else:
            inv = self.create_inverse_operator()
        stc = self.compute_inverse(inv)
        return stc

    def compute_inverse(self, inv):
        """
        Apply the inverse operator on the given data.
        :param inv: The inverse operator.
        :type inv: MNE.InverseOperator
        :return: The source estimation of the evoked response of the data.
        :rtype: MNE.SourceEstimate
        """
        print("Apply inverse")
        evoked = self.file_data.average()
        snr = 3.0
        lambda2 = 1.0 / snr ** 2
        stc = apply_inverse(evoked, inv, lambda2, method=self.source_estimation_method, pick_ori="normal", verbose=False)
        return stc

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
    Getters
    """
    def get_source_estimation_data(self):
        """
        Get the source estimation data.
        :return: The source estimation of the evoked response of the data.
        :rtype: MNE.SourceEstimate
        """
        return self.source_estimation_data
