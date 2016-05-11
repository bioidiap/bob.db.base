#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
# @date:   Thu Dec  6 12:28:25 CET 2012
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os

import bob.db.base.utils

from .file import File


class SQLiteDatabase(object):
  """This class can be used for handling SQL databases.
  It opens an SQL database in a read-only mode and keeps it opened during the whole session."""

  def __init__(self, sqlite_file, file_class):
    """**Contructor Documentation**

    Opens a connection to the given SQLite file and keeps it open through the whole session.

    Keyword parameters:

    sqlite_file : str
      The file name (including full path) of the SQLite file to read or generate.

    file_class : a class instance
      The ``File`` class, which needs to be derived from :py:class:`bob.db.verification.utils.File`.
      This is required to be able to :py:meth:`query` the databases later on.

    Other keyword arguments passed to the :py:class:`bob.db.verification.utils.Database` constructor.
    """

    self.m_sqlite_file = sqlite_file
    if not os.path.exists(sqlite_file):
      self.m_session = None
    else:
      self.m_session = bob.db.base.utils.session_try_readonly('sqlite', sqlite_file)
    # call base class constructor
    # also set the File class that is used (needed for a query)
    # assert the given file class is derived from the File class
    assert issubclass(file_class, File)
    self.m_file_class = file_class

  def __del__(self):
    """Closes the connection to the database when it is not needed any more."""
    if self.is_valid():
      # do some magic to close the connection to the database file
      try:
        # Since the dispose function re-creates a pool
        #   which might fail in some conditions, e.g., when this destructor is called during the exit of the python interpreter
        self.m_session.close()
        self.m_session.bind.dispose()
      except TypeError:
        # ... I can just ignore the according exception...
        pass
      except AttributeError:
        pass

  def is_valid(self):
    """Returns if a valid session has been opened for reading the database."""
    return self.m_session is not None

  def assert_validity(self):
    """Raise a RuntimeError if the database back-end is not available."""
    if not self.is_valid():
      raise IOError("Database of type 'sqlite' cannot be found at expected location '%s'." % self.m_sqlite_file)

  def query(self, *args):
    """Creates a query to the database using the given arguments."""
    self.assert_validity()
    return self.m_session.query(*args)

  def files(self, ids, preserve_order=True):
    """Returns a list of ``File`` objects with the given file ids

    Keyword Parameters:

    ids : [various type]
      The ids of the object in the database table "file".
      This object should be a python iterable (such as a tuple or list).

    preserve_order : bool
      If True (the default) the order of elements is preserved, but the
      execution time increases.

    Returns a list (that may be empty) of ``File`` objects.
    """
    file_objects = self.query(self.m_file_class).filter(self.m_file_class.id.in_(ids))
    if not preserve_order:
      return list(file_objects)
    else:
      path_dict = {}
      for f in file_objects:
        path_dict[f.id] = f
      return [path_dict[id] for id in ids]

  def paths(self, ids, prefix=None, suffix=None, preserve_order=True):
    """Returns a full file paths considering particular file ids, a given
    directory and an extension

    Keyword Parameters:

    ids : [various type]
      The ids of the object in the database table "file". This object should be
      a python iterable (such as a tuple or list).

    prefix : str or None
      The bit of path to be prepended to the filename stem

    suffix : str or None
      The extension determines the suffix that will be appended to the filename
      stem.

    preserve_order : bool
      If True (the default) the order of elements is preserved, but the
      execution time increases.

    Returns a list (that may be empty) of the fully constructed paths given the
    file ids.
    """

    file_objects = self.files(ids, preserve_order)
    return [f.make_path(prefix, suffix) for f in file_objects]

  def reverse(self, paths, preserve_order=True):
    """Reverses the lookup: from certain paths, return a list of
    File objects

    Keyword Parameters:

    paths : [str]
      The filename stems to query for. This object should be a python
      iterable (such as a tuple or list)

    preserve_order : True
      If True (the default) the order of elements is preserved, but the
      execution time increases.

    Returns a list (that may be empty).
    """

    file_objects = self.query(self.m_file_class).filter(self.m_file_class.path.in_(paths))
    if not preserve_order:
      return file_objects
    else:
      # path_dict = {f.path : f for f in file_objects}  <<-- works fine with python 2.7, but not in 2.6
      path_dict = {}
      for f in file_objects:
        path_dict[f.path] = f
      return [path_dict[path] for path in paths]
