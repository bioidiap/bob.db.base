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

import bob.io.base


class File(object):
  """Abstract class that define basic properties of File objects.
  Your file instance should have at least the self.id and self.path properties."""

  def __init__(self, path, file_id=None):
    """**Constructor Documentation**

    Initialize the File object with the minimum required data.

    Parameters:

    path : str
      The path to this file, relative to the basic directory.
      If you use an SQL database, this should be the SQL type String.
      Please do not specify any file extensions.

    file_id : various type
      The id of the file.
      Its type depends on your implementation.
      If you use an SQL database, this should be an SQL type like Integer or String.
      If you are using an automatically determined file id, you don't need to specify this parameter.
    """

    self.path = path
    """A relative path, which includes file name but excludes file extension"""

    # set file id only, when specified
    if file_id:
      self.id = file_id
      """A unique identifier of the file."""
    else:
      # check that the file id at least exists
      if not hasattr(self, 'id'):
        raise NotImplementedError("Please either specify the file id as parameter, or create an 'id' member variable in the derived class that is automatically determined (e.g. by SQLite)")

  def __lt__(self, other):
    """This function defines the order on the File objects. File objects are always ordered by their ID, in ascending order."""
    return self.id < other.id

  def __repr__(self):
    """This function describes how to convert a File object into a string."""
    return "<File('%s': '%s')>" % (str(self.id), str(self.path))

  def make_path(self, directory=None, extension=None):
    """Wraps the current path so that a complete path is formed

    Keyword Parameters:

    directory
      An optional directory name that will be prefixed to the returned result.

    extension
      An optional extension that will be suffixed to the returned filename. The
      extension normally includes the leading ``.`` character as in ``.jpg`` or
      ``.hdf5``.

    Returns a string containing the newly generated file path.
    """
    # assure that directory and extension are actually strings
    # create the path
    return str(os.path.join(directory or '', self.path + (extension or '')))

  def save(self, data, directory=None, extension='.hdf5', create_directories=True):
    """Saves the input data at the specified location and using the given
    extension. Override it if you need to save differently.

    Keyword Parameters:

    data
      The data blob to be saved (normally a :py:class:`numpy.ndarray`).

    directory
      [optional] If not empty or None, this directory is prefixed to the final
      file destination

    extension
      [optional] The extension of the filename - this will control the type of
      output and the codec for saving the input blob.

    """
    # get the path
    path = self.make_path(directory or '', extension or '')
    # use the bob API to save the data
    bob.io.base.save(data, path, create_directories=create_directories)

  def load(self, directory=None, extension='.hdf5'):
    """Loads the data at the specified location and using the given extension.
    Override it if you need to load differently.

    Keyword Parameters:

    data
      The data blob to be saved (normally a :py:class:`numpy.ndarray`).

    directory
      [optional] If not empty or None, this directory is prefixed to the final
      file destination

    extension
      [optional] The extension of the filename - this will control the type of
      output and the codec for saving the input blob.

    """
    # get the path
    path = self.make_path(directory or '', extension or '')
    return bob.io.base.load(path)
