Full Documentation
==================

Module
------

.. automodule:: E200
   :members:
   :imported-members:

Directly Accessible Classes
---------------------------

.. autoclass:: E200.E200_Image_Iter

Indirectly Accessible Classes
-----------------------------

.. autoclass:: E200.E200_Dat
   :members:
   :exclude-members: uid

.. autoclass:: E200.Data
   :members:

.. autoclass:: E200.Drill
   :members:

   .. attribute:: UID
      
      An array of the :ref:`UIDs <uid>` available.

      *(Note: Typical, may not be present.)*

   .. attribute:: dat

      An array of the data available.

      *(Note: Typical, may not be present.)*

   .. attribute:: desc

      A description of the data.

      *(Note: Typical, may not be present.)*

.. autoclass:: E200.E200_Image
   :members:
   :inherited-members:
   :exclude-members: uid, dat, UID

   .. attribute:: UID

      An array of UIDs.

