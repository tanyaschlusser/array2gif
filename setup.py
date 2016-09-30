#!/usr/bin/env python

import array2gif

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


long_description = open('README.rst').read()
packages = ['array2gif']


setup(
    name=array2gif.core.__title__,
    version=array2gif.core.__version__,
    description='Write a (list of) NumPy array(s) to an (animated) GIF.',
    long_description=long_description,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering :: Visualization'
    ),
    keywords='array2gif animated gif encoder numpy rgb',
    author=array2gif.core.__author__,
    maintainer='Tanya Schlusser',
    url='https://github.com/tanyaschlusser/array2gif',
    license=array2gif.core.__license__,
    packages=packages,
    install_requires=[
        'numpy'
    ]
)
