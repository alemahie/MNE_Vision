#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools runnable
"""

from PyQt6.QtCore import QRunnable, pyqtSignal, QObject

from mne import make_forward_solution, write_forward_solution, compute_covariance, setup_source_space, \
                write_source_spaces, make_bem_model, make_bem_solution, write_bem_solution
from mne.minimum_norm import read_inverse_operator, make_inverse_operator, apply_inverse, \
                             write_inverse_operator
from mne.preprocessing import ICA

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class icaWorkerSignals(QObject):
    finished = pyqtSignal()


class icaRunnable(QRunnable):
    def __init__(self, ica_method, file_data):
        super().__init__()
        self.signals = icaWorkerSignals()
        self.ica_method = ica_method
        self.file_data = file_data

    def run(self):
        ica = ICA(method=self.ica_method)
        ica.fit(self.file_data)
        self.signals.finished.emit()

    def get_file_data(self):
        return self.file_data


class sourceEstimationWorkerSignals(QObject):
    finished = pyqtSignal()


class sourceEstimationRunnable(QRunnable):
    def __init__(self, source_estimation_method, file_data, file_path, write_files, read_files, n_jobs):
        super().__init__()
        self.signals = sourceEstimationWorkerSignals()
        self.source_estimation_method = source_estimation_method
        self.file_data = file_data
        self.file_path = file_path
        self.read_files = read_files
        self.write_files = write_files
        self.n_jobs = n_jobs
        self.subject = "fsaverage"
        self.subjects_dir = "../../data/freesurfer/subjects/"

        self.source_estimation_data = None

    def run(self):
        self.source_estimation_data = self.mne_source_estimation_computation()
        self.signals.finished.emit()

    def mne_source_estimation_computation(self):
        self.file_data.apply_baseline()
        self.file_data.set_eeg_reference(projection=True)
        if self.read_files:
            inv = read_inverse_operator(self.file_path + "-inv.fif", verbose=False)
        else:
            inv = self.create_inverse_operator()
        stc = self.compute_inverse(inv)
        return stc

    def compute_inverse(self, inv):
        print("Apply inverse")
        evoked = self.file_data.average()
        snr = 3.0
        lambda2 = 1.0 / snr ** 2
        stc = apply_inverse(evoked, inv, lambda2, method=self.source_estimation_method, pick_ori="normal", verbose=False)
        return stc

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

    def get_source_estimation_data(self):
        return self.source_estimation_data
