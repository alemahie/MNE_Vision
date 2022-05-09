#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Connectivity runnable
"""

from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

from mne import compute_covariance, setup_source_space, write_source_spaces, make_bem_model, make_bem_solution, \
    write_bem_solution, make_forward_solution, write_forward_solution, extract_label_time_course
from mne.minimum_norm import make_inverse_operator, write_inverse_operator, read_inverse_operator, apply_inverse_epochs
from mne_connectivity import envelope_correlation, spectral_connectivity_epochs

from utils.error_window import errorWindow
from utils.file_path_search import get_project_freesurfer_path, get_labels_from_subject

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class envelopeCorrelationWorkerSignals(QObject):
    finished = pyqtSignal()


class envelopeCorrelationRunnable(QRunnable):
    def __init__(self, file_data):
        super().__init__()
        self.signals = envelopeCorrelationWorkerSignals()

        self.file_data = file_data
        self.envelope_correlation_data = None

    def run(self):
        correlation_data = envelope_correlation(self.file_data).combine()
        self.envelope_correlation_data = correlation_data.get_data(output="dense")[:, :, 0]
        self.signals.finished.emit()

    """
    Getters
    """
    def get_envelope_correlation_data(self):
        return self.envelope_correlation_data


class sourceSpaceConnectivityWorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal()


# noinspection PyUnresolvedReferences
class sourceSpaceConnectivityRunnable(QRunnable):
    def __init__(self, file_data, file_path, source_estimation_method, save_data, load_data, n_jobs):
        super().__init__()
        self.signals = sourceSpaceConnectivityWorkerSignals()

        self.file_data = file_data
        self.file_path = file_path
        self.source_estimation_method = source_estimation_method
        self.write_files = save_data
        self.read_files = load_data
        self.n_jobs = n_jobs
        self.subject = "fsaverage"
        self.subjects_dir = get_project_freesurfer_path()

        self.source_space_connectivity_data = None

    def run(self):
        try:
            correlation_data = self.compute_envelope_correlation_with_source_space()
            self.source_space_connectivity_data = correlation_data.get_data(output="dense")[:, :, 0]
            self.signals.finished.emit()
        except FileNotFoundError as error:
            error_message = "An error as occurred during the computation of the source space for the envelope correlation. \n" \
                            "You can not load source estimation data if it has not been computed and saved earlier."
            detailed_message = str(error)
            error_window = errorWindow(error_message, detailed_message)
            error_window.show()
            self.signals.error.emit()
        except Exception as error:
            error_message = "An error as occurred during the computation of the source space."
            detailed_message = str(error)
            error_window = errorWindow(error_message, detailed_message)
            error_window.show()
            self.signals.error.emit()

    """
    Utils
    """
    def compute_envelope_correlation_with_source_space(self):
        self.file_data.apply_baseline()
        self.file_data.set_eeg_reference(projection=True)
        if self.read_files:
            inv = read_inverse_operator(self.file_path + "-inv.fif", verbose=False)
        else:
            inv = self.create_inverse_operator()
        stcs = self.compute_inverse(inv)
        labels = get_labels_from_subject(self.subject, self.subjects_dir)
        label_ts = extract_label_time_course(stcs, labels, inv['src'], mode='mean_flip', return_generator=True)
        sfreq = self.file_data.info["sfreq"]
        correlation_data = spectral_connectivity_epochs(label_ts, method="pli", mode='multitaper', sfreq=sfreq,
                                                        faverage=True, mt_adaptive=True, n_jobs=self.n_jobs)
        return correlation_data

    """
    Source Space
    """
    def compute_inverse(self, inv):
        print("Apply inverse to epochs")
        snr = 1.0
        lambda2 = 1.0 / snr ** 2
        stcs = apply_inverse_epochs(self.file_data, inv, lambda2, method=self.source_estimation_method, pick_ori="normal",
                                    return_generator=True, verbose=False)
        return stcs

    def create_inverse_operator(self):
        print("Compute all data necessary for creating inverse\n===============================================")
        noise_cov = self.compute_noise_covariance()
        src = self.compute_source_space()
        bem = self.compute_bem_solution()
        fwd = self.compute_forward_solution(src, bem)
        inv = self.compute_inverse_operator(fwd, noise_cov)
        return inv

    def compute_noise_covariance(self):
        print("Compute noise covariance")
        noise_cov = compute_covariance(self.file_data, tmax=0., method=['shrunk', 'empirical'], n_jobs=self.n_jobs, verbose=False)
        if self.write_files:
            noise_cov.save(self.file_path + "-cov.fif")
        return noise_cov

    def compute_source_space(self):
        print("Compute source space")
        src = setup_source_space(subject=self.subject, spacing='oct6', add_dist='patch', subjects_dir=self.subjects_dir,
                                 n_jobs=self.n_jobs, verbose=False)
        if self.write_files:
            write_source_spaces(self.file_path + "-src.fif", src, overwrite=True, verbose=False)
        return src

    def compute_bem_solution(self):
        print("Compute bem solution")
        conductivity = (0.3, 0.006, 0.3)  # for three layers
        model = make_bem_model(subject=self.subject, ico=4, conductivity=conductivity, subjects_dir=self.subjects_dir,
                               verbose=False)
        bem = make_bem_solution(model, verbose=False)
        if self.write_files:
            write_bem_solution(self.file_path + "-bem-sol.fif", bem, overwrite=True, verbose=False)
        return bem

    def compute_forward_solution(self, src, bem):
        print("Compute forward solution")
        fwd = make_forward_solution(self.file_data.info, trans='fsaverage', src=src, bem=bem, meg=False, eeg=True,
                                    mindist=5.0, n_jobs=self.n_jobs, verbose=False)
        if self.write_files:
            write_forward_solution(self.file_path + "-fwd.fif", fwd, overwrite=True, verbose=False)
        return fwd

    def compute_inverse_operator(self, fwd, noise_cov):
        print("Compute inverse operator")
        inverse_operator = make_inverse_operator(self.file_data.info, fwd, noise_cov, loose=0.2, depth=0.8,
                                                 verbose=False)
        if self.write_files:
            write_inverse_operator(self.file_path + "-inv.fif", inverse_operator, verbose=False)
        return inverse_operator

    """
    Getters
    """
    def get_source_space_connectivity_data(self):
        return self.source_space_connectivity_data
