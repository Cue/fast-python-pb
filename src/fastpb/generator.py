#!/usr/bin/env python

import plugin_pb2

from jinja2 import Template
from pkg_resources import resource_string

import os.path
import sys
import tempfile


def main():
  request = plugin_pb2.CodeGeneratorRequest()
  request.ParseFromString(sys.stdin.read())

  response = plugin_pb2.CodeGeneratorResponse()

  generateFiles = set(request.file_to_generate)
  files = []
  for file in request.proto_file:
    if file.name not in generateFiles:
      continue

    name = file.name.split('.')[0]
    files.append(name)

    context = {
      'moduleName': name,
      'messages': file.message_type
    }

    # Write the C file.
    t = Template(resource_string(__name__, 'template/module.jinja.c'))
    cFile = response.file.add()
    cFile.name = name + '.c'
    cFile.content = t.render(context)

  # Write setup.py.
  t = Template(resource_string(__name__, 'template/setup.jinja.py'))
  setupFile = response.file.add()
  setupFile.name = 'setup.py'
  setupFile.content = t.render({'files': files})

  sys.stdout.write(response.SerializeToString())


if __name__ == '__main__':
  main()
