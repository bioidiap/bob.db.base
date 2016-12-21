#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Mon 13 Aug 2012 16:19:18 CEST

"""This module defines, among other less important constructions, a management
interface that can be used by Bob to display information about the database and
manage installed files.
"""

import os
import abc
import six


def dbshell(arguments):
  """Drops you into a database shell"""

  if len(arguments.files) != 1:
    raise RuntimeError("Something is wrong this database is supposed to be of type SQLite, but you have more than one data file available: %s" % argument.files)

  if arguments.type == 'sqlite':
    prog = 'sqlite3'
  else:
    raise RuntimeError("Error auxiliary database file '%s' cannot be used to initiate a database shell connection (type='%s')" % (dbfile, arguments.type))

  cmdline = [prog, arguments.files[0]]

  import subprocess

  try:
    if arguments.dryrun:
      print("[dry-run] exec '%s'" % ' '.join(cmdline))
      return 0
    else:
      p = subprocess.Popen(cmdline)
  except OSError as e:
    # occurs when the file is not executable or not found
    print("Error executing '%s': %s (%d)" % (' '.join(cmdline), e.strerror,
        e.errno))
    import sys
    sys.exit(e.errno)

  try:
    p.communicate()
  except KeyboardInterrupt: # the user CTRL-C'ed
    import signal
    os.kill(p.pid, signal.SIGTERM)
    return signal.SIGTERM

  return p.returncode


def dbshell_command(subparsers):
  """Adds a new dbshell subcommand to your subparser"""

  parser = subparsers.add_parser('dbshell', help=dbshell.__doc__)
  parser.add_argument("-n", "--dry-run", dest="dryrun", default=False,
      action='store_true',
      help="does not actually run, just prints what would do instead")
  parser.set_defaults(func=dbshell)


def upload(arguments):
  """Uploads generated metadata to the Idiap build server"""

  import pkg_resources
  basedir = pkg_resources.resource_filename('bob.db.%s' % arguments.name, '')
  assert basedir, "Database and package names do not match. Your declared " \
      "database name should be <name>, if your package is called bob.db.<name>"

  target_file = os.path.join(arguments.destination,
      arguments.name + ".tar.bz2")

  # check all files exist
  for p in arguments.files:
    if not os.path.exists(p):
      raise IOError("Metadata file `%s' is not available. Did you run " \
          "`create' before attempting to upload?" % (p,))

  # if destination exists, try to erase it before
  if os.path.exists(target_file):
    try:
      os.unlink(target_file)
    except Exception as e:
      print("Cannot erase existing file `%s': %s" % (target_file, e))

  # if you get here, all files are there, ready to package
  print("Compressing metadata files to `%s'" % (target_file,))

  # compress
  import tarfile

  f = tarfile.open(target_file, 'w:bz2')
  for k,p in enumerate(arguments.files):
    n = os.path.relpath(p, basedir)
    print("+ [%d/%d] %s" % (k+1, len(arguments.files), n))
    f.add(p, n)
  f.close()

  # set permissions for sane Idiap storage
  import stat
  perms = stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IWGRP|stat.S_IROTH
  os.chmod(target_file, perms)


def upload_command(subparsers):
  """Adds a new 'upload' subcommand to your parser"""

  parser = subparsers.add_parser('upload', help=upload.__doc__)
  parser.add_argument("--destination", default="/idiap/group/torch5spro/databases/latest")
  parser.set_defaults(func=upload)

  return parser


def download(arguments):
  """Downloads and uncompresses meta data generated files from Idiap

  Parameters:

    arguments (argparse.Namespace): A set of arguments passed by the
      command-line parser


  Returns:

    int: A POSIX compliant return value of ``0`` if the download is successful,
    or ``1`` in case it is not.

  """

  # check all files don't exist
  for p in arguments.files:
    if os.path.exists(p):
      if arguments.force:
        os.unlink(p)
      else:
        raise IOError("Metadata file `%s' is already available. Please " \
            "remove self-generated files before attempting download or " \
            "--force" % (p,))

  # if you get here, all files aren't there, unpack
  source_url = os.path.join(arguments.source, arguments.name + ".tar.bz2")

  target_dir = arguments.test_dir #test case

  if not target_dir: #tries to dig it up

    import pkg_resources
    try:
      target_dir = pkg_resources.resource_filename('bob.db.%s' % \
          arguments.name, '')
    except ImportError as e:
      print("The package `bob.db.%s' is not currently installed" % \
          (arguments.name,))
      print("N.B.: The database and package names **must** match. Your " \
          "package should be named `bob.db.%s', if the driver name for your "
          "database is `<name>'")
      return 1

  # download file from Idiap server, unpack and remove it
  import sys
  import tempfile
  import tarfile
  import pkg_resources
  if sys.version_info[0] <= 2:
    import urllib2 as urllib
  else:
    import urllib.request as urllib

  try:
    print ("Extracting url `%s' into `%s'" %(source_url, target_dir))
    u = urllib.urlopen(source_url)
    f = tempfile.NamedTemporaryFile(suffix = ".tar.bz2")
    open(f.name, 'wb').write(u.read())
    t = tarfile.open(fileobj=f, mode='r:bz2')
    t.extractall(target_dir)
    t.close()
    f.close()
    return 0

  except Exception as e:
    print ("Error while downloading: %s" % e)
    return 1


