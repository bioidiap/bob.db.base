.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>
.. Mon  4 Nov 20:58:04 2013 CET

============================
 |project| Database Support
============================

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

.. testsetup:: *

   import xbob.db


Iris Flower Data Set
====================

The `Iris flower data set <http://en.wikipedia.org/wiki/Iris_flower_data_set>`_
or Fisher's Iris data set is a multivariate data set introduced by Sir Ronald
Aylmer Fisher (1936) as an example of discriminant analysis. The dataset
consists of 50 samples from three species of Iris flowers (Iris setosa, Iris
virginica and Iris versicolor). Four features were measured from each sample,
they are the length and the width of sepal and petal, in centimeters.

As this data set is quite small and used for testing purpose, it is directly
integrated into |project|, which provides both ways to access the data, as well
as the data itself (feature vectors of length four for various samples of the
three species).

A description of the feature vector can be obtained using the attribute
:py:attr:`xbob.db.iris.names`.

.. doctest::

   >>> descriptor_labels = xbob.db.iris.names
   >>> descriptor_labels
   ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']

The data (feature vectors) can be retrieved using the :py:meth:`xbob.db.iris.data()`
function. This returns a 3-key dictionary, with 3 :py:class:`numpy.ndarray`
as values, one for each of the three species of Iris flowers.

.. doctest::

  >>> data = xbob.db.iris.data()
  >>> type(data['setosa'])
  <... 'numpy.ndarray'>
  >>> data['setosa'].shape
  (50, 4)
  >>> list(data.keys())
  ['setosa', 'versicolor', 'virginica']

Each :py:class:`numpy.ndarray` consists of 50 feature vectors of length four.

The database also contains statistics about the feature vectors, which can be
obtained using the :py:attr:`xbob.db.iris.stats` dictionary. A description
of these statistics is provided by :py:attr:`xbob.db.iris.stat_names`.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. include:: links.rst

.. Place here your external references

