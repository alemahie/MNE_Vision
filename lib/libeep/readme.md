libeep is python package to load eego datafiles with python.

Take a look at the most recent release at https://github.com/translationalneurosurgery/libeep/releases and you might be lucky and skip the need to compile the binaries.

# Contribution

My tiny contribution stands on the shoulders of the giant Robert Smies, from whom i forked this from https://gitlab.com/smeeze/libeep/. I added instructions and automated the compilation of an installable python package, revised the API for a cleaner object-oriented approach, minimized the risk of locked files and segmentation faults, and expanded the documentation.

# Installation

## Linux / Ubuntu

You might need a recent cmake (tested with cmake 3.17.1) and the `build-essential`, so maybe run first
```
wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | sudo apt-key add -
sudo apt-add-repository 'deb https://apt.kitware.com/ubuntu/ bionic main'
sudo apt-get update
sudo apt-get install cmake
sudo apt-get install build-essential
```  
See also [Kitwares instructions](https://apt.kitware.com/) for installation of cmake. 
Afterwards this should do the trick:
```
make clean python
pip install -e .
```
You will find a file called `pyeep.so` in `build/python/v3`. This is a python extension to load eego files.

## Linux / Arch

You need cmake, e.g. from the snap store (https://snapcraft.io/install/cmake/arch) and base-devel. Afterwards this should do the trick:
```
make clean python
pip install -e .
```

## Windows

In Windows you need Visual Studio with C++ support and CMake installed. Then, from the project root, run in the Developer Command Prompt

```{bash}
mkdir build
cmake -S . -B build
cd build
cmake --build . --config Release
```
You will find a set of files  in `build/python/v3/Release`. This are the python extension files required to load eego files.

Create and install the python package by running from the project root

```{bash}
mkdir libeep
copy build\python\v3\Release\* libeep
copy python\__init__.py libeep
pip install -e .
```

# Usage

## Object-oriented-interface for python

After running `pip install -e .`, you will then be able to import eep and use its object oriented interface.

```{python}
import libeep
import matplotlib.pyplot as plt

fname = "example.cnt"
cnt = libeep.cnt_file(fname)
print(f"Within the file {fname} are")
print(f"{cnt.get_channel_count()} channels and ")
print(f"{cnt.get_sample_count()} samples and")
print(f"{cnt.get_trigger_count()} events")

# load 1s before and after the second event
fs = cnt.get_sample_frequency()
marker, tstamp, *info = cnt.get_trigger(1)
data = cnt.get_samples(tstamp-fs, tstamp+fs)
# plot the data
plt.plot(data)
```


## Low-level interface

Because it is a python extension, `pyeep.so` can also be simply imported with `import pyeep`. If the python package is installed, you can use `from libeep import pyeep`. This does only offer a low-level interface. You can find an example use case [here](python/demo_read_cnt.py) or in the following:

```{python}
import pyeep
fname = "example.cnt"
fh = pyeep.read(fname)  # get the file handle

sampling_rate = pyeep.get_sample_frequency(fh)

chan_count = pyeep.get_channel_count(fh)
channel_labels = [pyeep.get_channel_label(fh, chan) for chan in range(chan_count)]

sample_count = pyeep.get_sample_count(fh) # get how many samples are there
data = pyeep.get_samples(fh, 0, sample_count)  # load them all


trigger_count = pyeep.get_trigger_count(fh)
markers = [pyeep.get_trigger(fh, trigger) for trigger in range(trigger_count)]

```
