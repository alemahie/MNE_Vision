#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File path search
"""

from pathlib import Path

from mne import read_labels_from_annot
from mne.datasets.sample import data_path

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


def get_project_root_path():
    """
    Get the project root path.
    :return: The path to the project root directory.
    :rtype: str
    """
    path = Path(__file__).parent.parent.parent
    return str(path)


def get_project_freesurfer_path():
    """
    Get the project freesurfer path, where the "fsaverage" data is present, used for the source space computations.
    If the path does not exist, create the path and download the files.
    :return: The project freesurfer path.
    :rtype: str
    """
    try:
        subjects_dir = str(data_path(download=False))
        if subjects_dir == ".":
            subjects_dir = None
        else:
            subjects_dir += "/subjects/"
    except FileNotFoundError:   # Path does not exist, create it and download the data.
        subjects_dir = None
    return subjects_dir


def get_directory_path_from_file_path(file_path):
    """
    Get the directory of the file given.
    :param file_path: The path to the file.
    :type file_path: str
    :return: The directory.
    :rtype: str
    """
    path = Path(file_path).parent
    return str(path)


def get_labels_from_subject(subject, subjects_dir):
    """
    Get the labels names from a specific subject.
    :param subject: The subject used by the source space computations.
    :type subject: str
    :param subjects_dir: The directory of the subject used by the source space computations.
    :type subjects_dir: str
    :return: The labels.
    :rtype: list of str
    """
    labels = read_labels_from_annot(subject, parc='aparc', subjects_dir=subjects_dir)
    for i in range(len(labels)):
        if labels[i].name == "unknown-lh":
            del labels[i]
            break
    return labels


def get_image_folder():
    """
    Get the image directory.
    :return: The image directory.
    :rtype: str
    """
    return get_project_root_path() + "/image/"
