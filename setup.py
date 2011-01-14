#!/usr/bin/env python
# Copyright 2010 Greplin, Inc.  All Rights Reserved.

"""Setup script for fast python protocol buffers."""

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

setup(name='fastpb',
      version='0.1',
      description='Fast Python Protocol Buffers',
      license='Apache',
      author='Greplin, Inc.',
      author_email='opensource@greplin.com',
      url='http://www.github.com/Greplin/fast-python-pb',
      package_dir={'': 'src'},
      packages=['fastpb'],
      package_data = {
        'fastpb': ['template/*'],
      },
      entry_points = {
        'console_scripts': [
          'protoc-gen-fastpython = fastpb.generator:main'
        ]
      }
)