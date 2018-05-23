#!/usr/bin/env python

import array2gif

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


long_description = open('README.rst').read()
history = open('HISTORY.rst').read()
packages = ['array2gif']


setup(
    name=array2gif.core.__title__,
    version=array2gif.core.__version__,
    description='Write a (list of) NumPy array(s) to an (animated) GIF.',
    long_description=long_description + '\n\n' + history,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Visualization'
    ),
    keywords='array2gif animated gif encoder numpy rgb',
    author=array2gif.core.__author__,
    author_email='tanya@tickel.net',
    url='https://github.com/tanyaschlusser/array2gif',
    license=array2gif.core.__license__,
    packages=packages,
    install_requires=[
        'numpy'
    ]
)
