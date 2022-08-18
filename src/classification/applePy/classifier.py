import os
import math
import time

import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt

from copy import deepcopy

from scipy.stats import randint

from mne import Epochs, concatenate_epochs, read_epochs
from mne.io import read_raw_eeglab, read_epochs_eeglab
from mne.channels import make_standard_montage
from mne.event import find_events

from sklearn import metrics
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import KFold, LeaveOneOut, GroupKFold

from pyriemann.estimation import Covariances

from classification.applePy.channel_selection import ElectrodeSelection
from classification.applePy.pipeline_catalogue import Pipeline_catalogue
from classification.applePy.sources_estimator import Sources_estimator
from classification.applePy.cnn import CNN

CONST_MAX_1by1_ELECTRODES = 30
CONST_MAX_5by5_ELECTRODES = 50
CONST_DEFAULT_RANDOMIZEDSEARCH_NBITER = 10


class ApplePyClassifier(BaseEstimator, TransformerMixin):
    """
    Global class dealing with automated classification. Inherits BaseEstimator and TransformerMix, in order to make it adaptable to 
    other estimators from other libraries. This class contains :  \n
        - A pipeline catalogue with all the pipelines and the important information about the parameters to fit \n
        - All the predictions and the prediction probabilities for all pipelines \n
        - All the correct answers \n
        - All the scores, confusion matrices, precisions, recalls, and ROC infos for all matrices \n
        - The dataset and the labels, as well as source dataset  \n
        - The group indices \n
        - The eventual test dataset, labels and groups \n
    """

    def __init__(self, used_pipelines=None):
        self.classifier_log = []

        self.pipeline_catalogue = Pipeline_catalogue(used_pipelines)
        self.catalogue = self.pipeline_catalogue.catalogue
        self.parameters = self.pipeline_catalogue.parameters_to_fit
        self.predictions = {key: [] for key in list(self.catalogue.keys())}
        self.predictions_proba = {key: [] for key in list(self.catalogue.keys())}
        self.expected_answers = []

        self.scores = {key: [] for key in list(self.catalogue.keys())}
        self.scores_fold = {key: [] for key in list(self.catalogue.keys())}
        self.confusion_matrices = {key: [] for key in list(self.catalogue.keys())}
        self.precisions = {key: [] for key in list(self.catalogue.keys())}
        self.recalls = {key: [] for key in list(self.catalogue.keys())}
        self.roc_infos = {key: [] for key in list(self.catalogue.keys())}

        self.dataset = None
        self.labels = None
        self.dataset_sources = None
        self.labels_sources = None
        self.electrodes = None
        self.groups = None
        self.nb_subj = 1
        self.nb_paradigms = None
        self.vertices = None
        self.event_names = None

        self.test_dataset = []
        self.test_labels = []
        self.test_groups = []

    """
    Pipelines
    """
    def modify_add_pipeline(self, name, pipeline, parameters):
        """
        Modifies or adds a new pipeline to the catalogue. \n
        Parameters \n
        ---------- \n
        name :  string \n
                name of the pipeline \n
        pipeline :  instance of pipeline \n
                    the pipeline to be used \n
        parameters :    see doc for pipeline catalogue \n
                    the notation for the parameters to fit \n
        """
        new_pipeline = True
        if name in self.catalogue.keys():
            new_pipeline = False
        self.pipeline_catalogue.modify_add_pipeline(name, pipeline, parameters)
        if new_pipeline:
            self.predictions[name] = []
            self.predictions_proba[name] = []

    def delete_pipelines(self, pipeline_names):
        """
        Deletes a pipeline by calling the method from the pipeline catalogue.
        Additionally, deletes all occurences of the pipeline. \n
        Parameters \n
        ---------- \n 
        name :  string \n
                name of the pipeline \n
        """
        for name in pipeline_names:
            names = list(self.catalogue.keys())
            names.sort()
            if name not in names:
                text = "Pipeline " + name + " does not exist."
                raise Exception(text)

            self.pipeline_catalogue.delete_pipeline(name)

            del self.predictions[name]
            del self.predictions_proba[name]
            del self.scores[name]
            del self.scores_fold[name]
            del self.confusion_matrices[name]
            del self.precisions[name]
            del self.recalls[name]
            del self.roc_infos[name]

    def modify_parameters(self, name, parameters):
        """
        Modifies a pipeline's parameters by calling the method from the pipeline catalogue. \n
        Parameters \n
        ---------- \n
        name :  string \n
                name of the pipeline \n
        parameters :    see doc for pipeline catalogue \n 
                        the notation for the parameters to fit \n
        """
        self.pipeline_catalogue.modify_parameters(name, parameters)

    def restore(self):
        """
        Restores the classifier by restoring the predictions, predictions probabilities, expected answers, scores,
        confusion matrices, precisions, recalls and roc info
        """
        self.predictions = {key: [] for key in list(self.catalogue.keys())}
        self.predictions_proba = {key: [] for key in list(self.catalogue.keys())}
        self.expected_answers = []

        self.scores = {key: [] for key in list(self.catalogue.keys())}
        self.confusion_matrices = {key: [] for key in list(self.catalogue.keys())}
        self.precisions = {key: [] for key in list(self.catalogue.keys())}
        self.recalls = {key: [] for key in list(self.catalogue.keys())}
        self.roc_infos = {key: [] for key in list(self.catalogue.keys())}

    """
    File reading
    """
    def read_one_file(self, file_path, file_name, destination, bads=None, picks=None, filtering=(1, 45), tmin=0,
                      tmax=0.5, ICA=False, resample=False, baseline=None, event_ids=None, reference=None):
        """
        Reads one non pre-epoched (raw) set file and saves the result in a -epo.fif file. \n
        Parameters \n
        ---------- \n
        file_path : path to the file to be opened \n
        file_name : name of the file \n
        destination : path where the -epo.fif file will be saved \n
        bads : list of electrodes to be rejected \n
        picks : list of electrodes to be worked on \n
        filtering : tuple containing the higher and lower frequencies to filter the data \n 
        tmin, tmax : tmin, tmax for delimiting the epochs in time \n 
        ICA : Boolean, whether or not to apply Independent Component Analysis \n
        resample : boolean, whether or not to resample the data at 512 Hz \n
        baseline : the baseline to be applied to the data  \n
        event_ids : The id of the event to consider \n
        reference : the name of the reference to be applied to the data \n
        """
        print("Reading ", file_name)
        eeg = read_raw_eeglab(file_path, preload=True)
        if reference is not None:
            eeg.set_eeg_reference(reference, projection=False)
        if resample:
            eeg.resample(512, npad='auto')
        if filtering[0] is None:
            filtering[0] = eeg.info['highpass']
        if filtering[1] is None:
            filtering[1] = eeg.info['lowpass']
        eeg.filter(filtering[0], filtering[1])
        if filtering[0] < 50 and filtering[1] > 50:
            eeg.notch_filter(np.asarray([47.5, 50, 52.5]))
        try:
            events = find_events(eeg)
        except ValueError:
            print("Invalid events in ", file_name)
            raise Exception()

        eeg.drop_channels(eeg.info['bads'])
        if bads is not None:
            eeg.drop_channels(bads)
        if picks is not None:
            eeg.pick_channels(picks)
        if ICA:
            ica = ICA(method="extended-infomax", random_state=1)
            ica.fit(eeg)
            ica.plot_components(inst=eeg)
            ica.apply(eeg)
        epochs = Epochs(eeg, events, event_id=event_ids, tmin=tmin, tmax=tmax, baseline=baseline)
        file_name = file_name[:-4] + '-epo.fif'
        fname = os.path.join(destination, file_name)
        epochs.save(fname)

    def prepare_nonepoched_dataset(self, directory, nb_subj, tmin, tmax, bads=None, picks=None, filtering=[None, None],
                                   ICA=False, resample=False, baseline=None, event_ids=[None, None], reference=None):
        """
        Prepare a   subjects x epochs x channels x times     dataset from raw files  \n
        Parameters \n
        ---------- \n
        directory : the path to the directory containing the dataset \n
        nb_subj : the number of subjects to be considered \n
        tmin, tmax : tmin, tmax for delimiting the epochs in time \n
        bads : list of electrodes to be rejected \n
        picks : list of electrodes to be worked on \n
        filtering : tuple containing the higher and lower frequencies to filter the data \n
        tmin, tmax : tmin, tmax for delimiting the epochs in time \n
        ICA : Boolean, whether or not to apply Independent Component Analysis \n
        resample : boolean, whether or not to resample the data at 512 Hz \n
        baseline : the baseline to be applied to the data  \n
        event_ids : The id of the event to consider \n
        reference : the name of the reference to be applied to the data \n
        """

        # MNE loading parameters
        # montage = make_standard_montage("standard_1005")

        # Load raw EEG data
        # =================
        data_root_folder = directory
        paradigms = os.listdir(directory)
        # epoched_raw_eeg_dataset = [[] for _ in range(nb_subj)]
        # epoched_raw_eeg_sources = [[] for _ in range(nb_subj)]
        # labels = [[] for _ in range(nb_subj)]
        # labels_sources = [[] for _ in range(nb_subj)]
        file_names = []
        # epochs = []
        # groups = []

        directory_new = os.path.join(directory, "epoched")
        if not os.path.exists(directory_new):
            os.makedirs(directory_new)

        for label, paradigm in enumerate(paradigms):
            data_class_folder = os.path.join(data_root_folder, paradigm)
            epoched_data_class_folder = os.path.join(directory_new, paradigm)
            list_of_files = []
            list_of_dirs = []
            event_id = event_ids[label]
            for raw_eeg_file in os.listdir(data_class_folder):
                if ".set" in raw_eeg_file:
                    list_of_files.append(raw_eeg_file)
                if "directory" in raw_eeg_file:
                    list_of_dirs.append(raw_eeg_file)
            list_of_files.sort()
            list_of_dirs.sort()
            subject_i = 0
            if not os.path.exists(epoched_data_class_folder):
                os.makedirs(epoched_data_class_folder)

            for subject_i, raw_eeg_file in enumerate(list_of_files):
                raw_file_path = os.path.join(data_class_folder, raw_eeg_file)
                self.read_one_file(raw_file_path, raw_eeg_file, epoched_data_class_folder, bads, picks, filtering, tmin,
                                   tmax, ICA=ICA, resample=resample, baseline=baseline, event_ids=event_id,
                                   reference=reference)

            for subject_j, raw_eeg_dir in enumerate(list_of_dirs):
                raw_path_subject = os.path.join(data_class_folder, raw_eeg_dir)
                epoched_raw_path_subject = os.path.join(epoched_data_class_folder, raw_eeg_dir)
                if not os.path.exists(epoched_raw_path_subject):
                    os.makedirs(epoched_raw_path_subject)
                subject_files = []
                for raw_eeg_file in os.listdir(raw_path_subject):
                    if ".set" in raw_eeg_file:
                        subject_files.append(raw_eeg_file)
                    # nb_files = len(subject_files)
                if subject_i + subject_j < nb_subj:
                    file_names.append(raw_eeg_dir)
                    for raw_eeg_file in subject_files:
                        raw_file_path = os.path.join(raw_path_subject, raw_eeg_file)
                        self.read_one_file(raw_file_path, raw_eeg_file, epoched_raw_path_subject, bads, picks,
                                           filtering, tmin, tmax, ICA=ICA, resample=resample, baseline=baseline,
                                           event_ids=event_id, reference=reference)

    def read_all_files(self, directory, nb_subj=None, divided_dataset=True, tmin=0, tmax=0.5, bads=None, picks=None,
                       filtering=[None, None], pre_epoched=True, ICA=False, resample=False, baseline=None,
                       event_ids=[None, None], reference=None):
        """
        Create a   subjects x epochs x channels x times     dataset from epoched files. \n
        Parameters \n
        ---------- \n
        directory : the path to the directory containing the dataset \n
        nb_subj : the number of subjects to be considered \n
        divided_dataset : boolean; whether or not the dataset is divided by classes \n
        tmin, tmax : tmin, tmax for delimiting the epochs in time \n
        bads : list of electrodes to be rejected \n
        picks : list of electrodes to be worked on \n
        filtering : tuple containing the higher and lower frequencies to filter the data \n
        pre_epoched : boolean; whether or not the dataset has been pre-epoched \n 
        tmin, tmax : tmin, tmax for delimiting the epochs in time \n
        ICA : Boolean, whether or not to apply Independent Component Analysis \n
        resample : boolean, whether or not to resample the data at 512 Hz \n
        baseline : the baseline to be applied to the data  \n
        event_ids : The id of the event to consider \n
        reference : the name of the reference to be applied to the data \n
        """
        if nb_subj is None:
            nb_subj = self.count_subjects(directory)

        if pre_epoched and not divided_dataset:
            self.read_preepoched_oneFilePerSubj(directory, nb_subj, tmin, tmax, bads=bads, picks=picks,
                                                filtering=filtering, ICA=ICA, resample=resample, baseline=baseline,
                                                event_ids=event_ids, reference=None)
            return

        self.classifier_log.extend(
            [("directory", directory), ("nb of subjects", nb_subj), ("tmin", tmin), ("tmax", tmax), ("bads", bads),
             ("picks", picks), ("filtering", filtering), ('pre_epoched', pre_epoched), ('ICA', ICA),
             ('resample', resample), ('baseline', baseline), ('event_ids', event_ids), ('reference', reference)])
        # MNE loading parameters
        montage = make_standard_montage("standard_1005")

        if not pre_epoched:
            if divided_dataset:
                self.prepare_nonepoched_dataset(directory, nb_subj, tmin, tmax, bads=bads, picks=picks,
                                                filtering=filtering, ICA=ICA, resample=resample, baseline=baseline,
                                                event_ids=event_ids, reference=reference)
                # print("would have prepared")
            else:
                self.prepare_nonepoched_dataset_oneFilePerSubj(directory, nb_subj, tmin, tmax, bads=bads, picks=picks,
                                                               filtering=filtering, ICA=ICA, resample=resample,
                                                               baseline=baseline, event_ids=event_ids,
                                                               reference=reference)
            directory = os.path.join(directory, "epoched")

        # Load raw EEG data
        # =================

        data_root_folder = directory
        paradigms = os.listdir(directory)
        epoched_raw_eeg_dataset = [[] for _ in range(nb_subj)]
        epoched_raw_eeg_sources = [[] for _ in range(nb_subj)]
        labels = [[] for _ in range(nb_subj)]
        labels_sources = [[] for _ in range(nb_subj)]
        file_names = []
        # epochs = []
        groups = []
        enumerated_paradigms = enumerate(paradigms)
        self.nb_paradigms = len(paradigms)
        self.classifier_log.append(('nb of paradigms', self.nb_paradigms))

        for label, paradigm in enumerated_paradigms:
            event_id = event_ids[label]
            data_class_folder = os.path.join(data_root_folder, paradigm)
            list_of_files = []
            list_of_dirs = []
            for raw_eeg_file in os.listdir(data_class_folder):
                if (".set" in raw_eeg_file) or ("-epo.fif" in raw_eeg_file):
                    list_of_files.append(raw_eeg_file)
                if "directory" in raw_eeg_file:
                    list_of_dirs.append(raw_eeg_file)
            list_of_files.sort()
            list_of_dirs.sort()
            subject_i = -1
            for subject_i, raw_eeg_file in enumerate(list_of_files):
                if subject_i < nb_subj:
                    file_names.append(raw_eeg_file)
                    raw_file_path = os.path.join(data_class_folder, raw_eeg_file)
                    if pre_epoched:
                        epoched_eeg = read_epochs_eeglab(raw_file_path, montage=montage, event_id=event_id)
                        if reference is not None:
                            epoched_eeg.set_eeg_reference(reference, projection=False)
                        if filtering[0] is None:
                            filtering[0] = epoched_eeg.info['highpass']
                        if filtering[1] is None:
                            filtering[1] = epoched_eeg.info['lowpass']
                        epoched_eeg.filter(filtering[0], filtering[1])
                        if picks is not None:
                            epoched_eeg.pick_channels(picks)
                        epoched_eeg.crop(tmin=tmin, tmax=tmax)
                        if resample:
                            epoched_eeg.resample(512)
                    else:
                        epoched_eeg = read_epochs(
                            raw_file_path)  # not read_epochs_eeglab because it doesn't work for .fif, and because it's already preprocessed

                    epoched_sources = deepcopy(epoched_eeg)
                    epoched_data = epoched_eeg.get_data()

                    epoched_labels = np.zeros(epoched_data.shape[0], dtype=np.int) + label
                    epoched_labels_sources = label

                    epoched_raw_eeg_dataset[subject_i].append(epoched_data)
                    labels[subject_i].append(epoched_labels)

                    epoched_raw_eeg_sources[subject_i].append(epoched_sources)
                    labels_sources.append(epoched_labels_sources)

            for subject_j, raw_eeg_dir in enumerate(list_of_dirs):
                raw_path_subject = os.path.join(data_class_folder, raw_eeg_dir)
                subject_files = []
                for raw_eeg_file in os.listdir(raw_path_subject):
                    if (".set" in raw_eeg_file) or ("-epo.fif" in raw_eeg_file):
                        subject_files.append(raw_eeg_file)
                    nb_files = len(subject_files)
                if subject_i + subject_j + 1 < nb_subj:
                    file_names.append(raw_eeg_dir)
                    epoched_raw_eeg_dataset[subject_i + subject_j + 1].append([])
                    labels[subject_i + subject_j + 1].append([])
                    epoched_raw_eeg_sources[subject_i + subject_j + 1].append([])
                    for raw_eeg_file in subject_files:
                        raw_file_path = os.path.join(raw_path_subject, raw_eeg_file)
                        if pre_epoched:
                            epoched_eeg = read_epochs_eeglab(raw_file_path, montage=montage, event_id=event_id)
                            if reference is not None:
                                epoched_eeg.set_eeg_reference(reference, projection=False)
                            if filtering[0] is None:
                                filtering[0] = epoched_eeg.info['highpass']
                            if filtering[1] is None:
                                filtering[1] = epoched_eeg.info['lowpass']
                            epoched_eeg.filter(filtering[0], filtering[1])
                            if picks is not None:
                                epoched_eeg.pick_channels(picks)
                            epoched_eeg.crop(tmin=tmin, tmax=tmax)
                        else:
                            epoched_eeg = read_epochs(raw_file_path)

                        epoched_sources = deepcopy(epoched_eeg)
                        epoched_data = epoched_eeg.get_data()

                        epoched_labels = np.zeros(epoched_data.shape[0], dtype=np.int) + label
                        epoched_labels_sources = label
                        epoched_raw_eeg_dataset[subject_i + subject_j + 1][label].append(epoched_data)
                        labels[subject_i + subject_j + 1][label].append(epoched_labels)

                        epoched_raw_eeg_sources[subject_i + subject_j + 1][label].append(epoched_sources)
                        labels_sources.append(epoched_labels_sources)

                    if nb_files > 1:
                        epoched_raw_eeg_dataset[subject_i + subject_j + 1][label] = np.asarray(
                            np.concatenate(epoched_raw_eeg_dataset[subject_i + subject_j + 1][label]))
                        labels[subject_i + subject_j + 1][label] = np.asarray(
                            np.concatenate(labels[subject_i + subject_j + 1][label]))
                        epoched_raw_eeg_sources[subject_i + subject_j + 1][label] = concatenate_epochs(
                            epoched_raw_eeg_sources[subject_i + subject_j + 1][label])
                    else:
                        epoched_raw_eeg_dataset[subject_i + subject_j + 1][label] = np.asarray(
                            epoched_raw_eeg_dataset[subject_i + subject_j + 1][label][0])
                        labels[subject_i + subject_j + 1][label] = np.asarray(
                            labels[subject_i + subject_j + 1][label][0])
                        epoched_raw_eeg_sources[subject_i + subject_j + 1][label] = \
                            epoched_raw_eeg_sources[subject_i + subject_j + 1][label][0]

        for subject_i in range(len(epoched_raw_eeg_dataset)):
            if self.nb_paradigms == 2:
                first = epoched_raw_eeg_dataset[subject_i][0].shape[0]
                second = epoched_raw_eeg_dataset[subject_i][1].shape[0]
                minimum = min([first, second])
                epoched_raw_eeg_dataset[subject_i][0] = epoched_raw_eeg_dataset[subject_i][0][:minimum]
                epoched_raw_eeg_dataset[subject_i][1] = epoched_raw_eeg_dataset[subject_i][1][:minimum]
                labels[subject_i][0] = labels[subject_i][0][:minimum]
                labels[subject_i][1] = labels[subject_i][1][:minimum]
            epoched_raw_eeg_dataset[subject_i] = np.concatenate(np.asarray(epoched_raw_eeg_dataset[subject_i]), axis=0)
            for k in range(epoched_raw_eeg_dataset[subject_i].shape[0]):
                groups.append(subject_i)
            labels[subject_i] = np.concatenate(np.asarray(labels[subject_i]), axis=0)

            epoched_raw_eeg_sources = np.asarray(epoched_raw_eeg_sources)
            labels_sources = np.asarray(labels_sources)

        if picks is not None:
            electrodes = picks
        else:
            electrodes = epoched_raw_eeg_sources[0][0].info['ch_names']

        epoched_raw_eeg_dataset = np.asarray(epoched_raw_eeg_dataset)
        # labels_sources = np.asarray(labels_sources)
        labels = np.asarray(labels)
        self.dataset = epoched_raw_eeg_dataset
        self.dataset_sources = epoched_raw_eeg_sources
        self.labels = labels
        self.electrodes = electrodes
        self.groups = np.asarray(groups)
        self.vertices = []

        labs = np.concatenate(self.labels)
        unique, counts = np.unique(labs, return_counts=True)
        occurences = dict(zip(unique, counts))
        self.classifier_log.append(("occurences from each class : ", occurences))

    def read_preepoched_oneFilePerSubj(self, directory, nb_subj, tmin, tmax, bads=None, picks=None,
                                       filtering=[None, None], ICA=False, resample=False, baseline=None,
                                       event_ids=[None, None], reference=None):
        """
        Create a   subjects x epochs x channels x times     dataset from epoched files. \n
        Parameters \n
        ---------- \n
        directory : the path to the directory containing the dataset \n
        nb_subj : the number of subjects to be considered \n
        tmin, tmax : tmin, tmax for delimiting the epochs in time \n
        bads : list of electrodes to be rejected \n
        picks : list of electrodes to be worked on \n
        filtering : tuple containing the higher and lower frequencies to filter the data \n
        tmin, tmax : tmin, tmax for delimiting the epochs in time \n
        ICA : Boolean, whether or not to apply Independent Component Analysis \n
        resample : boolean, whether or not to resample the data at 512 Hz \n
        baseline : the baseline to be applied to the data  \n
        event_ids : The id of the event to consider \n
        reference : the name of the reference to be applied to the data \n
        """
        self.classifier_log.extend(
            [("directory", directory), ("nb_subj", nb_subj), ("tmin", tmin), ("tmax", tmax), ("bads", bads),
             ("picks", picks), ("filtering", filtering), ('pre_epoched', True), ('ICA', ICA), ('resample', resample),
             ('baseline', baseline), ('event_ids', event_ids), ('reference', reference)])
        # MNE loading parameters
        montage = make_standard_montage("standard_1005")

        self.nb_paradigms = len(event_ids)
        # self.classifier_log.append(('nb of paradigms', nb_paradigms))
        # Load raw EEG data
        # =================

        data_root_folder = directory
        epoched_raw_eeg_dataset = [[] for _ in range(nb_subj)]
        epoched_raw_eeg_sources = [[] for _ in range(nb_subj)]
        labels = [[] for _ in range(nb_subj)]
        labels_sources = [[] for _ in range(nb_subj)]
        file_names = []
        # epochs = []
        groups = []

        list_of_files = []
        list_of_dirs = []

        for raw_eeg_file in os.listdir(data_root_folder):
            if (".set" in raw_eeg_file) or ("-epo.fif" in raw_eeg_file):
                list_of_files.append(raw_eeg_file)
            if "directory" in raw_eeg_file:
                list_of_dirs.append(raw_eeg_file)
        list_of_files.sort()
        list_of_dirs.sort()

        # subject_i = -1
        for subject_i, raw_eeg_file in enumerate(list_of_files):
            if subject_i < nb_subj:
                file_names.append(raw_eeg_file)
                raw_file_path = os.path.join(data_root_folder, raw_eeg_file)  # data_class_folder

                for condition in range(len(event_ids)):
                    label = condition
                    epoched_eeg = read_epochs_eeglab(raw_file_path, event_id=event_ids[condition])  # montage=montage
                    if reference is not None:
                        epoched_eeg.set_eeg_reference(reference, projection=False)
                    if filtering[0] is None:
                        filtering[0] = epoched_eeg.info['highpass']
                    if filtering[1] is None:
                        filtering[1] = epoched_eeg.info['lowpass']
                    epoched_eeg.filter(filtering[0], filtering[1])
                    if picks is not None:
                        epoched_eeg.pick_channels(picks)
                    epoched_eeg.crop(tmin=tmin, tmax=tmax)

                    epoched_sources = deepcopy(epoched_eeg)
                    epoched_data = epoched_eeg.get_data()

                    epoched_labels = np.zeros(epoched_data.shape[0], dtype=np.int) + label
                    epoched_labels_sources = label

                    epoched_raw_eeg_dataset[subject_i].append(epoched_data)
                    labels[subject_i].append(epoched_labels)

                    epoched_raw_eeg_sources[subject_i].append(epoched_sources)
                    labels_sources.append(epoched_labels_sources)

            for subject_j, raw_eeg_dir in enumerate(list_of_dirs):
                raw_path_subject = os.path.join(raw_file_path, raw_eeg_dir)
                subject_files = []
                for raw_eeg_file_path in os.listdir(raw_path_subject):
                    if (".set" in raw_eeg_file_path) or ("-epo.fif" in raw_eeg_file_path):
                        subject_files.append(raw_eeg_file_path)
                    nb_files = len(subject_files)
                if subject_i + subject_j + 1 < nb_subj:
                    file_names.append(raw_eeg_dir)
                    epoched_raw_eeg_dataset[subject_i + subject_j + 1].append([])
                    labels[subject_i + subject_j + 1].append([])
                    epoched_raw_eeg_sources[subject_i + subject_j + 1].append([])
                    for raw_eeg_subject_file in subject_files:
                        raw_file_path = os.path.join(raw_path_subject, raw_eeg_subject_file)

                        for condition in range(len(event_ids)):

                            label = condition
                            epoched_eeg = read_epochs_eeglab(raw_file_path, montage=montage,
                                                             event_id=event_ids[condition])
                            if reference is not None:
                                epoched_eeg.set_eeg_reference(reference, projection=False)
                            if filtering[0] is None:
                                filtering[0] = epoched_eeg.info['highpass']
                            if filtering[1] is None:
                                filtering[1] = epoched_eeg.info['lowpass']
                            epoched_eeg.filter(filtering[0], filtering[1])
                            if picks is not None:
                                epoched_eeg.pick_channels(picks)
                            epoched_eeg.crop(tmin=tmin, tmax=tmax)

                            epoched_sources = deepcopy(epoched_eeg)
                            epoched_data = epoched_eeg.get_data()

                            epoched_labels = np.zeros(epoched_data.shape[0], dtype=np.int) + label
                            epoched_labels_sources = label
                            epoched_raw_eeg_dataset[subject_i + subject_j + 1][label].append(epoched_data)
                            labels[subject_i + subject_j + 1][label].append(epoched_labels)

                            epoched_raw_eeg_sources[subject_i + subject_j + 1][label].append(epoched_sources)
                            labels_sources.append(epoched_labels_sources)

                    if nb_files > 1:
                        epoched_raw_eeg_dataset[subject_i + subject_j + 1][label] = np.asarray(
                            np.concatenate(epoched_raw_eeg_dataset[subject_i + subject_j + 1][label]))
                        labels[subject_i + subject_j + 1][label] = np.asarray(
                            np.concatenate(labels[subject_i + subject_j + 1][label]))
                        epoched_raw_eeg_sources[subject_i + subject_j + 1][label] = concatenate_epochs(
                            epoched_raw_eeg_sources[subject_i + subject_j + 1][label])
                    else:
                        epoched_raw_eeg_dataset[subject_i + subject_j + 1][label] = np.asarray(
                            epoched_raw_eeg_dataset[subject_i + subject_j + 1][label][0])
                        labels[subject_i + subject_j + 1][label] = np.asarray(
                            labels[subject_i + subject_j + 1][label][0])
                        epoched_raw_eeg_sources[subject_i + subject_j + 1][label] = \
                            epoched_raw_eeg_sources[subject_i + subject_j + 1][label][0]

        for subject_i in range(len(epoched_raw_eeg_dataset)):
            if self.nb_paradigms == 2:
                first = epoched_raw_eeg_dataset[subject_i][0].shape[0]
                second = epoched_raw_eeg_dataset[subject_i][1].shape[0]
                minimum = min([first, second])
                epoched_raw_eeg_dataset[subject_i][0] = epoched_raw_eeg_dataset[subject_i][0][:minimum]
                epoched_raw_eeg_dataset[subject_i][1] = epoched_raw_eeg_dataset[subject_i][1][:minimum]
                labels[subject_i][0] = labels[subject_i][0][:minimum]
                labels[subject_i][1] = labels[subject_i][1][:minimum]
            epoched_raw_eeg_dataset[subject_i] = np.concatenate(np.asarray(epoched_raw_eeg_dataset[subject_i]), axis=0)
            for k in range(epoched_raw_eeg_dataset[subject_i].shape[0]):
                groups.append(subject_i)
            labels[subject_i] = np.concatenate(np.asarray(labels[subject_i]), axis=0)

            # epoched_raw_eeg_sources = np.asarray(epoched_raw_eeg_sources)
            labels_sources = np.asarray(labels_sources)

        electrodes = epoched_raw_eeg_sources[0][0].info['ch_names']

        epoched_raw_eeg_dataset = np.asarray(epoched_raw_eeg_dataset)
        # labels_sources = np.asarray(labels_sources)
        labels = np.asarray(labels)
        self.dataset = epoched_raw_eeg_dataset
        self.dataset_sources = epoched_raw_eeg_sources
        self.labels = labels
        self.electrodes = electrodes
        self.groups = np.asarray(groups)
        self.vertices = []

        labs = np.concatenate(self.labels)
        unique, counts = np.unique(labs, return_counts=True)
        occurences = dict(zip(unique, counts))
        self.classifier_log.append(("occurences from each class : ", occurences))

    def prepare_nonepoched_dataset_oneFilePerSubj(self, directory, nb_subj, tmin, tmax, bads=None, picks=None,
                                                  filtering=[None, None], ICA=False, resample=False, baseline=None,
                                                  event_ids=[None, None]):
        """
        Prepare a   subjects x epochs x channels x times     dataset from raw files  \n
        Parameters \n
        ---------- \n
        directory : the path to the directory containing the dataset \n
        nb_subj : the number of subjects to be considered \n
        tmin, tmax : tmin, tmax for delimiting the epochs in time \n
        bads : list of electrodes to be rejected \n
        picks : list of electrodes to be worked on \n
        filtering : tuple containing the higher and lower frequencies to filter the data \n
        tmin, tmax : tmin, tmax for delimiting the epochs in time \n
        ICA : Boolean, whether or not to apply Independent Component Analysis \n
        resample : boolean, whether or not to resample the data at 512 Hz \n
        baseline : the baseline to be applied to the data  \n
        event_ids : The id of the event to consider \n
        reference : the name of the reference to be applied to the data \n
        """

        # MNE loading parameters
        # montage = make_standard_montage("standard_1005")

        # Load raw EEG data
        # =================
        data_root_folder = directory

        # epoched_raw_eeg_dataset = [[] for _ in range(nb_subj)]
        # epoched_raw_eeg_sources = [[] for _ in range(nb_subj)]
        # labels = [[] for _ in range(nb_subj)]
        # labels_sources = [[] for _ in range(nb_subj)]
        file_names = []
        # epochs = []
        # groups = []

        directory_new = os.path.join(directory, "epoched")
        if not os.path.exists(directory_new):
            os.makedirs(directory_new)

        for paradigm in range(len(event_ids)):
            epoched_data_class_folder = os.path.join(directory_new, str(paradigm))
            list_of_files = []
            list_of_dirs = []
            event_id = event_ids[paradigm]
            for raw_eeg_file in os.listdir(data_root_folder):
                if ".set" in raw_eeg_file:
                    list_of_files.append(raw_eeg_file)
                if "directory" in raw_eeg_file:
                    list_of_dirs.append(raw_eeg_file)
            list_of_files.sort()
            list_of_dirs.sort()
            subject_i = 0
            if not os.path.exists(epoched_data_class_folder):
                os.makedirs(epoched_data_class_folder)

            for subject_i, raw_eeg_file in enumerate(list_of_files):
                raw_file_path = os.path.join(data_root_folder, raw_eeg_file)
                self.read_one_file(raw_file_path, raw_eeg_file, epoched_data_class_folder, bads, picks, filtering, tmin,
                                   tmax, ICA=ICA, resample=resample, baseline=baseline, event_ids=event_id)

            for subject_j, raw_eeg_dir in enumerate(list_of_dirs):
                raw_path_subject = os.path.join(data_root_folder, raw_eeg_dir)
                epoched_raw_path_subject = os.path.join(epoched_data_class_folder, raw_eeg_dir)
                if not os.path.exists(epoched_raw_path_subject):
                    os.makedirs(epoched_raw_path_subject)
                subject_files = []
                for raw_eeg_file in os.listdir(raw_path_subject):
                    if ".set" in raw_eeg_file:
                        subject_files.append(raw_eeg_file)
                    # nb_files = len(subject_files)
                if subject_i + subject_j < nb_subj:
                    file_names.append(raw_eeg_dir)
                    for raw_eeg_file in subject_files:
                        raw_file_path = os.path.join(raw_path_subject, raw_eeg_file)
                        self.read_one_file(raw_file_path, raw_eeg_file, epoched_raw_path_subject, bads, picks,
                                           filtering, tmin, tmax, ICA=ICA, resample=resample, baseline=baseline,
                                           event_ids=event_id)

    """
    Computation
    """
    def estimate_sources(self, raw_dataset, info, tmin_noise, tmax_noise, trans=None, sourceSpaces=None,
                         bemSolution=None, mixedSourceSpaces=None, loose=1, snr=3, fixed=False):
        """
        Estimates the sources for the dataset using a Sources_estimator object. \n
        Parameters \n
        --------- \n
        raw_dataset : the dataset to be estimated \n
        info : info dictionary for the EEG recordings (see Epochs.info) \n
        tmin_noise, tmax_noise : tmin and tmax for delimiting the noise estimation \n
        trans=None : path to the eventual coregistration file \n
        sourceSpaces : path to the eventual source spaces file \n
        bemSolution : path to the eventual bem solution file \n
        mixedSourceSpaces : path to the eventual mixed source spaces file \n
        loose : between 0 and 1. "value that weights the source variances of the dipole components that are parallel (tangential) to the cortical surface" \n
        snr = signal to noise ratio value \n
        fixed : Boolean, whether or not to use fixed source orientations normal to the cortical mantle \n
        """
        sources_estimator = Sources_estimator(raw_dataset, info, tmin_noise, tmax_noise, trans=trans,
                                              sourceSpaces=sourceSpaces,
                                              bemSolution=bemSolution, mixedSourceSpaces=mixedSourceSpaces, loose=loose,
                                              snr=snr, fixed=fixed)
        labels, labeled_sources = sources_estimator.estimate_sources()
        self.dataset_sources = labeled_sources
        return labels

    def estimate_covariance_matrices(self, dataset):
        """
        Creates the simple covariance matrices for the raw data. \n
        Result format = nb_subj  x  nb_epochs  x  nb_channels  x  nb_channels \n
        Parameters \n
        ---------- \n
        dataset : the dataset on which to estimate the covariance matrices. \n
        """
        covariance_matrices = []
        if self.nb_subj == 1:
            covariance_matrices.append(Covariances("oas").transform(dataset))
        else:
            for subject in dataset:
                covariance_matrices.append(Covariances("oas").transform(subject))
        return np.asarray(covariance_matrices)

    def independent_features_selection(self, use_sources=False, channels_to_select=None, use_groups=True):
        """
        Applies independent channel or zone selection on the data, without the pipelines. Only the selected channels or zones will be
        kept on the final data.  \n 
        Parameters  \n
        ---------- \n
        use_sources : boolean; whether or not to use sources for feature selection \n
        cv : int; number of folds for cross validation \n
        channels_to_select : int; if any, the desired number of features  \n
        use_groups : boolean; whether or not to use groups when dividing the data \n
        """
        if not use_sources:
            dataset = self.dataset
            feats = self.electrodes
        else:
            dataset = self.dataset_sources
            feats = self.vertices

        dataset_cov = self.estimate_covariance_matrices(dataset.get_data())
        labels = self.labels

        nb_subjects = dataset_cov.shape[0]
        nb_channels = dataset_cov[0].shape[1]

        if nb_subjects == 1:
            dataset_cov = dataset_cov[0]
        else:
            dataset_cov = np.concatenate(dataset_cov)
            labels = np.concatenate(labels)

        cv = self.create_folder(4)
        if nb_channels <= CONST_MAX_1by1_ELECTRODES:
            tries = [i for i in range(1, nb_channels + 1)]
        elif nb_channels <= CONST_MAX_5by5_ELECTRODES:
            tries = [i for i in range(1, nb_channels + 1, 5)]
            if nb_channels % 5 != 0:
                tries.append(nb_channels)
        else:
            tries = [i for i in range(1, nb_channels + 1, 10)]
            if nb_channels % 10 != 0:
                tries.append(nb_channels)

        if channels_to_select is None:
            es = GridSearchCV(ElectrodeSelection(), param_grid={"nelec": tries}, cv=cv,
                              scoring=self.score_func_independent_feat_selection, n_jobs=-1)
            if use_groups:
                es.fit(dataset_cov, labels, self.groups)
            else:
                es.fit(dataset_cov, labels)
            # idx = es.best_index_
            selected_estimator = es.best_estimator_
            print("Number of selected features : ", selected_estimator.nelec)
            selected_feats_idx = selected_estimator.subelec_
            selected_feats = [feats[i] for i in selected_feats_idx]
            additional_informations = [("independent features selection", True),
                                       ("pre_selected number of features", False),
                                       ("selected number of features", selected_estimator.nelec),
                                       ("features", selected_feats)]
        else:
            print("You have chosen to select the best ", channels_to_select, " channels.")
            es = ElectrodeSelection(nelec=channels_to_select)
            print(dataset_cov.shape)
            print(labels.shape)
            es.fit(dataset_cov, labels)
            selected_feats_idx = es.subelec_
            selected_feats = [feats[i] for i in selected_feats_idx]
            additional_informations = [("independent ChanVertexSelection", True),
                                       ("pre_selected number of features", channels_to_select),
                                       ("features", selected_feats)]
        self.classifier_log.extend(additional_informations)
        print("Selected features are : ", selected_feats)
        # for person_idx in range(self.dataset.shape[0]):
        #     self.dataset[person_idx] = self.dataset[person_idx][:, selected_feats_idx, :]
        return self.dataset

    def tune_hyperparameters(self, cv, use_sources=False, use_groups=True, factor=None):
        """
        Tune the hyperparameters for the different pipelines and replace the pipelines by their improved versions. \n
        Parameters \n
        ---------- \n
        cv : cross validation for tuning \n
        use_sources : boolean; whether or not to use the sources dataset \n
        use_groups : boolean; whether or not to use groups for the cross validation \n
        factor : int; the stair by which to augment the number of filters or electrodes \n
        """
        self.classifier_log.extend([("hyperparameters tuning", True), ("cross validation for tuning", cv)])

        max_filters = int(len(self.electrodes) / 2)
        if max_filters > 5:
            if factor is None:
                additional_filters = [i for i in range(10, max_filters + 1, 10)]
            else:
                additional_filters = [i for i in range(10, max_filters + 1, factor)]
            if max_filters % 5 != 0:
                additional_filters.append(max_filters)

            self.pipeline_catalogue.XDAWN_filters.extend(additional_filters)
            self.pipeline_catalogue.csp_filters.extend(additional_filters)

        if use_sources:
            dataset = self.dataset_sources
        else:
            dataset = self.dataset

        labels = self.labels
        cv = self.create_folder(cv)

        nb_subjects = self.nb_subj
        nb_channels = len(self.electrodes)

        if nb_subjects == 1:
            dataset = dataset[0]
            labels = labels[0]
        else:
            dataset = np.concatenate(dataset)
            labels = np.concatenate(labels)

        if factor is None:
            if nb_channels <= CONST_MAX_1by1_ELECTRODES:
                nb_elec = [i for i in range(1, nb_channels + 1)]
            elif nb_channels <= CONST_MAX_5by5_ELECTRODES:
                nb_elec = [i for i in range(1, nb_channels + 1, 5)]
                if nb_channels % 5 != 0:
                    nb_elec.append(nb_channels)
            else:
                nb_elec = [i for i in range(1, nb_channels + 1, 10)]
                if nb_channels % 10 != 0:
                    nb_elec.append(nb_channels)
        else:
            nb_elec = [i for i in range(1, nb_channels + 1)]
            if nb_channels % factor != 0:
                nb_elec.append(nb_channels)
        self.pipeline_catalogue.nb_elec = nb_elec

        pipelines = list(self.catalogue.keys())
        pipelines.sort()
        grid_searches = {}
        random_searches = {}
        for pipeline in pipelines:
            if self.parameters[pipeline][0] == 0:
                pass
            elif self.parameters[pipeline][0] == 1:
                grid_searches[pipeline] = GridSearchCV(self.catalogue[pipeline],
                                                       param_grid=self.parameters[pipeline][1], cv=cv)
            elif self.parameters[pipeline][0] == 2:
                distribution = randint(1, max_filters)
                self.parameters[pipeline][1] = {self.parameters[pipeline][1][i]: distribution for i in
                                                range(len(self.parameters[pipeline][1]))}
                random_searches[pipeline] = RandomizedSearchCV(self.catalogue[pipeline],
                                                               param_distributions=self.parameters[pipeline][1],
                                                               n_iter=self.parameters[pipeline][2], cv=cv, n_jobs=-1)
        for gs in grid_searches:
            if use_groups:
                grid_searches[gs].fit(dataset, labels, groups=self.groups)
            else:
                grid_searches[gs].fit(dataset, labels)
            selected_estimator = grid_searches[gs].best_estimator_
            self.catalogue[gs] = selected_estimator

        for gs in random_searches:
            if use_groups:
                random_searches[gs].fit(dataset, labels, groups=self.groups)
            else:
                random_searches[gs].fit(dataset, labels)
            selected_estimator = random_searches[gs].best_estimator_
            self.catalogue[gs] = selected_estimator

        print("Pipelines' hyperparameters have been tuned")

    def fit(self, x_train, y_train):
        """
        Fits all the pipeline to a provided dataset. \n
        Parameters \n
        ---------- \n
        x_train : the training samples \n
        y_train : the correct answers to the training samples \n
        """
        pipelines = list(self.catalogue.keys())
        pipelines.sort()

        for pipeline_name in pipelines:
            pipeline = self.catalogue[pipeline_name]
            try:
                pipeline.fit(x_train, y_train)
            except:
                print("Errors encountered with pipeline " + pipeline_name + ". This pipeline will be removed.")
                self.delete_pipelines([pipeline_name])
        return self

    def fit_transform(self, x, y):
        self.fit(x, y)

    def predict(self, x_test):
        """
        Predicts the values for a dataset. \n
        Parameters \n
        ---------- \n
        x_test : the test samples \n
        """
        pipelines = list(self.catalogue.keys())
        pipelines.sort()
        pipeline_counter = 0
        round_predictions = []
        for pipeline_name in pipelines:
            pipeline = self.catalogue[pipeline_name]

            preds = pipeline.predict(x_test)
            round_predictions.append(preds)
            for i in range(len(preds)):
                self.predictions[pipeline_name].append(preds[i])
            pipeline_counter += 1
        return round_predictions

    def predict_proba(self, x_test):
        """
        Predicts with probabilities the values for a dataset. \n
        Parameters \n
        ---------- \n
        x_test : the test samples \n
        """
        pipelines = list(self.catalogue.keys())
        pipelines.sort()
        pipeline_counter = 0
        round_predictions = []
        for pipeline_name in pipelines:
            pipeline = self.catalogue[pipeline_name]

            preds = pipeline.predict_proba(x_test)
            round_predictions.append(preds)
            preds_abs = np.argmax(preds, axis=1)
            for i in range(len(preds)):
                self.predictions_proba[pipeline_name].append(preds[i])
                self.predictions[pipeline_name].append(preds_abs[i])

            pipeline_counter += 1
        return round_predictions

    """
    Scores
    """
    def final_score(self):
        """
        Final scoring function. For each pipeline, a score, confusion matrix, precision, recall, and ROC curve is created.
        """
        labels = self.labels
        pipelines = list(self.catalogue.keys())
        pipelines.sort()
        expected = self.expected_answers

        try:
            if self.nb_subj != 1:
                labels = np.concatenate(labels)
            for pipeline_name in pipelines:
                predictions_pipeline = self.predictions[pipeline_name]
                score = 0
                precision = 0
                recall = 0

                confusion_matrix = [[0 for _ in range(self.nb_paradigms)] for _ in range(self.nb_paradigms)]
                for pred_idx in range(len(predictions_pipeline)):
                    confusion_matrix[expected[pred_idx]][predictions_pipeline[pred_idx]] += 1
                corrects = np.sum([confusion_matrix[i][i] for i in range(self.nb_paradigms)])
                score = corrects / np.sum(confusion_matrix)
                if self.nb_paradigms == 2:
                    if confusion_matrix[1][1] + confusion_matrix[0][1] != 0:
                        precision = confusion_matrix[1][1] / (confusion_matrix[1][1] + confusion_matrix[0][1])
                    else:
                        precision = 0
                    if confusion_matrix[1][1] + confusion_matrix[1][0] != 0:
                        recall = confusion_matrix[1][1] / (confusion_matrix[1][1] + confusion_matrix[1][0])
                    else:
                        recall = 0

                    self.precisions[pipeline_name] = precision
                    self.recalls[pipeline_name] = recall

                self.scores[pipeline_name] = score
                self.confusion_matrices[pipeline_name] = confusion_matrix

                if self.nb_paradigms == 2:
                    # ROC curve
                    preds_proba = self.predictions_proba[pipeline_name]
                    positive_proba = []
                    for j in range(len(preds_proba)):
                        positive_proba.append(preds_proba[j][1])
                    fpr, tpr, threshold = metrics.roc_curve(expected, positive_proba)
                    roc_auc = metrics.auc(fpr, tpr)
                    self.roc_infos[pipeline_name] = [fpr, tpr, roc_auc]
            if self.nb_paradigms == 2:
                auc_scores = deepcopy(self.roc_infos)
                for pipeline in self.roc_infos:
                    auc_scores[pipeline] = auc_scores[pipeline][2]
            self.classifier_log.append(('pipelines : ', list(self.catalogue.keys())))
            self.classifier_log.append(("scores", self.scores))
            if self.nb_paradigms == 2:
                self.classifier_log.append(("scores auc", auc_scores))
                self.classifier_log.append(("recalls", self.recalls))
                self.classifier_log.append(("precisions", self.precisions))
        except Exception as e:
            print(e)
            exit()

    def score(self, x, y):
        """
        Return the accuracy on the given test data and labels. \n
        Parameters \n
        ---------- \n
        x : test samples \n
        y : correct answers for x \n
        weights : Sample weights \n
        """
        pipelines = list(self.catalogue.keys())
        pipelines.sort()
        scores = {key: [] for key in list(self.catalogue.keys())}

        for pipeline_name in pipelines:
            pipeline = self.catalogue[pipeline_name]
            score = pipeline.score(x, y)
            scores[pipeline_name] = score

        return scores

    def score_all_pipelines(self, x, y):
        """
        Return the accuracy on the given predictions and labels for all trained pipelines. \n
        Parameters \n
        ---------- \n
        x : test samples \n
        y : correct answers for x \n
        """
        scores = [0.0 for _ in range(len(self.catalogue.keys()))]
        for pipeline in list(x.keys()):
            for i in range(len(x[pipeline])):
                if x[pipeline][i] == y[i]:
                    scores[pipeline] += 1
            scores[pipeline] = scores[pipeline] / len(x[pipeline])
        return scores

    def predict_test_dataset(self):
        """
        Predicts the left out test dataset, computes the score and shows the results.
        """
        self.restore()

        self.dataset = self.test_dataset
        self.labels = self.test_labels

        dataset = np.concatenate(self.dataset)
        labels = np.concatenate(self.labels)
        self.expected_answers = labels

        self.predict_proba(dataset)

        self.final_score()
        print(self.scores)
        self.show_results(4)

    def score_func_independent_feat_selection(self, estimator, x_test, y_test):
        """
        Scoing function for the independent feature selection. The previously trained pipeline is used to predict the test dataset. \n
        At the end, the predicted data are compared to the correct answers, and the percentage of correctly classified data is considered the score. \n
        Parameters \n
        ---------- \n
        estimator : the estimator that predicts and scores \n
        x_test : the test dataset \n
        y_test : the correct answers to the dataset \n
        """
        x_test = estimator.transform(x_test)
        score = 0
        pipeline = estimator.pipeline
        predictions = pipeline.predict(x_test)
        for i in range(y_test.shape[0]):
            if predictions[i] == y_test[i]:
                score += 1
        score = score / y_test.shape[0]
        return score

    def score_func(self, estimator, x_test, y_test):
        """
        Scoing function for the independent feature selection. The previously trained pipeline is used to predict the test dataset.
        At the end, the predicted data are compared to the correct answers, and the percentage of correctly classified data is considered the score. \n
        Parameters \n
        ---------- \n
        estimator : the estimator that predicts and scores \n
        x_test : the test dataset \n
        y_test : the correct answers to the dataset \n
        """
        estimator_steps = estimator.named_steps.keys()
        i = 0
        for step in estimator_steps:
            i += 1
            if i == len(estimator_steps):
                break
            x_test = estimator.named_steps[step].transform(x_test)
        score = 0
        predictions = estimator.named_steps[step].predict(x_test)
        for i in range(y_test.shape[0]):
            if predictions[i] == y_test[i]:
                score += 1
        score = score / y_test.shape[0]
        return score

    """
    Plot
    """
    def plot_ROC(self, nb_lines, nb_columns):
        """
        Plots the ROC curves for all the pipelines from the catalogue. \n
        Parameters \n
        ---------- \n
        nb_lines : the number of lines to be used for all the pipelines \n
        nb_columns : the number of columns to be used for all the pipelines \n
        """
        pipelines = list(self.catalogue.keys())
        pipelines.sort()
        # pipeline_counter = 0

        x = 0
        y = 0
        fig, axs = plt.subplots(nb_lines, nb_columns)

        for pipeline_name in pipelines:
            fpr, tpr, auc = self.roc_infos[pipeline_name]
            # plt.subplot(nb_lines, nb_columns, pipeline_counter + 1)
            # title = pipeline_name + " : " + str(self.scores[pipeline_name])

            if nb_lines > 1:
                axs[x, y].set_title(pipeline_name)
                axs[x, y].plot(fpr, tpr, 'b', label='AUC = %0.2f' % auc)
                axs[x, y].legend(loc='lower right')
                axs[x, y].plot([0, 1], [0, 1], 'r--')
                axs[x, y].set_xlim([0, 1])
                axs[x, y].set_ylim([0, 1])
                axs[x, y].set_ylabel('True Positive Rate')
                axs[x, y].set_xlabel('False Positive Rate')
                # pipeline_counter += 1
                y += 1
                if y == nb_columns:
                    y = 0
                    x += 1
            else:
                axs[y].set_title(pipeline_name)
                axs[y].plot(fpr, tpr, 'b', label='AUC = %0.2f' % auc)
                axs[y].legend(loc='lower right')
                axs[y].plot([0, 1], [0, 1], 'r--')
                axs[y].set_xlim([0, 1])
                axs[y].set_ylim([0, 1])
                axs[y].set_ylabel('True Positive Rate')
                axs[y].set_xlabel('False Positive Rate')
                y += 1

        fig.show()

    def plot_confusion(self, nb_lines, nb_columns, names):
        """
        Plots the confusion matrices for all the pipelines from the catalogue. \n
        Parameters \n
        ---------- \n
        nb_lines : the number of lines to be used for all the pipelines \n
        nb_columns : the number of columns to be used for all the pipelines \n
        names : list; list containing the names of the labels for the categories. \n
        """
        pipelines = list(self.catalogue.keys())
        pipelines.sort()
        pipeline_counter = 0
        for pipeline_name in pipelines:
            confusion_matrix = self.confusion_matrices[pipeline_name]
            plotted_confusion_matrix = [[] for _ in range(len(confusion_matrix))]
            for i in range(len(confusion_matrix)):
                for j in range(len(confusion_matrix)):
                    plotted_confusion_matrix[i].append(confusion_matrix[i][j]/np.sum(confusion_matrix[i]))
            plt.subplot(nb_lines, nb_columns, pipeline_counter + 1)
            plt.title(pipeline_name)
            sn.heatmap(plotted_confusion_matrix, annot=True, cmap="YlGnBu", vmin=0, vmax=1, xticklabels=names,
                       yticklabels=names)
            pipeline_counter += 1
        plt.show()

    def show_results(self, nb_columns):
        """
        Shows the ROC curves and the confusion matrices for all the pipelines. \n
        Parameters \n
        ---------- \n
        nb_columns : the number of columns to be used for all the pipelines \n
        names : list; list containing the names of the labels for the categories. \n
        """
        pipelines = list(self.catalogue.keys())
        pipelines.sort()
        nb_lines = math.ceil(len(pipelines) / nb_columns)
        # Confusion
        self.plot_confusion(nb_lines, nb_columns, self.event_names)
        time.sleep(1)
        # ROC
        if self.nb_paradigms == 2:
            self.plot_ROC(nb_lines, nb_columns)

    def plot_ROC_(self, nb_columns):
        pipelines = list(self.catalogue.keys())
        pipelines.sort()
        nb_lines = math.ceil(len(pipelines) / nb_columns)
        # ROC
        if self.nb_paradigms == 2:
            self.plot_ROC(nb_lines, nb_columns)

    def plot_confusion_(self, nb_columns):
        pipelines = list(self.catalogue.keys())
        pipelines.sort()
        nb_lines = math.ceil(len(pipelines) / nb_columns)
        # Confusion
        self.plot_confusion(nb_lines, nb_columns, self.event_names)

    """
    Classification
    """
    def classify(self, dataset, dataset_path=None, test_dataset_size=5, cv_value=5, independent_features_selection=False,
                 channels_to_select=20, use_groups=True, tune_hypers=False, classify_test=False):
        """
        Global classification method of the library. (inter-subjects)\n
        Reads the dataset, can apply independent features selection, can tune hyperparameters, fits, predicts, scores, and shows results.\n
        Parameters \n
        ----------
        dataset : string; the path to the dataset \n
        test_dataset_size : int; the fraction of the dataset to be considered for testing \n
        pre_epoched : boolean; whether the dataset is already epoched or not\n
        tmin, tmax : time limits for the epochs \n
        bads : list of electrodes to be rejected \n
        picks : list of electrodes to be worked on \n
        filtering : tuple containing the higher and lower frequencies to filter the data \n
        tmin, tmax : tmin, tmax for delimiting the epochs in time \n
        ICA : Boolean, whether to apply Independent Component Analysis or not\n
        resample : boolean, whether to resample the data at 512 Hz or not \n
        baseline : the baseline to be applied to the data  \n
        cv_value : int; the number of folds for cross validation. If None, the number of subjects will be used (Leave one out) \n
        independent_features_selection : boolean; whether to apply independent features selection or not \n
        channels_to_select : int or None; the number of channels to be selected or None if automatic number selection \n
        use_groups : boolean; whether to use groups for cross validation or not \n
        tune_hypers : boolean; whether to tune hyperparameters or not \n
        names : list; names of the categories \n
        classify_test : boolean; whether there should be a separate test dataset or not \n
        """
        self.dataset = dataset
        self.labels = []
        self.event_names = []
        self.electrodes = dataset.info["ch_names"]

        labels_dic = {}
        labels_idx = 0
        for event in self.dataset.events:
            event_label = event[2]
            if event_label not in labels_dic:
                labels_dic[event_label] = labels_idx
                for key in dataset.event_id.keys():
                    if dataset.event_id[key] == event_label:
                        self.event_names.append(key)
                labels_idx += 1
            self.labels.append(labels_dic[event_label])

        self.labels = np.asarray(self.labels)
        self.nb_paradigms = len(self.dataset.event_id)

        try:
            if classify_test and test_dataset_size != 0:
                limit_dataset = self.dataset.shape[0] // test_dataset_size
                limit_dataset_0 = limit_dataset // 2
                limit_dataset_1 = limit_dataset - limit_dataset_0
                self.test_dataset = np.concatenate(
                    [self.dataset[:limit_dataset_0], self.dataset[-limit_dataset_1:]])
                self.dataset = self.dataset[limit_dataset_0:-limit_dataset_1]
                self.test_labels = np.concatenate([self.labels[:limit_dataset_0], self.labels[-limit_dataset_1:]])
                self.labels = self.labels[limit_dataset_0:-limit_dataset_1]
        except Exception as e:
            print(e)

        if use_groups:
            cv = GroupKFold(cv_value)
        else:
            cv = KFold(cv_value, shuffle=True, random_state=42)

        if independent_features_selection:
            try:
                self.independent_features_selection(False, channels_to_select=channels_to_select, use_groups=use_groups)
            except Exception as e:
                print("Independent features selection error")
                print(e)
        if tune_hypers:
            try:
                self.tune_hyperparameters(cv_value, use_sources=False, use_groups=use_groups)
            except Exception as e:
                print("Hyperparameters tuning error")
                print(e)
        if use_groups:
            groups = self.groups
        else:
            groups = None

        dataset = np.asarray(self.dataset)
        labels = self.labels

        for train_index, test_index in cv.split(dataset, labels, groups=groups):

            x_train = dataset[train_index]
            y_train = labels[train_index]

            x_test = dataset[test_index]
            y_test = labels[test_index]

            self.fit(x_train, y_train)
            predictions_proba = self.predict_proba(x_test)
            scores = self.score(x_test, y_test)
            for pipeline in scores.keys():
                self.scores_fold[pipeline].append(scores[pipeline])
            predictions_proba = np.argmax(predictions_proba, axis=2)
            self.expected_answers.extend(y_test)

        self.final_score()
        pipelines = list(self.catalogue.keys())
        pipelines.sort()
        print(self.classifier_log)

        self.classifier_log.append(('Predictions', "see 'predictions.npy' in dataset folder"))
        np.save(os.path.join(dataset_path, "predictions.npy"), self.predictions)

        self.save_program_log(dataset_path)

        if classify_test:
            if test_dataset_size == 0:
                text = "Test dataset size is 0. Test dataset estimation can not be applied."
                raise Exception(text)
            self.predict_test_dataset()

    def classify_intraSubject(self, dataset, divided_dataset=True, nb_subj=None, test_dataset_size=5, pre_epoched=True,
                              tmin=-0.2, tmax=0.5, bads=None, picks=None, filtering=[None, None], ICA=False,
                              resample=False, baseline=None, event_ids=[None, None], reference=None,
                              cv_value=5, independent_features_selection=False, channels_to_select=20,
                              tune_hypers=False, names=[0, 1], classify_test=False, use_all_pipelines=False):
        """
        Global classification method of the library. (intra-subject) \n
        Reads the dataset, can apply independent features selection, can tune hyperparameters, fits, predicts, scores, and shows results. \n
        Parameters \n
        ---------- \n
        dataset : string; the path to the dataset \n
        nb_subj : int; number of subjects to consider \n
        test_dataset_size : int; the fraction of the dataset to be considered for testing \n
        pre_epoched : boolean; whether or not the dataset is already epoched \n
        tmin, tmax : time limits for the epochs \n
        bads : list of electrodes to be rejected \n
        picks : list of electrodes to be worked on \n
        filtering : tuple containing the higher and lower frequencies to filter the data \n
        tmin, tmax : tmin, tmax for delimiting the epochs in time \n
        ICA : Boolean, whether or not to apply Independent Component Analysis \n
        resample : boolean, whether or not to resample the data at 512 Hz \n
        baseline : the baseline to be applied to the data  \n
        cv_value : int; the number of folds for cross validation. If None, the number of subjects will be used (Leave one out) \n
        independent_features_selection : boolean; whether or not to apply independent features selection \n
        channels_to_select : int or None; the number of channels to be selected or None if automatic number selection \n
        tune_hypers : boolean; whether or not to tune hyperparameters \n
        names : list; names of the categories \n
        classify_test : boolean; whether or not there should be a separate test dataset \n
        use_all_pipelines : boolean; whether or not all the pipelines should be used for classification or only a subset \n
        """

        if not use_all_pipelines:
            self.delete_pipelines(['XdawnCov', 'Xdawn', 'CSP', 'Cosp', 'HankelCov', 'CSSP', 'PSD', 'FgMDM'])

        if nb_subj is None:
            nb_subj = self.count_subjects(dataset)

        if test_dataset_size != 0:
            limit_dataset = nb_subj // test_dataset_size

        self.read_all_files(dataset, nb_subj, divided_dataset=divided_dataset, tmin=tmin, tmax=tmax,
                            pre_epoched=pre_epoched, bads=bads, picks=picks, filtering=filtering, ICA=ICA,
                            resample=resample, baseline=baseline, event_ids=event_ids, reference=reference)

        if classify_test:
            if test_dataset_size != 0:
                self.test_dataset = self.dataset[-limit_dataset:]
                self.dataset = self.dataset[:-limit_dataset]
                self.test_labels = self.labels[-limit_dataset:]
                self.labels = self.labels[:-limit_dataset]

                idx = nb_subj - limit_dataset
                for i in range(idx, nb_subj):
                    lst_idx = np.where(self.groups == i)
                    self.test_groups = np.append(self.test_groups, self.groups[lst_idx])
                    self.groups = np.delete(self.groups, lst_idx)

        loo = LeaveOneOut()
        cv = KFold(cv_value)

        if independent_features_selection:
            self.independent_features_selection(False, cv=cv_value, channels_to_select=channels_to_select,
                                                use_groups=True)
        if tune_hypers:
            self.tune_hyperparameters(cv_value, use_sources=False, use_groups=True)

        for train_index, test_index in loo.split(self.dataset):
            x_train = np.asarray(self.dataset[test_index[0]])
            y_train = np.asarray(self.labels[test_index[0]])

            for train, test in cv.split(x_train, y_train):
                self.fit(x_train[train], y_train[train])
                self.predict_proba(x_train[test])
                self.expected_answers.extend(y_train[test])

        self.final_score()
        print(self.scores)
        pipelines = list(self.catalogue.keys())
        pipelines.sort()
        print(pipelines)
        self.show_results(4, names)
        print(self.classifier_log)

        self.classifier_log.append(('Predictions', "see 'predictions.npy' in dataset folder"))
        np.save(os.path.join(dataset_path, "predictions.npy"), self.predictions)

        self.save_program_log(dataset_path)

        if classify_test:
            if test_dataset_size == 0:
                text = "Test dataset size is 0. Test dataset estimation can not be applied."
                raise Exception(text)

            self.predict_test_dataset()

    def classify_with_CNN(self, dataset, nb_subj=None, divided_dataset=True, pre_epoched=True, tmin=0, tmax=0.5,
                          bads=None, picks=None, filtering=[None, None], ICA=False, resample=False, baseline=None,
                          event_ids=[None, None], reference=None, test_size=5):
        """
        Global classification method of the library. (inter-subjects) \n
        Reads the dataset, can apply independent features selection, can tune hyperparameters, fits, predicts, scores, and shows results. \n
        Parameters \n
        ---------- \n
        dataset : string; the path to the dataset \n
        nb_subj : int; number of subjects to consider \n
        test_dataset_size : int; the fraction of the dataset to be considered for testing \n
        pre_epoched : boolean; whether or not the dataset is already epoched \n
        tmin, tmax : time limits for the epochs \n
        bads : list of electrodes to be rejected \n
        picks : list of electrodes to be worked on \n
        filtering : tuple containing the higher and lower frequencies to filter the data \n
        tmin, tmax : tmin, tmax for delimiting the epochs in time \n
        ICA : Boolean, whether or not to apply Independent Component Analysis \n
        resample : boolean, whether or not to resample the data at 512 Hz \n
        baseline : the baseline to be applied to the data  \n
        cv_value : int; the number of folds for cross validation. If None, the number of subjects will be used (Leave one out) \n
        independent_features_selection : boolean; whether or not to apply independent features selection \n
        channels_to_select : int or None; the number of channels to be selected or None if automatic number selection \n
        use_groups : boolean; whether or not to use groups for cross validation \n
        tune_hypers : boolean; whether or not to tune hyperparameters \n
        names : list; names of the categories \n
        classify_test : boolean; whether or not there should be a separate test dataset \n
        use_all_pipelines : boolean; whether or not all the pipelines should be used for classification or only a subset \n
        """
        # dataset_path = dataset

        if nb_subj is None:
            self.nb_subj = self.count_subjects(dataset)
            nb_subj = self.nb_subj
        else:
            self.nb_subj = nb_subj

        self.read_all_files(dataset, nb_subj, divided_dataset=divided_dataset, tmin=tmin, tmax=tmax,
                            pre_epoched=pre_epoched, bads=bads, picks=picks, filtering=filtering, ICA=ICA,
                            resample=resample, baseline=baseline, event_ids=event_ids, reference=reference)

        """
        if self.nb_subj == 1:
            self.dataset = self.dataset[0]
            self.labels = self.labels[0]
            use_groups=False
        """

        limit_dataset = nb_subj // test_size
        x_test = np.concatenate(self.dataset[0:limit_dataset])
        x_train = np.concatenate(self.dataset[limit_dataset:])

        y_test = np.concatenate(self.labels[0:limit_dataset])
        y_train = np.concatenate(self.labels[limit_dataset:])

        x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
        x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], x_test.shape[2], 1)

        y_test_biss = []
        y_train_biss = []

        for elem in range(y_test.shape[0]):
            if y_test[elem] == 0:
                y_test_biss.append([1, 0])
            elif y_test[elem] == 1:
                y_test_biss.append([0, 1])
            else:
                print("error here test")

        for elem in range(y_train.shape[0]):
            if y_train[elem] == 0:
                y_train_biss.append([1, 0])
            elif y_train[elem] == 1:
                y_train_biss.append([0, 1])
            else:
                print("error here train")

        y_train = np.asarray(y_train_biss)
        y_test = np.asarray(y_test_biss)

        cnn = CNN()
        cnn.compile()
        cnn.train(x_train, y_train, x_test, y_test)
        print(cnn.evaluate(x_test, y_test))
        cnn.show_results()

    """
    Others
    """
    def count_subjects(self, directory):
        """
        Count the number of subjects in the dataset. \n
        Parameters \n
        ---------- \n
        directory : the path to the dataset \n
        """
        subfolders = os.listdir(directory)
        if subfolders[0] != "epoched":
            folder = subfolders[0]
        else:
            folder = subfolders[1]
        list_of_files = []
        path = os.path.join(directory, folder)
        for raw_eeg_file in os.listdir(path):
            if (".set" in raw_eeg_file) or ("directory" in raw_eeg_file) or (".txt" in raw_eeg_file):
                list_of_files.append(raw_eeg_file)
        self.nb_subj = len(list_of_files)
        return len(list_of_files)

    def save_program_log(self, path):
        """
        Saves the program log in a file. \n
        Parameters \n
        ---------- \n
        path : string; path to the place where the file will be saved. \n
        """
        path = os.path.join(path, "program_log.txt")
        file = open(path, "w")
        for element in self.classifier_log:
            text = str(element[0]) + " : " + str(element[1]) + "\n"
            file.write(text)

    def create_folder(self, k):
        """
        Creates the k-folds folder for the data. \n
        Parameters \n
        ---------- \n
        k : int \n
            number of folds \n
        """
        folder = KFold(k, shuffle=True, random_state=42)
        return folder
