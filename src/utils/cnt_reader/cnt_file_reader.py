#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CNT file reader
"""

from mne import create_info
from mne.io import RawArray
from mne.channels import make_standard_montage

import numpy as np

from utils.cnt_reader.libeep import cnt_file

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


def get_raw_from_cnt(path_to_file):
    """
    Get an MNE.Raw object from a CNT file
    :param path_to_file: Path to the file.
    :type path_to_file: str
    :return: The MNE data of the dataset.
    :rtype: MNE.Raw
    """
    cnt = cnt_file(path_to_file)

    sample_count = cnt.get_sample_count()
    sample_frequency = cnt.get_sample_frequency()
    channel_names, channel_types = get_all_channels_names(cnt)

    data = np.transpose(cnt.get_samples(0, sample_count))

    cnt_info = create_info(channel_names, sample_frequency, ch_types=channel_types)
    cnt_raw = RawArray(data, cnt_info)

    montage = make_standard_montage('standard_1005')
    cnt_raw.set_montage(montage)

    return cnt_raw


def get_all_channels_names(cnt):
    """
    Get all the channels' names based on the CNT data
    :param cnt: The CNT file read.
    :type cnt: libeep.cnt_file
    :return: channel_names: The channels' names.
    channel_types: The channels' types.
    :rtype: list of str, list of str
    """
    channel_names = []
    channel_types = []
    for i in range(cnt.get_channel_count()):
        channel = cnt.get_channel_info(i)[0]
        channel_names.append(channel)
        if channel == 'EOGv' or channel == 'EOGh' or channel == 'Sync' or channel[:3] == 'BIP':
            channel_types.append('misc')
        elif channel == 'EOG':
            channel_types.append('eog')
        else:
            channel_types.append('eeg')
    return channel_names, channel_types
