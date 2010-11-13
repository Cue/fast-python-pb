#!/usr/bin/env python

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
      # install_requires=['protobuf'],
      package_dir={'fastpb': 'src/fastpb'},
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