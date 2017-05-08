.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>

.. _bob.db.base_userguide:

===========================
 Using |project| Databases
===========================

|project| database packages can be used to query databases for samples and
associated metadata. The queries can be done both in Python or through a
command-line-based application (see :ref:`bob.db.base_devguide`).


.. note::

   We'll use the `AT&T Faces Dataset`_ to examplify database usage and
   development in this guide. This database is small and its raw files can be
   downloaded without an end-user license agreement. The equivalent db package
   interface is implemented in :py:mod:`bob.db.atnt`. If you don't have it
   installed yet, install this package to try out concepts described in this
   guide for yourself.


The Python API
--------------

There are no firm project standards for the pythonic API of a |project| db
package, though we advise package developers to follow guidelines (see
:ref:`bob.db.base_devguide`) which ensure homogeinity through different
packages. Typically, interfaces provide a ``Database`` class allowing the user
to build an object that will be used to access raw data samples (and associated
metadata) available in the dataset, possibly constrained to a number of
selector parameters for sub-selecting samples.

The constructor of a database is pretty much database dependent, but it
generally allows the user to setup installation-dependent parameters such as,
for example, the location where raw data files may be stored, in case those are
not shipped with the |project| db package. Examples in this guide try to
abstract away from such specifities in order to provide a general understanding
of the framework. When specific information is required about a db package
interface, we recommend you read the specific documentation for that package.

Here is an example of a |project| db package interface in use:

.. code-block:: python
   :linenos:

   import bob.db.atnt
   db = bob.db.atnt.Database()
   >>> for sample in db.objects():
   ...     # do something with "sample"

In this example, the user imports the data package (line 1), instantiates the
database (line 2) and then starts iterating over its objects (line 3). Each
object returned by the ``objects()`` method represents one sample from the
database.


Samples
=======

A sample represents one atomic data point from the dataset. For example, this
may mean:

* An image of a person's face in a face recognition database,
* An audio track within a file (with multiple audio tracks) in a speech
  recognition database
* A row in a large file containing measures of flowers (petal width and length)
  representing the measurements for an individual flower
* A phrase in a collection of documents stored in an SQL server

Because sample storage varies from dataset to dataset, it is difficult to
provide a one-fits-all set of tools to read out samples from any kind of
support. |project| provides typical readout routines for samples stored in
files (one-file-per-sample model), while other tools for reading subsets of
data from files are provided by third-party libraries or within the Python
standard library.

The sample abstraction returned in lists through the db package's ``objects()``
method represents an abstraction of this concept and should allow usage of such
objects **independently** of the storage model used by the raw dataset,
allowing the user to, as transparently as possible, access information with
minimal setup.

Currently, among all types of samples implemented through different db packages
in the |project| eco-system, file-based samples are probably the most used. In
a file-based storage, typically, one raw sample corresponds to data stored in a
single file on the file system. Very often, samples are organized in
subdirectories and share a common root installation directory. For example,
this would be a typical organization for an image database:

.. code-block:: text

   $ tree /path/to/root/of/database
   /path/to/root/of/database
   +- directory1
      +- sample1-1.png
      +- sample1-1.txt
      +- sample1-2.png
      +- sample1-2.txt
   +- directory2
      +- sample2-1.png
      +- sample2-1.txt
      +- sample2-2.png
      +- sample2-2.txt

Each sample in this database has the suffix ``.png`` and corresponds to an
image. For each image, there is a matching file containing tag annotations (one
per line) indicating what the image file contains, with the suffix ``.txt``.

If one would be in charge of designing a |project| db package for such an
organization of samples, it is reasonable to expect that:

1. The ``Database`` class constructor to provide a parameter allowing the user
   to re-allocate the root of their own database installation
2. The ``Database`` ``objects()`` method would return samples that allow one to
   load in memory the content of ``.png`` files and *optionally* access
   associated metadata transparently. For example, each sample could have a
   method called ``tags()``, which loaded the content of the text files and
   returned the text tags in a python list

In this context, samples encompass *abstractions* allowing users to load
information from raw datasets without writing code to do so. #STOPPED HERE


