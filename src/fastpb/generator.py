#!/usr/bin/env python

import plugin_pb2

from jinja2 import Template
from pkg_resources import resource_string

import os.path
import sys
import tempfile


def main():
  log = sys.stderr

  request = plugin_pb2.CodeGeneratorRequest()
  request.ParseFromString(sys.stdin.read())

  path = tempfile.mkdtemp()

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

    cFilePath = os.path.join(path, name + '.c')
    with open(cFilePath, 'w') as f:
      t = Template(resource_string(__name__, 'template/module.jinja.c'))
      f.write(t.render(context))

  setupPyPath = os.path.join(path, 'setup.py')
  with open(setupPyPath, 'w') as f:
    t = Template(resource_string(__name__, 'template/setup.jinja.py'))
    f.write(t.render({'files': files}))

  print >> log, path


if __name__ == '__main__':
  main()
