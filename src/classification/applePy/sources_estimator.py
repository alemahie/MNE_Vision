import os
import mne

import numpy as np


class Sources_estimator:
    def __init__(self, raw_dataset, info, tmin_noise, tmax_noise, trans=None, sourceSpaces=None, bemSolution=None,
                 mixedSourceSpaces=None, coregistration=None, loose=1, snr=3, fixed=False):
        self.raw_dataset = raw_dataset
        self.info = info
        self.tmin_noise = tmin_noise
        self.tmax_noise = tmax_noise
        self.trans = trans
        self.sourceSpaces = sourceSpaces
        self.bemSolution = bemSolution
        self.mixedSourceSpaces = mixedSourceSpaces
        self.coregistration = coregistration
        self.loose = loose
        self.snr = snr
        self.fixed = fixed

        self.sources_log = [("sources", True), ("coregistration", coregistration), ("loose", loose), ("snr", snr),
                            ('fixed', fixed)]

    def apply_common_average(self):
        """
        Applies a common average reference if not already applied.
        Raw_dataset format must be : subjects x conditions x epochsEEGLAB
        Raw_dataset must be an array.
        """
        for person_idx in range(self.raw_dataset.shape[0]):
            for condition_idx in range(self.raw_dataset[person_idx].shape[0]):
                self.raw_dataset[person_idx][condition_idx].set_eeg_reference('average', projection=True)
                self.raw_dataset[person_idx][condition_idx].apply_proj()

    def open_make_forward_solutions(self):
        """
        Opens the forward solution parts from the default files or the specified files.
        Then, creates the forward solution from the three previously opened parts.
        """
        if self.sourceSpaces is None:
            path = os.path.join(sources_files, 'fsaverage-oct6-src.fif')
            self.sources_log.append(("source spaces", path))
            self.sourceSpaces = mne.read_source_spaces(path)
        else:
            try:
                self.sources_log.append(("source spaces", self.sourceSpaces))
                self.sourceSpaces = mne.read_source_spaces(self.sourceSpaces)
            except:
                print("Invalid file " + self.sourceSpaces + ". Default will be used")
                path = os.path.join(sources_files, 'fsaverage-oct6-src.fif')
                self.sources_log.append(("source spaces", path))
                self.sourceSpaces = mne.read_source_spaces(path)

        if self.bemSolution is None:
            path = os.path.join(sources_files, 'fsaverage-bem-sol.fif')
            self.sources_log.append(("bem solution", path))
            self.bemSolution = mne.read_bem_solution(path)
        else:
            try:
                self.sources_log.append(("bem solution", self.bemSolution))
                self.bemSolution = mne.read_bem_solution(self.bemSolution)
            except:
                print("Invalid file " + self.sourceSpaces + ". Default will be used")
                path = os.path.join(sources_files, 'fsaverage-bem-sol.fif')
                self.sources_log.append(("bem solution", path))
                self.bemSolution = mne.read_bem_solution(path)

        if self.mixedSourceSpaces is None:
            path = os.path.join(sources_files, 'fsaverage-oct6-mixed-src.fif')
            self.sources_log.append(("mixed source spaces", path))
            self.mixedSourceSpaces = mne.read_source_spaces(path)
        else:
            try:
                self.sources_log.append(("mixed source spaces", self.mixedSourceSpaces))
                self.mixedSourceSpaces = mne.read_source_spaces(self.mixedSourceSpaces)
            except:
                print("Invalid file " + self.sourceSpaces + ". Default will be used")
                path = os.path.join(sources_files, 'fsaverage-oct6-mixed-src.fif')
                self.sources_log.append(("mixed source spaces", path))
                self.mixedSourceSpaces = mne.read_source_spaces(path)

        if self.coregistration is not None:
            try:
                self.coregistration = mne.read_trans(self.coregistration)
            except:
                print("Invalid file " + self.sourceSpaces + ". None will be used.")
        forwardSolution = mne.make_forward_solution(self.info, self.coregistration, self.mixedSourceSpaces,
                                                    self.bemSolution, mindist=5.0, n_jobs=4)
        return forwardSolution

    def compute_noise_covariances(self):
        """
        Computes the noise covariances for the raw data.
        Raw_dataset format must be : subjects x conditions x epochsEEGLAB
        The limits of the noise must be provided.
        """
        noise_covariances = []
        temp = [sbj.tolist() for sbj in self.raw_dataset]
        dataset = []
        for subject in temp:
            dataset.append(mne.concatenate_epochs(subject))
        dataset = np.asarray(dataset)

        for subject in dataset:
            noise_covariances.append(mne.compute_covariance(subject, tmin=self.tmin_noise, tmax=self.tmax_noise))
        noise_covariances = np.asarray(noise_covariances)

        return noise_covariances

    def create_inverse_operator(self, forwardSolution, noise_covariances, depth, fixed):
        """
        Calls the inverse operator method from mne with the chosen arguments. Returns the inverse operator.
        """
        inverse_operators = []
        for subject_covariance in noise_covariances:
            inverseOperator = mne.minimum_norm.make_inverse_operator(self.info, forwardSolution, subject_covariance,
                                                                     self.loose, depth, fixed)
            inverse_operators.append(inverseOperator)
        inverse_operators = np.asarray(inverse_operators)
        return inverse_operators

    def save_sources(self, inverse_operators):
        """
        Computes the sources for all subjects and conditions. Default estimated snr is 3.
        Raw_dataset format must be : subjects x conditions x epochsEEGLAB
        """
        lambda2 = 1.0 / self.snr ** 2

        for person_idx in range(self.raw_dataset.shape[0]):
            for condition_idx in range(self.raw_dataset[person_idx].shape[0]):
                computed_source = mne.minimum_norm.apply_inverse_epochs(self.raw_dataset[person_idx][condition_idx],
                                                                        inverse_operators[person_idx], lambda2=lambda2,
                                                                        method="sLORETA", pick_ori=None)

                # np.save("subject"+str(person_idx)+"_"+str(condition_idx), computed_source)

    @staticmethod
    def create_labels():
        labelsParc = mne.read_labels_from_annot('fsaverage', parc='aparc')
        return labelsParc

    def extract_labels_from_sources(self, labelsParc, inverseOperator):
        labeled_dataset = [[] for i in range(self.raw_dataset.shape[0])]
        for person_idx in range(self.raw_dataset.shape[0]):
            for condition_idx in range(self.raw_dataset[person_idx].shape[0]):
                sources_person = np.load("subject" + str(person_idx) + "_" + str(condition_idx))
                extracted = mne.extract_label_time_course(sources_person, labelsParc, inverseOperator["src"],
                                                          mode='mean', allow_empty=True)
                np.save("subject" + str(person_idx) + "_" + str(condition_idx) + "_labels.npy", extracted)
                labeled_dataset[person_idx].append(extracted)
            labeled_dataset[person_idx] = np.asarray(labeled_dataset[person_idx])
        labeled_dataset = np.asarray(labeled_dataset)

        labelsAseg = mne.get_volume_labels_from_src(inverseOperator['src'], 'fsaverage',
                                                    '/usr/local/freesurfer/subjects')
        labels = labelsParc + labelsAseg
        np.save("labels.npy", labels)
        return labels, labeled_dataset

    def estimate_sources(self):
        """
        Call all the above methods in order to estimate the sources on the dataset.
        """
        self.apply_common_average()
        forward_solution = self.open_make_forward_solutions()
        noise_covariances = self.compute_noise_covariances()
        inverse_operator = self.create_inverse_operator(forward_solution, noise_covariances, depth=None, fixed=False)
        self.save_sources(inverse_operator)
        labelsParc = self.create_labels()
        labels, labeled_dataset = self.extract_labels_from_sources(labelsParc, inverse_operator)

        print("Sources estimated successfully")
        return labels, labeled_dataset
