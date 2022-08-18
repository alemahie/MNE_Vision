import os

import numpy as np

from mne.io import read_raw_eeglab
from mne.event import find_events
from mne.viz import plot_raw

from copy import deepcopy

from philistine.mne import write_raw_brainvision


class Transformer:
    def __init__(self):
        print("Transformer initialised")

    def read_one_file(self, filename, path, raw_eeg_file):
        """
        x = read_raw_eeglab("G:\\Niki\\dataset changed\\A 220219\\Tom et Paul\\debout\\Tom acteur couple debout.set", preload=True)
        x.pick_channels(["Sync"])
        #mne.viz.plot_raw(x, n_channels=10, duration=10, block=True, clipping="clamp")
        d = x.get_data()
        input(d[0][5000])
        input(d[0][27545])
        input(d[0][27546])
        input(d[0][27547])
        input(d[0][27600])
        time_samples = np.where(d > 0.120)
        input(time_samples)
        time_samples = time_samples[1][0]
        input(time_samples)
        time = time_samples / x.info['sfreq']
        input(time)
        mne.viz.plot_raw(x, n_channels=10, duration=10, block=True, clipping="clamp")
        """
        eeg = read_raw_eeglab(filename, preload=True)
        plot_raw(eeg, n_channels=10, duration=10, block=True, clipping="clamp")
        events = find_events(eeg)
        if events[0][2] == 1:
            found = True
        else:
            found = False

        if found:
            time_samples = events[0][0]
            time = time_samples / eeg.info['sfreq']
        else:
            eeg2 = deepcopy(eeg)
            if 'Sync' in eeg.info['ch_names']:
                eeg2.pick_channels(['Sync'])
            elif '136' in eeg.info['ch_names']:
                eeg2.pick_channels(['136'])
            else:
                return
            data = eeg2.get_data()
            time_samples = np.where(data > 0.120)
            time_samples = time_samples[1][0]
            time = time_samples / eeg.info['sfreq']

        print(time)
        if time != 0.0:
            eeg.crop(tmin=time)
        """
        eeg.resample(512, npad='auto')
        eeg.filter(None, 145)
        eeg.filter(0.1, None)
        eeg.notch_filter(np.asarray([48,50,52]))
        """
        raw_eeg_file = raw_eeg_file[:-4]
        raw_eeg_file = raw_eeg_file + ".vhdr"
        file_path = os.path.join(path, raw_eeg_file)
        write_raw_brainvision(eeg, file_path, events=True)

    def read_all_files(self, directory):
        subfolders = os.listdir(directory)
        for folder in subfolders:
            data_class_folder = os.path.join(directory, folder)
            list_of_files = []
            for raw_eeg_file in os.listdir(data_class_folder):
                if ".set" in raw_eeg_file:
                    list_of_files.append(raw_eeg_file)
            list_of_files.sort()
            for subject_i, raw_eeg_file in enumerate(list_of_files):
                print(raw_eeg_file)
                raw_file_path = os.path.join(data_class_folder, raw_eeg_file)
                self.read_one_file(raw_file_path, data_class_folder, raw_eeg_file)