Each sample in the database in turn, provides a number of methods
to access information about its raw or meta-data, allowing the user to create a
*continuous processing* pipeline.

Database sample objects often provide a ``load()`` allowing the
pointed object to be loaded in memory:

.. code-block:: python

   import bob.db.atnt
   db = bob.db.atnt.Database()
   all_images = []
   >>> for sample in db.objects():
   ...     all_images.append(sample.load())

In the example above, the user loads the object pointed by
:py:mod:`bob.db.atnt`'s image samples using their ``load()`` method,
accumulating (in memory) all images available in the dataset. While

The task of the |project| db package implementation is to *bridge*
the raw file storage with your Python scripts so you can script data traversal
and loading.



Usage
=====

The usage of a db package API normally goes through 3 stages:

1. Construct a ``Database`` object
2. Use the ``Database.objects()`` method to query for samples
3. Use the returned list of samples in your application

You




The command-line Interface
--------------------------

The
programmatic API of each database should be consulted on their own packages.
The command-line interfaces are centralized through a common application called
``bob_dbmanage.py``.

A command-line script is provided to manage the installed databases::

	$ bob_dbmanage.py --help
	usage: bob_dbmanage.py [-h]
	                       {iris,mnist,wine,atnt,all}
	                       ...

	This script drives all commands from the specific database subdrivers.

	optional arguments:
	  -h, --help            show this help message and exit

	databases:
	  {iris,mnist,wine,atnt,all}
	    iris                Fisher's Iris Flower dataset
	    mnist               MNIST database
	    wine                Wine dataset
	    atnt                AT&T/ORL Face database
	    all                 Drive commands to all (above) databases in one shot

	  For a list of available databases:
	  >>> bob_dbmanage.py --help

	  For a list of actions on a database:
	  >>> bob_dbmanage.py <database-name> --help

.. note::

	To use a particular database in |project|, its respective package must be
	installed. For example, here ``bob.db.iris``, ``bob.db.mnist``,
	``bob.db.wine``, and ``bob.db.atnt`` packages are installed. Packages
  should be installed following our standard installation instructions.

Typically, database packages provide a standard set of commands allowing basic
probing of their metadata, though each database *can* provide its own set of
custom commands. To see for example what commands the ``atnt`` database
provide, use the following command line::

	$ bob_dbmanage.py atnt --help
	usage: bob_dbmanage.py atnt [-h]
	                            {version,files,dumplist,checkfiles,reverse,path}
	                            ...


Checking the database files for consistency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the database package is installed, it can be used to check the database
for missing files.::

	$ bob_dbmanage.py atnt checkfiles --help
	usage: bob_dbmanage.py atnt checkfiles [-h] -d DIRECTORY [-e EXTENSION]

	optional arguments:
	  -d DIRECTORY, --directory DIRECTORY
	                        the path to the AT&T images.

	$ bob_dbmanage.py atnt checkfiles --directory /path/to/orl_faces


Generating file lists for experiments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

File lists can be obtained from the database interfaces to be used in other
scripts for running experiments.::

	$ bob_dbmanage.py atnt dumplist --help
	usage: bob_dbmanage.py atnt dumplist [-h] [-d DIRECTORY] [-e EXTENSION]
	                                     [-C {ClientID}]
	                                     [-g {world,dev}] [-p {enroll,probe}]

	optional arguments:
	  -d DIRECTORY, --directory DIRECTORY
	 To simplify maintenance and improve homogeneity between different db
   packages, we further suggest you follow                        if given, this path will be prepended to every entry
	                        returned.
	  -e EXTENSION, --extension EXTENSION
	                        if given, this extension will be appended to every
	                        entry returned.
	  -g {world,dev}, --group {world,dev}
	                        if given, this value will limit the output files to
	                        those belonging to a particular group.

	$ bob_dbmanage.py atnt dumplist -d /path/to/orl_faces -e .pgm --group dev
	/path/to/orl_faces/s32/9.pgm
	/path/to/orl_faces/s32/2.pgm
	...


