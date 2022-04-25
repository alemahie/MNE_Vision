#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File path search
"""

from pathlib import Path

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


def get_project_root_path():
    path = Path(__file__).parent.parent.parent
    return str(path)


def get_project_freesurfer_path():
    return get_project_root_path() + "/data/freesurfer/subjects/"


def get_directory_path_from_file_path(file_path):
    path = Path(file_path).parent
    return str(path)
