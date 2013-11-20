#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Andre Anjos <andre.anjos@idiap.ch>
# Mon 16 Apr 08:18:08 2012 CEST

from setuptools import setup, find_packages

version = '2.0.0a0'

setup(

    name='xbob.db',
    version=version,
    description='Bindings for bob.db',
    url='http://github.com/anjos/xbob.db',
    license='BSD',
    author='Andre Anjos',
    author_email='andre.anjos@idiap.ch',

    long_description=open('README.rst').read(),

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
      'setuptools',
      'xbob.io',
      'xbob.measure',
      'xbob.machine',
      'xbob.trainer',
    ],

    namespace_packages=[
      "xbob",
      ],

    entry_points={
      'console_scripts': [
        'xbob_dbmanage.py = xbob.db.script.dbmanage:main',
        ],

      'xbob.db': [
        'iris = xbob.db.iris.driver:Interface',
        ],

      },

    classifiers = [
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Software Development :: Libraries :: Python Modules',
      ],

    )
