.. vim: set fileencoding=utf-8 :
.. Thu 13 Oct 2016 10:34:35 CEST

.. _bob.db.base:

============================
 |project| Database Support
============================

.. todolist::

.. todo::
   Improve the documentation by providing a users guide and a development guide.

|project| provides an API to easily query and interface with well known
database protocols. A |project| database contains information about the
organization of the files, functions to query information such as the data
which might be used for training a model, but it usually does **not** contain
the data itself (except for some toy examples). Many of the database packages
provide functionality through data stored in sqlite_ files, whereas the
smallest ones can be stored as filelists.

As databases usually contain thousands of files, and as verification protocols
often require to store information about pairs of files, the size of such
databases can become very large. For this reason, we have decided to
externalize many of them in Satellite Packages.


Documentation
-------------

.. toctree::
   :maxdepth: 2

   extend
   py_api


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. include:: links.rst
