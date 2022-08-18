#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Connectivity runnable
"""

from copy import deepcopy

from PyQt5.QtCore import QRunnable, pyqtSignal, QObject

from mne import compute_covariance, setup_source_space, write_source_spaces, make_bem_model, make_bem_solution, \
    write_bem_solution, make_forward_solution, write_forward_solution, extract_label_time_course
from mne.minimum_norm import make_inverse_operator, write_inverse_operator, read_inverse_operator, apply_inverse_epochs
from mne_connectivity import envelope_correlation, spectral_connectivity_epochs, phase_slope_index

from utils.view.error_window import errorWindow
from utils.file_path_search import get_project_freesurfer_path, get_labels_from_subject

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


# Envelope Correlation
class envelopeCorrelationWorkerSignals(QObject):
    """
    Contain the signals used by the envelope correlation runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


# noinspection PyUnresolvedReferences
class envelopeCorrelationRunnable(QRunnable):
    def __init__(self, file_data, psi, fmin, fmax, connectivity_method, n_jobs, export_path):
        """
        Runnable for the computation of the envelope correlation of the dataset.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param psi: Check if the computation of the Phase Slope Index must be done. The PSI give an indication to the
        directionality of the connectivity.
        :type psi: bool
        :param fmin: Minimum frequency from which the envelope correlation will be computed.
        :type fmin: float
        :param fmax: Maximum frequency from which the envelope correlation will be computed.
        :type fmax: float
        :param connectivity_method: Method used for computing the source space connectivity.
        :type connectivity_method: str
        :param n_jobs: Number of processes used to compute the source estimation
        :type n_jobs: int
        :param export_path: Path where the envelope correlation data will be stored.
        :type export_path: str
        """
        super().__init__()
        self.signals = envelopeCorrelationWorkerSignals()

        self.file_data = deepcopy(file_data)
        self.psi = psi
        self.fmin = fmin
        self.fmax = fmax
        self.connectivity_method = connectivity_method
        self.n_jobs = n_jobs
        self.export_path = export_path

        self.envelope_correlation_data = None
        self.psi_data = None

    def run(self):
        """
        Launch the computation of the envelope correlation on the given data.
        Notifies the main model that the computation is finished.
        """
        try:
            self.compute_correlation_data()
            if self.psi:
                correlation_data = phase_slope_index(self.file_data, fmin=self.fmin, fmax=self.fmax)
                self.psi_data = correlation_data.get_data(output="dense")[:, :, 0]
            self.check_data_export()
            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error as occurred during the computation of the envelope correlation."
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()

    def compute_correlation_data(self):
        """
        Compute the correct correlation data depending on the method chosen by the user.
        """
        if self.connectivity_method == "envelope_correlation":

            correlation_data = envelope_correlation(self.file_data).combine()
            self.envelope_correlation_data = correlation_data.get_data(output="dense")[:, :, 0]
        else:
            sfreq = self.file_data.info["sfreq"]
            correlation_data = spectral_connectivity_epochs(self.file_data, method=self.connectivity_method, mode="multitaper",
                                                            sfreq=sfreq, fmin=self.fmin, fmax=self.fmax, faverage=True, mt_adaptive=True,
                                                            n_jobs=self.n_jobs)
            self.envelope_correlation_data = correlation_data.get_data(output="dense")[:, :, 0]

    def check_data_export(self):
        """
        Check if the envelope correlation data and the PSI must be exported.
        """
        if self.export_path is not None:
            data = self.envelope_correlation_data
            channels = self.file_data.ch_names
            self.save_data(data, channels, "-connectivity")
            if self.psi:
                data = self.psi_data
                self.save_data(data, channels, "-PSI")

    def save_data(self, data, channels, file_name):
        """
        If it is the case, create the file and write the data in it.
        :param data: The data to save, either the connectivity of PSI.
        :type data: list of, list of float
        :param channels: The channels names to save.
        :type channels: list of str
        :param file_name: The name of the data to save.
        :type file_name: str
        """
        print(data)
        file = open(self.export_path + file_name + ".txt", "x")
        # Write header
        for i in range(len(channels)):
            if i != len(channels) - 1:
                file.write(channels[i] + ", ")
            else:
                file.write(channels[i])
        file.write("\n")
        # Write data
        for i in range(len(data)):  # Channels 1
            for j in range(len(data)):  # Channels 2
                if j != len(data) - 1:
                    file.write(str(data[i][j]) + ", ")
                else:
                    file.write(str(data[i][j]))
            file.write("\n")
        file.close()

    """
    Getters
    """
    def get_envelope_correlation_data(self):
        """
        Get the envelope correlation's data.
        :return: The envelope correlation's data.
        :rtype: list of, list of float
        """
        return self.envelope_correlation_data

    def get_psi_data(self):
        """
        Get the psi's data.
        :return: The psi's data. Or nothing if the psi's data has not been computed.
        :rtype: list of, list of float
        """
        return self.psi_data


