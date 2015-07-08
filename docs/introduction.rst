Introduction
============

E200 data files are recorded in a directory structure of in Matlab format::

        /nas/nas-li20-pm00/{project}/{year}/{date: YYYYMMDD}/{project}_{dataset number}/{project}_{dataset number}.mat

While Matlab can write HDF5 files, these files may not conform to the HDF5 standard. In order to read them in Python, they must first be translated by Matlab into HDF5, which Python can then load.

The data files follow a hierarchical structure, which is ideal for HDF5. Unfortunately, the de facto Python software for reading and writing HDF5 files is `h5py <http://www.h5py.org/>`.
