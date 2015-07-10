.. _api:

API
===

The :mod:`E200` package makes it easy to analyze datasets saved at FACET. In order to do analysis, some understanding of how data can be correlated in practice is necessary. For more information, see the :ref:`introduction`.

.. _loading-data:

Loading Data
------------

Before anything can be done, a dataset must be loaded. When loading data, only data contained in the :ref:`master file <master-file-type>` is loaded immediately. Other data, such as image data, must be loaded later. This is a practical consideration in order to load files quickly and avoid filling up memory, as there can be anywhere from one image to terabytes of images.

Data can be loaded in two main ways. The most accessible way is through :func:`E200.E200_load_data_gui`, which presents the user with a graphical file picker::

        import E200
        data = E200.E200_load_data_gui()

The file path picked is then passed through to :func:`E200.E200_load_data`. This function can, of course, be loaded directly instead of accessed through :func:`E200.E200_load_data_gui`. The function :func:`E200.E200_load_data` loads a file from a string::

        import E200
        filepath = 'nas/nas-li20-pm00/E217/2015/20150606/E217_17990/E217_17990.mat'
        data = E200.E200_load_data(filepath)

.. _data-class:

Drill Data Class
----------------

It becomes immediately obvious that loaded data is returned in the form of the class :class:`E200.classes.Drill`. The dataset's nested dictionary as returned from `h5py <http://www.h5py.org/>`_ is given by::

        data.read_file

It is cumbersome to find all of the nested dictionaries, as tab completion does not work for dictionaries in the Python interpreter. Each nested level must be explored individually::

        >>> list(data.read_file['data'].keys())
        ['VersionInfo', 'processed', 'raw', 'user']

The :class:`E200.classes.Drill` class anticipates this problem: it is far simpler to enter::

        >>> data.rdrill.data
        <E200.E200_load_data.Drill with keys:
        _hdf5
        VersionInfo
        processed
        raw
        user
        >

One can immediately see that this class includes keys. Ignoring ``_hdf5``, which includes the dictionary for this level, the keys are:

* ``VersionInfo``: Information about the :ref:`DAQ <daq>` version used to collect data
* ``raw``: Data and references to data
* ``processed``: Data post-processed by other routines
* ``user``: Space to hold individuals' calculations
  
Of these, only ``raw`` is expected to hold data. Exploring ``raw`` reveals its own levels:

* ``images``: Cameras with images
* ``scalars``: Scalar :ref:`BSA data <bsa-data>` and data indicating :ref:`DAQ <daq>` settings 
* ``metadata``: Data about the dataset collected
* ``arrays``: Multi-dimensional :ref:`BSA data <bsa-data>` (not used)
* ``vectors``: List of :ref:`BSA data <bsa-data>` (not used)

Tree Tips
---------

At the tips of the nested data class are actual data. For instance, ``scalars.step_num`` shows:

        >>> data.rdrill.data.raw.scalars.step_num
        <E200.E200_load_data.Drill with keys:
        _hdf5
        IDtype
        UID
        dat
        desc
        >

Of these, ``UID``, ``dat``, and ``desc`` are interesting:

* ``UID``: An array of the :ref:`UIDs <uid>` available
* ``dat``: An array of the data available
* ``desc``: A description of the data in ``step_num``

This holds true across all tree tips, except for in images, where ``dat`` is a file path to the data. While the file path is relative to the top of the directory holding all of the datasets, we have a way of loading images automatically, and this is not needed by the average analyst.

.. Selecting Data by UID
.. ---------------------

.. Selecting Data by Value
.. -----------------------

.. Loading Images by UID
.. ---------------------

.. _uid:

UID
---

Uids are used to correlate data. Every single shot at FACET is designed to have a unique identification number or :ref:`uid`. Every piece of BSA data, whether it is an image or a number, is correlated to a :ref:`uid`. Nearly 

.. automodule:: E200
   :members:
   :imported-members:

.. autoclass:: E200.classes.Data
   :members:
