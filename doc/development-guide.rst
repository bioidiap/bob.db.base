.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>

.. _bob.db.base_devguide:

===================
 Development Guide
===================

The best way to create a new database for |project| is by looking at examples.
Name of database inteface packages for |project| usually start with ``bob.db.``.
Take a look at our `satellite packages`_ list to find the available databases.


Although we don't enforce it, most of our existing db package interfaces
provide both a class named ``Database`` and an associated method called
``objects``. The database constructor may take any number of input parameters
but none are standard. The ``objects`` method may take any number of *optional*
arguments allowing the user to sub-select from the total


Low and High-Level Interfaces
-----------------------------

Bob database interfaces come in two levels:

1. **Low-level interfaces** allow developers to create programmatic APIs to
   access samples and metadata available with databases as they are distributed
   by their controllers
2. **High-level interfaces** allow developers to create programmatic APIs to
   *bind* low-level interfaces to frameworks that perform a *specific*
   function.