def download_command(subparsers):
  """Adds a new 'download' subcommand to your parser"""

  from argparse import SUPPRESS

  if 'DOCSERVER' in os.environ:
    USE_SERVER=os.environ['DOCSERVER']
  else:
    USE_SERVER='https://www.idiap.ch'

  parser = subparsers.add_parser('download', help=download.__doc__)
  parser.add_argument("--source",
      default="%s/software/bob/databases/latest/" % USE_SERVER)
  parser.add_argument("--force", action='store_true', help = "Overwrite existing database files?")
  parser.add_argument("--test-dir", help=SUPPRESS)
  parser.set_defaults(func=download)

  return parser


def print_files(arguments):
  """Prints the current location of raw database files."""

  print ("Files for database '%s':" % arguments.name)
  for k in arguments.files: print(k)

  return 0


def files_command(subparsers):
  """Adds a new 'files' subcommand to your parser"""

  parser = subparsers.add_parser('files', help=print_files.__doc__)
  parser.set_defaults(func=print_files)

  return parser


def version(arguments):
  """Outputs the database version"""

  print('%s == %s' % (arguments.name, arguments.version))

  return 0


def version_command(subparsers):

  parser = subparsers.add_parser('version', help=version.__doc__)
  parser.set_defaults(func=version)

  return parser


@six.add_metaclass(abc.ABCMeta)
class Interface(object):
  """Base manager for Bob databases

  You should derive and implement an Interface object on every ``bob.db``
  package you create.
  """


  @abc.abstractmethod
  def name(self):
    '''The name of this database

    Returns:

      str: a Python-conforming name for this database. This **must** match the
      package name. If the package is named ``bob.db.foo``, then this function
      must return ``foo``.
    '''

    return


  @abc.abstractmethod
  def files(self):
    '''List of meta-data files for the package to be downloaded/uploaded

    This function should normally return an empty list, except in case the
    database being implemented requires download/upload of metadata files that
    are **not** kept in its (git) repository.

    Returns:

      list: A python iterable with all metadata files needed. The paths listed
      by this method should correspond to full paths (not relative ones) w.r.t.
      the database package implementing it. This is normally achieved by using
      ``pkg_resources.resource_filename()``.

    '''

    return


  @abc.abstractmethod
  def version(self):
    '''The version of this package

    Returns:

      str: The current version number defined in ``setup.py``
    '''

    return


  @abc.abstractmethod
  def type(self):
    '''The type of auxiliary files you have for this database

    Returns:

      str: A string defining the type of database implemented. You can return
      only two values on this function, either ``sqlite`` or ``text``. If you
      return ``sqlite``, then we append special actions such as ``dbshell`` on
      ``bob_dbmanage`` automatically for you. Otherwise, we don't.

    '''

    return


  def setup_parser(self, parser, short_description, long_description):
    '''Sets up the base parser for this database.

    Parameters:

      short_description (str): A short description (one-liner) for this
        database

      long_description (str): A more involved explanation of this database


    Returns:

      argparse.ArgumentParser: a subparser, ready so you can add commands on

    '''

    from argparse import RawDescriptionHelpFormatter

    # creates a top-level parser for this database
    top_level = parser.add_parser(self.name(),
        formatter_class=RawDescriptionHelpFormatter,
        help=short_description, description=long_description)

    type = self.type()
    files = self.files()

    top_level.set_defaults(name=self.name())
    top_level.set_defaults(version=self.version())
    top_level.set_defaults(type=type)
    top_level.set_defaults(files=files)

    subparsers = top_level.add_subparsers(title="subcommands")

    # adds some stock commands
    version_command(subparsers)

    if files:
      upload_command(subparsers)
      download_command(subparsers)

    if type in ('sqlite',):
      dbshell_command(subparsers)

    if files is not None:
      files_command(subparsers)

    return subparsers


  @abc.abstractmethod
  def add_commands(self, parser):
    '''Adds commands to a given :py:class:`argparse.ArgumentParser`

    This method, effectively, allows you to define special commands that your
    database will be able to perform when called from the common driver like
    for example ``create`` or ``checkfiles``.

    You are not obliged to overwrite this method. If you do, you will have the
    chance to establish your own commands. You don't have to worry about stock
    commands such as :py:meth:`files` or :py:meth:`version`. They will be
    automatically hooked-in depending on the values you return for
    :py:meth:`type` and :py:meth:`files`.


    Parameters:

      parser (argparse.ArgumentParser): An instance of a parser that you can
        customize, i.e., call :py:meth:`argparse.ArgumentParser.add_argument`
        on.

    '''

    return


__all__ = ('Interface',)
