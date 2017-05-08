==========================
 Using |project| databases
==========================

|project| database packages can be used to query databases.
The query can be done both in Python and through the command-line.


The command-line Interface
--------------------------

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
	``bob.db.wine``, and ``bob.db.atnt`` packages are installed.

Each database provides its own custom commands. To see for example what commands
does the ``atnt`` database provide::

	$ bob_dbmanage.py atnt --help
	usage: bob_dbmanage.py atnt [-h]
	                            {version,files,dumplist,checkfiles,reverse,path}
	                            ...


Checking the database files for consistency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the database package is installed, it can be used to check the database for
missing files.::

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
	                        if given, this path will be prepended to every entry
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
