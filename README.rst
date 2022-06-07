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

Secondly, you will need to install the "libeep" module, for that open a terminal and go to the directory "libeep" under the "lib" directory of the MNE_Vision project.
From there launch the command :

.. code-block:: console

	$ pip install -e .
	
This will install the "libeep" module.

Finally, you may need to add the "lib" directory of the MNE_Vision project to your environment variables.
For that, you can follow the `this tutorial <https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html>`_ on how to add an environment variable.
Under the "System Variables" tab, you can add (or modify if it already exists) the variable "PYTHONPATH" and add the path to the "lib" directory "path\to\MNE_VISION\lib".

Dependencies
^^^^^^^^^^^^

The required dependencies to run MNE-Python are:

- Python >= 3.9.13
- keras >= 2.9.0
- matplotlib >= 3.5.2
- mne >= 1.0.3
- mne_connectivity >= 0.3
- numpy >= 1.22.4
- pymatreader >= 0.0.30
- PyQt5 >= 5.15.6
- PyQt5-stubs >= 5.15.6.0
- pyriemann >= 0.2.7
- pyvista >= 0.34.1
- pyvistaqt >= 0.9.0
- scikit_learn >= 1.1.1
- scipy >= 1.8.1
- seaborn >= 0.11.2
- tensorflow >= 2.9.1

Licensing
^^^^^^^^^

MNE_Vision is **GNU-licenced**, for more information please read the GNU General Public License v3.0.


.. End

.. _EEGLAB: https://sccn.ucsd.edu/eeglab/index.php
.. _MATLAB: https://fr.mathworks.com/products/matlab.html
.. _MNE_Python: https://mne.tools/stable/index.html
.. _Python: https://www.python.org/downloads/

.. |MNE_Vision| image:: image/mne_vision_logo.png


.. Packages en plus : philistine, pyEDFlib, PyQtWebEngine
