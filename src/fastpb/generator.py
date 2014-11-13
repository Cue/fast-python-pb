#!/usr/bin/env python
# Copyright 2011 The fast-python-pb Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Generates a Python wrapper for a C++ protocol buffer."""

import plugin_pb2

from google.protobuf import descriptor_pb2
from fastpb.util import order_dependencies
from jinja2 import Template

# pylint: disable=E0611
from pkg_resources import resource_string

import os.path
import sys


TYPE = {
  'STRING': descriptor_pb2.FieldDescriptorProto.TYPE_STRING,
  'DOUBLE': descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE,
  'FLOAT': descriptor_pb2.FieldDescriptorProto.TYPE_FLOAT,
  'INT32': descriptor_pb2.FieldDescriptorProto.TYPE_INT32,
  'SINT32': descriptor_pb2.FieldDescriptorProto.TYPE_SINT32,
  'UINT32': descriptor_pb2.FieldDescriptorProto.TYPE_UINT32,
  'INT64': descriptor_pb2.FieldDescriptorProto.TYPE_INT64,
  'SINT64': descriptor_pb2.FieldDescriptorProto.TYPE_SINT64,
  'UINT64': descriptor_pb2.FieldDescriptorProto.TYPE_UINT64,
  'MESSAGE': descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE,
  'BYTES': descriptor_pb2.FieldDescriptorProto.TYPE_BYTES,
  'BOOL': descriptor_pb2.FieldDescriptorProto.TYPE_BOOL,
  'ENUM': descriptor_pb2.FieldDescriptorProto.TYPE_ENUM,
  'FIXED32': descriptor_pb2.FieldDescriptorProto.TYPE_FIXED32,
  # TODO(robbyw): More types.
}

LABEL = {
  'REPEATED': descriptor_pb2.FieldDescriptorProto.LABEL_REPEATED
}


def template(name):
  """Gets a template of the given name."""
  return Template(resource_string(__name__, 'template/' + name))


def sort_messages(fileObject):
  """Return a sorted list of messages (sub-messages first).

  This avoids compilation problems involving declaration order.
  """
  dependencies = []
  msgDict = {}

  def visit(baseName, messages, parent=None):
    """Visitor for the message tree."""
    for msg in messages:
      # Build our type name (using the protocol buffer convention) and
      # use it to register this message type object in our dictionary.
      typeName = baseName + '.' + msg.name
      msgDict[typeName] = msg

      # If this is a nested message type, prepend our parent's name to
      # our name for all future name lookups (via template expansion).
      # This disambiguates nested message names so that two n-level
      # messages can both have nested message types with the same name.
      # This also matches the generated C++ code's naming convention.
      if parent is not None:
        msg.name = parent.name + '_' + msg.name

      # If this message has nested message types, recurse.
      if msg.nested_type:
        visit(typeName, msg.nested_type, parent=msg)

      # Generate the set of messages that this type is dependent upon.
      deps = set([field.type_name for field in msg.field
                  if field.type == TYPE['MESSAGE']])
      dependencies.append((typeName, deps))

  # Start by visiting the file's top-level message types.
  visit('.' + fileObject.package, fileObject.message_type)

  sortedMsgNames = order_dependencies(dependencies)
  return [msgDict[n] for n in sortedMsgNames]


def writeCFile(response, name, fileObject):
  """Writes a C file."""
  messages = sort_messages(fileObject)
  context = {
    'fileName': name,
    'moduleName': fileObject.package.lstrip('.'),
    'package': fileObject.package.replace('.', '::'),
    'packageName': fileObject.package.split('.')[-1],
    'messages': messages,
    'enums': fileObject.enum_type,
    'TYPE': TYPE,
    'LABEL': LABEL
  }

  cFile = response.file.add()
  cFile.name = name + '.cc'
  cFile.content = template('module.jinjacc').render(context)


def writeSetupPy(response, files, parents):
  """Writes the setup.py file."""
  setupFile = response.file.add()
  setupFile.name = 'setup.py'
  setupFile.content = template('setup.jinjapy').render({
    'files': files,
    'parents': parents
  })


def writeTests(response, files):
  """Writes the tests."""
  setupFile = response.file.add()
  setupFile.name = 'test.py'
  setupFile.content = template('test.jinjapy').render({
    'files': files,
    'TYPE': TYPE,
    'LABEL': LABEL
  })


def writeManifest(response, files):
  """Writes the manifest."""
  setupFile = response.file.add()
  setupFile.name = 'MANIFEST.in'
  setupFile.content = template('MANIFEST.jinjain').render({
    'files': files
  })


def main():
  """Main generation method."""
  request = plugin_pb2.CodeGeneratorRequest()
  request.ParseFromString(sys.stdin.read())

  response = plugin_pb2.CodeGeneratorResponse()

  parents = set()

  generateFiles = set(request.file_to_generate)
  files = []
  for fileObject in request.proto_file:
    if fileObject.name not in generateFiles:
      continue
    if not fileObject.package:
      sys.stderr.write('%s: package definition required, but not found\n' % fileObject.name)
      sys.exit(1)

    name = fileObject.name.split('.')[0]
    files.append({
      'name': name,
      'package': fileObject.package.lstrip('.'),
      'messages': fileObject.message_type
    })

    path = fileObject.package.lstrip('.').split('.')[:-1]
    for i in range(len(path)):
      filePathParts = path[:i+1]
      package = '.'.join(filePathParts)
      filePath = os.path.join(*filePathParts)
      if package not in parents:
        initPy = response.file.add()
        initPy.name = os.path.join('src', filePath, '__init__.py')
        initPy.content = """
import pkg_resources
pkg_resources.declare_namespace('%s')
""" % package
        parents.add(package)

    # Write the C file.
    writeCFile(response, name, fileObject)

  writeSetupPy(response, files, parents)
  writeTests(response, files)
  writeManifest(response, files)

  sys.stdout.write(response.SerializeToString())


if __name__ == '__main__':
  main()