# Source Space Connectivity
class sourceSpaceConnectivityWorkerSignals(QObject):
    """
    Contain the signals used by the source space connectivity runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


# noinspection PyUnresolvedReferences
class sourceSpaceConnectivityRunnable(QRunnable):
    def __init__(self, file_data, file_path, connectivity_method, spectrum_estimation_method, source_estimation_method,
                 save_data, load_data, n_jobs, export_path, psi, fmin, fmax):
        """
        Runnable for the computation of the source space connectivity of the dataset.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param file_path: Path to the file.
        :type file_path: str
        :param connectivity_method: Method used for computing the source space connectivity.
        :type connectivity_method: str
        :param spectrum_estimation_method: Method used for computing the spectrum estimation used inside the computation
        of the source space connectivity.
        :type spectrum_estimation_method: str
        :param source_estimation_method: Method used for computing the source estimation used inside the computation of
        the source space connectivity.
        :type source_estimation_method: str
        :param save_data: Boolean telling if the data computed must be saved into files.
        :type save_data: bool
        :param load_data: Boolean telling if the data used for the computation can be read from computer files.
        :type load_data: bool
        :param n_jobs: Number of processes used to computed the source estimation
        :type n_jobs: int
        :param export_path: Path where the source space connectivity data will be stored.
        :type export_path: str
        :param psi: Check if the computation of the Phase Slope Index must be done. The PSI give an indication to the
        directionality of the connectivity.
        :type psi: bool
        :param fmin: Minimum frequency from which the envelope correlation will be computed.
        :type fmin: float
        :param fmax: Maximum frequency from which the envelope correlation will be computed.
        :type fmax: float
        """
        super().__init__()
        self.signals = sourceSpaceConnectivityWorkerSignals()

        self.file_data = file_data
        self.file_path = file_path
        self.connectivity_method = connectivity_method
        self.spectrum_estimation_method = spectrum_estimation_method
        self.source_estimation_method = source_estimation_method
        self.write_files = save_data
        self.read_files = load_data
        self.n_jobs = n_jobs
        self.export_path = export_path
        self.psi = psi
        self.fmin = fmin
        self.fmax = fmax
        self.subject = "fsaverage"
        self.subjects_dir = get_project_freesurfer_path()

        self.source_space_connectivity_data = None
        self.psi_data = None

    def run(self):
        """
        Launch the computation of the source space connectivity on the given data.
        Notifies the main model when the computation is finished.
        If it is tried to load the source space information file, but that those file does not exist yet, an error message
        is displayed describing the error.
        If to extreme parameters are given and the computation fails, an error message is displayed describing the error.
        Notifies the main model when an error occurs.
        """
        try:
            self.compute_envelope_correlation_with_source_space()
            self.check_data_export()
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
    def check_data_export(self):
        """
        Check if the source space connectivity data must be exported.
        If it is the case, create the file and write the data in it.
        """
        if self.export_path is not None:
            data = self.source_space_connectivity_data
            labels = get_labels_from_subject("fsaverage", get_project_freesurfer_path())
            label_names = [label.name for label in labels]

            file = open(self.export_path + ".csv", "x")
            # Write header
            for i in range(len(label_names)):
                if i != len(label_names)-1:
                    file.write(label_names[i] + ", ")
                else:
                    file.write(label_names[i])
            file.write("\n")
            # Write data
            for i in range(len(data)):     # Source space area 1
                for j in range(len(data)):  # Source space area 2
                    if j != len(data)-1:
                        file.write(str(data[i][j]) + ", ")
                    else:
                        file.write(str(data[i][j]))
                file.write("\n")
            file.close()

    def compute_envelope_correlation_with_source_space(self):
        """
        Launch the computation of the source space if it is not provided.
        Once the source space is computed, compute the envelope correlation on this source space, giving the source space
        connectivity of the given data.
        """
        self.file_data.apply_baseline()
        self.file_data.set_eeg_reference(projection=True)
        if self.read_files:
            inv = read_inverse_operator(self.file_path + "-inv.fif", verbose=False)
        else:
            inv = self.create_inverse_operator()
        stcs = self.compute_inverse(inv)

        labels = get_labels_from_subject(self.subject, self.subjects_dir)
        label_ts = extract_label_time_course(stcs, labels, inv['src'], mode='mean_flip', return_generator=False)

        sfreq = self.file_data.info["sfreq"]
        correlation_data = spectral_connectivity_epochs(label_ts, method=self.connectivity_method, mode=self.spectrum_estimation_method,
                                                        sfreq=sfreq, fmin=self.fmin, fmax=self.fmax, faverage=True, mt_adaptive=True,
                                                        n_jobs=self.n_jobs)
        self.source_space_connectivity_data = correlation_data.get_data(output="dense")[:, :, 0]

        if self.psi:
            directionality_data = phase_slope_index(label_ts, mode=self.spectrum_estimation_method, fmin=self.fmin, fmax=self.fmax)
            self.psi_data = directionality_data.get_data(output="dense")[:, :, 0]

    """
    Source Space
    """
    def compute_inverse(self, inv):
        """
        Apply the inverse operator on the given data.
        :param inv: The inverse operator.
        :type inv: MNE.InverseOperator
        :return: The source estimation of all epochs.
        :rtype: list of MNE.SourceEstimate
        """
        print("Apply inverse to epochs")
        snr = 1.0
        lambda2 = 1.0 / snr ** 2
        stcs = apply_inverse_epochs(self.file_data, inv, lambda2, method=self.source_estimation_method, pick_ori="normal",
                                    return_generator=True, verbose=False)
        return stcs

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
    def get_source_space_connectivity_data(self):
        """
        Get the source space connectivity's data.
        :return: The source space's data.
        :rtype: list of, list of float
        """
        return self.source_space_connectivity_data

    def get_psi_data(self):
        """
        Get the psi's data.
        :return: The psi's data. Or nothing if the psi's data has not been computed.
        :rtype: list of, list of float
        """
        return self.psi_data


# Sensor Space Connectivity
class sensorSpaceConnectivityWorkerSignals(QObject):
    """
    Contain the signals used by the sensor space connectivity runnable.
    """
    finished = pyqtSignal()
    error = pyqtSignal()


# noinspection PyUnresolvedReferences
class sensorSpaceConnectivityRunnable(QRunnable):
    def __init__(self, file_data, export_path):
        """
        Runnable for the computation of the sensor space connectivity of the dataset.
        :param file_data: MNE data of the dataset.
        :type file_data: MNE.Epochs/MNE.Raw
        :param export_path: Path where the sensor space connectivity data will be stored.
        :type export_path: str
        """
        super().__init__()
        self.signals = sensorSpaceConnectivityWorkerSignals()

        self.file_data = file_data
        self.export_path = export_path
        self.sensor_space_connectivity_data = None

    def run(self):
        """
        Launch the computation of the sensor space connectivity on the given data.
        Notifies the main model that the computation is finished.
        """
        try:
            sfreq = self.file_data.info["sfreq"]
            connectivity_data = spectral_connectivity_epochs(self.file_data, method='pli', mode='multitaper', sfreq=sfreq,
                                                             faverage=True,  mt_adaptive=False, n_jobs=1)
            self.sensor_space_connectivity_data = connectivity_data.get_data(output='dense')[:, :, 0]
            self.check_data_export()
            self.signals.finished.emit()
        except Exception as error:
            error_message = "An error as occurred during the computation of the sensor space connectivity."
            error_window = errorWindow(error_message, detailed_message=str(error))
            error_window.show()
            self.signals.error.emit()

    def check_data_export(self):
        """
        Check if the sensor space connectivity data must be exported.
        If it is the case, create the file and write the data in it.
        """
        if self.export_path is not None:
            data = self.sensor_space_connectivity_data
            channels = self.file_data.ch_names

            file = open(self.export_path + ".txt", "x")
            # Write header
            for i in range(len(channels)):
                if i != len(channels) - 1:
                    file.write(channels[i] + ", ")
                else:
                    file.write(channels[i])
            file.write("\n")
            # Write data
            for i in range(len(data)):  # Channels 1
                for j in range(len(data)):  # Channels 2
                    if j != len(data) - 1:
                        file.write(str(data[i][j]) + ", ")
                    else:
                        file.write(str(data[i][j]))
                file.write("\n")
            file.close()

    """
    Getters
    """
    def get_sensor_space_connectivity_data(self):
        """
        Get the sensor space connectivity's data.
        :return: The sensor space's data.
        :rtype: list of, list of float
        """
        return self.sensor_space_connectivity_data
