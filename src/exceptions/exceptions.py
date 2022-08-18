#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exceptions
"""

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class EventFileError(Exception):
    """
    Exception for an event file error.
    When an event file is of the wrong type (wrong extension) the exception must be thrown.
    """
    pass
