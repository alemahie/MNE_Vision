#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stylesheet
"""

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


def get_stylesheet():
    stylesheet = '''
    #RedProgressBar {
        text-align: center;
    }
    #RedProgressBar::chunk {
        background-color: #F44336;
    }
    #GreenProgressBar {
        min-height: 12px;
        max-height: 12px;
        border-radius: 6px;
    }
    #GreenProgressBar::chunk {
        border-radius: 6px;
        background-color: #009688;
    }
    #BlueProgressBar {
        border: 2px solid #2196F3;
        border-radius: 5px;
        background-color: #E0E0E0;
    }
    #BlueProgressBar::chunk {
        background-color: #2196F3;
        width: 10px; 
        margin: 0.5px;
    }
    '''
    return stylesheet
