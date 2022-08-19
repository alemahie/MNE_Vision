.. -*- mode: rst -*-

|Mne_Vision|

MNE_Vision
==========

MNE Vision is a free and open source software based on MNE_Python_. 
We propose here a graphical interface for MNE, able to perform some of the most common tasks in EEG analysis and processing. 
While also proposing other tools such as the connectivity, and classification with machine learning.

The main objective is to propose a free alternative to EEGLAB_ which requires a MATLAB_ license to fully work.

Documentation
^^^^^^^^^^^^^

MNE_Vision documentation is available `here <https://alemahie.github.io/>`_.

Installing and using MNE_Vision
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two ways to install MNE Vision. 

First, you can download it by doing in a terminal :

.. code-block:: console

    $ pip install mne_vision
    
This requires Python to be installed, if you don't have python installed you can download it from `here <https://www.python.org/downloads/>`_.
    
Once MNE Vision is downloaded, you can launch it from a terminal by doing :

.. code-block:: console

    $ mne_vision
    
    

The second way to download MNE Vision is through the GitHub page (`here <https://github.com/alemahie/MNE_Vision>`_.).

You will first need to install his dependencies.
To do so you can you can open a terminal in the directory where MNE_Vision is stored and type :

.. code-block:: console

    $ pip install requirements.txt

Then, MNE Vision can be launch in a terminal from the directory "path\to\MNE_VISION\" and type :

.. code-block:: console

    $ python3 src/main.py
	
Note : Depending on how python is installed, python3 might need to be replaced by python if python3 is not reconised.

Dependencies
^^^^^^^^^^^^

The required dependencies to run MNE-Python are:

- Python >= 3.9.13
- eeglabio
- keras
- matplotlib
- mne >= 1.0.3
- mne_connectivity >= 0.3
- numpy
- pymatreader
- PyQt5
- PyQt5-stubs
- pyriemann
- pyvista
- pyvistaqt
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
.. _MNE_Vision_GitHub: https://github.com/alemahie/MNE_Vision
.. _MNE_Vision_Documentation: https://alemahie.github.io/

.. |MNE_Vision| image:: image/mne_vision_logo.png
