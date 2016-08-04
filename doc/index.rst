.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>
.. Mon  4 Nov 20:58:04 2013 CET

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

General functions
+++++++++++++++++

The :py:meth:`bob.db.base.read_annotation_file` method will return a dictionary of annotations of any kind for the given :py:class:`bob.db.base.File`, see :ref:`annotations`.
In case, no annotation is available for the given file, or the database does not define any annotations, ``None`` is returned.


Reference
---------

This section contains the reference guide for :py:mod:`bob.db.base`.

.. automodule:: bob.db.base

Database Handling Utilities
===========================

.. automodule:: bob.db.base.utils

Driver API
==========

.. automodule:: bob.db.base.driver

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. include:: links.rst