.. note::

	Each database provides its own **custom** interface through
	``bob_dbmanage.py``. To see what commands are available and what do they do,
	``bob_dbmanage.py <database-name> --help`` and
	``bob_dbmanage.py <database-name> <custom-command> --help`` must be used.


Issuing a common command for all databases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run a command on available database, the ``all`` option can be used.::

	$ bob_dbmanage.py all --help
	usage: bob_dbmanage.py all [-h] {files,upload,download,create,version} ...

	Using this special database you can command the execution of available
	commands to all other databases at the same time.

	optional arguments:
	  -h, --help            show this help message and exit

	subcommands:
	  {files,upload,download,create,version}
	    files               Prints the current location of raw database files.
	    upload              Uploads generated metadata to the Idiap build server
	    download            Downloads and uncompresses meta data generated files
	                        from Idiap Parameters: arguments (argparse.Namespace):
	                        A set of arguments passed by the command-line parser
	                        Returns: int: A POSIX compliant return value of ``0``
	                        if the download is successful, or ``1`` in case it is
	                        not. Raises: IOError: if metafiles exist and
	                        ``--force`` was not passed urllib2.HTTPError: if the
	                        target resource does not exist on the webserver
	    create              create all databases with default settings
	    version             Outputs the database version


Download Missing Files for Large Databases
------------------------------------------

Most databases which are large enough contain their information in separate
files (usually an SQL database) which might not be shipped with the database
package because of their size. However, ``bob_dbmanage.py`` can be used to
download the extra required files.::

	$ bob_dbmanage.py <database-name> download

or to download the missing files of all installed databases::

	$ bob_dbmanage.py all download --missing

.. note::

	The original database files as in **the data** is almost never included in
	the database package. The data files of the database must be obtained
	separately and manually.


The Python interface
--------------------

Each database inherits from :py:class:`bob.db.base.Database` and contains an
``objects`` method which returns the samples of the database. Each sample is an
instance of :py:class:`bob.db.base.File` and contains (at least) an attribute,
``path``, which is a unique string that represents the sample.

.. note::

    Historically, since each sample was stored in a separate file in databases,
    the :py:class:`bob.db.base.File` class is called ``File`` while it refers to
    a sample rather than a file. A file in a database can contain several
    samples or a sample can come from somewhere else (e.g. memory) rather than a
    file. While in most cases ``File.path`` represents an actual path to a file,
    this mainly is just a unique string that represents the sample. To load the
    data of a sample, you should use :py:meth:`bob.db.base.File.load`.


Since there is no mandated API, each database's interface can be different.
Please refer to the database's documentation for more information. Here is an
example for the :ref:`bob.db.atnt`:

.. code-block:: python

	>>> import bob.db.atnt
	>>> db = bob.db.atnt.Database(original_directory='/path/to/orl_faces', original_extension='.pgm')

Calling ``objects`` with no arguments returns all the samples of the
database. Use :py:func:`help` to find out more.

.. code-block:: python

	>>> help(db.objects)
	>>> db.objects()
	[<File('9': 's1/9')>, ..., <File('396': 's40/6')>]

Samples returned by the ``objects`` method are instances of :py:class:`bob.db.base.File` which provide several methods:

.. code-block:: python

	>>> sample = db.objects()[0]
	>>> sample
	<File('9': 's1/9')>
	>>> sample.path
	's1/9'
	>>> sample.id
	9
	>>> sample.client_id
	1
	>>> sample.make_path(db.original_directory, db.original_extension)
	'/path/to/orl_faces/s1/9.pgm'
	>>> image = sample.load(db.original_directory, db.original_extension)# doctest: +SKIP
	>>> image
	array([[42, 41, 44, ..., 50, 49, 57],
	       [41, 41, 43, ..., 51, 53, 53],
	       [54, 40, 43, ..., 49, 52, 53],
	       ...,
	       [38, 37, 36, ..., 40, 43, 40],
	       [38, 36, 37, ..., 44, 42, 39],
	       [37, 39, 37, ..., 42, 43, 41]], dtype=uint8)


.. include:: links.rst
