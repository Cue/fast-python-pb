#!/usr/bin/env python

import plugin_pb2

from google.protobuf import descriptor_pb2
from jinja2 import Template
from pkg_resources import resource_string

import os.path
import sys
import tempfile


def main():
  request = plugin_pb2.CodeGeneratorRequest()
  request.ParseFromString(sys.stdin.read())

  response = plugin_pb2.CodeGeneratorResponse()

  parents = set()

  generateFiles = set(request.file_to_generate)
  files = []
  for file in request.proto_file:
    if file.name not in generateFiles:
      continue

    name = file.name.split('.')[0]
    files.append({
        'name': name,
        'package': file.package.lstrip('.')
    })

    context = {
      'fileName': name,
      'moduleName': file.package.lstrip('.'),
      'package': file.package.replace('.', '::'),
      'packageName': file.package.split('.')[-1],
      'messages': file.message_type,
      'TYPE': {
        'STRING': descriptor_pb2.FieldDescriptorProto.TYPE_STRING,
        'DOUBLE': descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE,
        'INT64': descriptor_pb2.FieldDescriptorProto.TYPE_INT64,
        'MESSAGE': descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE
        # TODO(robbyw): More types.
      },
      'LABEL': {
        'REPEATED': descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED
      }
    }

    path = file.package.lstrip('.').split('.')[:-1]
    for i in range(len(path)):
      filePathParts = path[:i+1]
      package = '.'.join(filePathParts)
      filePath = os.path.join(*filePathParts)
      if package not in parents:
        initPy = response.file.add()
        initPy.name = os.path.join('src', filePath, '__init__.py')
        initPy.content = ''
        parents.add(package)

    # Write the C file.
    t = Template(resource_string(__name__, 'template/module.jinjacc'))
    cFile = response.file.add()
    cFile.name = name + '.cc'
    cFile.content = t.render(context)

  # Write setup.py.
  t = Template(resource_string(__name__, 'template/setup.jinjapy'))
  setupFile = response.file.add()
  setupFile.name = 'setup.py'
  setupFile.content = t.render({
    'files': files,
    'parents': parents
  })

  sys.stdout.write(response.SerializeToString())


if __name__ == '__main__':
  main()
