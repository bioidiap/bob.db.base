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

from . import utils

from .file import File


class Database(object):
    """Low-level Database API to be used within bob."""

    def check_parameters_for_validity(self, parameters, parameter_description, valid_parameters, default_parameters=None):
        """Checks the given parameters for validity, i.e., if they are contained in the set of valid parameters.
        It also assures that the parameters form a tuple or a list.
        If parameters is 'None' or empty, the default_parameters will be returned (if default_parameters is omitted, all valid_parameters are returned).

        This function will return a tuple or list of parameters, or raise a ValueError.

        Keyword parameters:

        parameters : str, [str] or None
          The parameters to be checked.
          Might be a string, a list/tuple of strings, or None.

        parameter_description : str
          A short description of the parameter.
          This will be used to raise an exception in case the parameter is not valid.

        valid_parameters : [str]
          A list/tuple of valid values for the parameters.

        default_parameters : [str] or None
          The list/tuple of default parameters that will be returned in case parameters is None or empty.
          If omitted, all valid_parameters are used.
        """
        if parameters is None:
            # parameters are not specified, i.e., 'None' or empty lists
            parameters = default_parameters if default_parameters is not None else valid_parameters

        if not isinstance(parameters, (list, tuple, set)):
            # parameter is just a single element, not a tuple or list -> transform it into a tuple
            parameters = (parameters,)

        # perform the checks
        for parameter in parameters:
            if parameter not in valid_parameters:
                raise ValueError("Invalid %s '%s'. Valid values are %s, or lists/tuples of those" % (parameter_description, parameter, valid_parameters))

        # check passed, now return the list/tuple of parameters
        return parameters

    def check_parameter_for_validity(self, parameter, parameter_description, valid_parameters, default_parameter=None):
        """Checks the given parameter for validity, i.e., if it is contained in the set of valid parameters.
        If the parameter is 'None' or empty, the default_parameter will be returned, in case it is specified, otherwise a ValueError will be raised.

        This function will return the parameter after the check tuple or list of parameters, or raise a ValueError.

        Keyword parameters:

        parameter : str
          The single parameter to be checked.
          Might be a string or None.

        parameter_description : str
          A short description of the parameter.
          This will be used to raise an exception in case the parameter is not valid.

        valid_parameters : [str]
          A list/tuple of valid values for the parameters.

        default_parameters : [str] or None
          The default parameter that will be returned in case parameter is None or empty.
          If omitted and parameter is empty, a ValueError is raised.
        """
        if parameter is None:
            # parameter not specified ...
            if default_parameter is not None:
                # ... -> use default parameter
                parameter = default_parameter
            else:
                # ... -> raise an exception
                raise ValueError("The %s has to be one of %s, it might not be 'None'." % (parameter_description, valid_parameters))

        if isinstance(parameter, (list, tuple, set)):
            # the parameter is in a list/tuple ...
            if len(parameter) > 1:
                raise ValueError("The %s has to be one of %s, it might not be more than one (%s was given)." % (parameter_description, valid_parameters, parameter))
            # ... -> we take the first one
            parameter = parameter[0]

        # perform the check
        if parameter not in valid_parameters:
            raise ValueError("The given %s '%s' is not allowed. Please choose one of %s." % (parameter_description, parameter, valid_parameters))

        # tests passed -> return the parameter
        return parameter

    def convert_names_to_highlevel(self, names, low_level_names, high_level_names):
        """
        Converts group names from a low level to high level API
        This is useful for example when you want to return db.groups()
        for the bob.bio.db. Your instance of the database should already have
        self.low_level_names and self.high_level_names initialized.
        """
        if names is None:
            return None
        mapping = dict(zip(low_level_names, high_level_names))
        if isinstance(names, str):
            return mapping.get(names)
        return [mapping[g] for g in names]

    def convert_names_to_lowlevel(self, names, low_level_names, high_level_names):
        """ Same as convert_names_to_highlevel but on reverse """
        if names is None:
            return None
        mapping = dict(zip(high_level_names, low_level_names))
        if isinstance(names, str):
            return mapping.get(names)
        return [mapping[g] for g in names]


class SQLiteDatabase(Database):
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
            self.m_session = utils.session_try_readonly('sqlite', sqlite_file)

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
            except (TypeError, AttributeError, KeyError):
                # ... I can just ignore the according exception...
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

    def uniquify(self, file_list):
        """Sorts the given list of File objects and removes duplicates from it.

        Args:
            file_list: [:py:class:`File`] A list of File objects to be handled. Also other objects can be handled, as long as they are sortable.

        Returns:
            A sorted copy of the given ``file_list`` with the duplicates removed.

        """
        return sorted(set(file_list))

    def all_files(self, **kwargs):
        """Returns the list of all File objects that satisfy your query.
        For possible keyword arguments, please check the :py:meth:`objects` function."""
        return self.uniquify(self.objects(**kwargs))
