#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Study Plots Listener
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2022"
__credits__ = ["Lemahieu Antoine"]
__license__ = "GNU General Public License v3.0"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class studyPlotsListener(ABC):
    """
    Listener doing the connection between the controller and the view for plotting data of the study.
    It retrieves the information from the view to send it to the controller.
    """

    @abstractmethod
    def cancel_button_clicked(self):
        pass

    @abstractmethod
    def confirm_button_clicked(self):
        pass

    """
    Plots
    """
    # ERPs
    @abstractmethod
    def plot_erps_clicked(self, channels_selected, subjects_selected):
        pass

    # PSD
    @abstractmethod
    def plot_psd_clicked(self, channels_selected, subjects_selected):
        pass

    @abstractmethod
    def plot_spectra_maps_information(self, minimum_frequency, maximum_frequency, minimum_time, maximum_time,
                                      topo_time_points):
        pass

    @abstractmethod
    def plot_spectra_maps_computation_finished(self):
        pass

    @abstractmethod
    def plot_spectra_maps_computation_error(self):
        pass

    @abstractmethod
    def plot_spectra_maps_finished(self):
        pass

    # ERP image
    @abstractmethod
    def plot_erp_image_clicked(self, channels_selected, subjects_selected):
        pass

    # ERSP ITC
    @abstractmethod
    def plot_ersp_itc_clicked(self, channels_selected, subjects_selected):
        pass
