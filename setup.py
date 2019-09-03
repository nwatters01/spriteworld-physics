"""Installation script for setuptools."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import find_packages
from setuptools import setup

setup(
    name='spriteworld-physics',
    version='1.0.1',
    description=('Spriteworld-Physics is a python-based physics simulator '
                 'consisting of a 2-dimensional arena with objects that obey '
                 'simple physical laws.'),
    author='Nicholas Watters',
    url='https://github.com/nwatters01/spriteworld-physics/',
    license='Apache License, Version 2.0',
    keywords=[
        'ai',
        'spriteworld',
        'python',
        'machine learning',
        'objects',
        'physics',
        'simulator',
    ],
    packages=find_packages(),
    install_requires=[
        'absl-py',
        'dm_env',
        'matplotlib',
        'numpy',
        'six',
        'spriteworld',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
)