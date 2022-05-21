.. -*- mode: rst -*-

|Mne_Vision|

MNE_Vision
==========

MNE Vision is a open source software mainly based on MNE_Python_ We propose here a graphical interface for MNE, able to perform some of the most common tasks in EEG analysis and processing and available in MNE, while also proposing other tools.

The main objective is to propose a free alternative to EEGLAB_ which requires a MATLAB_ license to fully work.

Documentation
^^^^^^^^^^^^^

`MNE_Vision documentation <docs/build/html/index.html>`_ is available inside the project files on this github.

Installing and using MNE_Vision
^^^^^^^^^^^^^

To use MNE_Vision, you will first need to install his dependencies.
To do so you can you can open a terminal in the directory where MNE_Vision is stored and type :

.. code-block:: console

    $ pip install requirements.txt

This requires Python to be installed, if you don't have python installed you can download it from `here <https://www.python.org/downloads/>`_.

Dependencies
^^^^^^^^^^^^

The required dependencies to run MNE-Python are:

- Python
- keras
- matplotlib
- mayavi
- mne
- mne_connectivity
- numpy
- philistine
- pyEDFlib
- PyQt5
- PyQt6
- PyQtWebEngine
- pyriemann
- scikit_learn
- scipy
- seaborn
- tensorflow

Licensing
^^^^^^^^^

MNE_Vision is **GNU-licenced**, for more information please read the GNU General Public License v3.0.


.. End

.. _EEGLAB: https://sccn.ucsd.edu/eeglab/index.php
.. _MATLAB: https://fr.mathworks.com/products/matlab.html
.. _MNE_Python: https://mne.tools/stable/index.html
.. _Python: https://www.python.org/downloads/

.. |MNE_Vision| image:: image/mne_vision_logo.png
