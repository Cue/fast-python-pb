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

"""Compare JSON and protocol buffer serialization times."""

from timeit import Timer

import person_proto
import person_pb2
import json
import simplejson
import cPickle
import lwpb.codec


GETTYSBURG = """
Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in
Liberty, and dedicated to the proposition that all men are created equal.

Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived
and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate
a portion of that field, as a final resting place for those who here gave their lives that that nation might
live. It is altogether fitting and proper that we should do this.

But, in a larger sense, we can not dedicate -- we can not consecrate -- we can not hallow -- this ground.
The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or
detract. The world will little note, nor long remember what we say here, but it can never forget what they did
here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here
have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before
us -- that from these honored dead we take increased devotion to that cause for which they gave the last full
measure of devotion -- that we here highly resolve that these dead shall not have died in vain -- that this
nation, under God, shall have a new birth of freedom -- and that government of the people, by the people, for
the people, shall not perish from the earth.
"""


def useJson():
  "Test serialization using JSON."
  lincoln = {
    'name': 'Abraham Lincoln',
    'birth_year': 1809,
    'nicknames': ['Honest Abe', 'Abe'],
    'facts': {
      'Born In': 'Kentucky',
      'Died In': 'Washington D.C.',
      'Greatest Speech': GETTYSBURG
    }
  }

  serialized = json.dumps(lincoln)

  json.loads(serialized)


def useSimpleJson():
  "Test serialization using SimpleJSON."
  lincoln = {
    'name': 'Abraham Lincoln',
    'birth_year': 1809,
    'nicknames': ['Honest Abe', 'Abe'],
    'facts': {
      'Born In': 'Kentucky',
      'Died In': 'Washington D.C.',
      'Greatest Speech': GETTYSBURG
    }
  }

  serialized = simplejson.dumps(lincoln)
  simplejson.loads(serialized)


def usePb():
  """Test protocol buffer serialization."""
  lincoln = person_proto.Person(name = 'Abraham Lincoln', birth_year = 1809)
  lincoln.nicknames = ['Honest Abe', 'Abe']
  lincoln.facts = [
      person_proto.Fact(name = 'Born In', content = 'Kentucky'),
      person_proto.Fact(name = 'Died In', content = 'Washington D.C.'),
      person_proto.Fact(name = 'Greatest Speech', content = GETTYSBURG)
  ]

  serializedLincoln = lincoln.SerializeToString()

  newLincoln = person_proto.Person()
  newLincoln.ParseFromString(serializedLincoln)


def useStandardPb():
  """Test protocol buffer serialization with native protocol buffers."""
  lincoln = person_pb2.Person(name = 'Abraham Lincoln', birth_year = 1809)
  lincoln.nicknames.extend(['Honest Abe', 'Abe'])

  fact = lincoln.facts.add()
  fact.name = 'Born In'
  fact.content = 'Kentucky'

  fact = lincoln.facts.add()
  fact.name = 'Died In'
  fact.content = 'Washington D.C.'

  fact = lincoln.facts.add()
  fact.name = 'Greatest Speech'
  fact.content = GETTYSBURG

  serializedLincoln = lincoln.SerializeToString()

  newLincoln = person_pb2.Person()
  newLincoln.ParseFromString(serializedLincoln)

def useLWPB(codec):
  """Test protocol buffer serialization with lwpb."""

  lincoln = {
    'name' : 'Abraham Lincoln',
    'birth_year' : 1809,
    'nicknames' : ['Honest Abe', 'Abe'],
    'facts' : [
      { 'name' : 'Born In', 'content' : 'Kentucky' },
      { 'name' : 'Died In', 'content' : 'Washington D.C.' },
      { 'name' : 'Greatest Speech', 'content' : GETTYSBURG },
    ]
  }

  serialized = codec.encode( lincoln )
  newlincoln = codec.decode( serialized )

def useCPickle():
  """Test protocol buffer serialization with cPickle."""

  lincoln = {
    'name' : 'Abraham Lincoln',
    'birth_year' : 1809,
    'nicknames' : ['Honest Abe', 'Abe'],
    'facts' : [
      { 'name' : 'Born In', 'content' : 'Kentucky' },
      { 'name' : 'Died In', 'content' : 'Washington D.C.' },
      { 'name' : 'Greatest Speech', 'content' : GETTYSBURG },
    ]
  }

  serialized = cPickle.dumps( lincoln )
  newlincoln = cPickle.loads( serialized )


lwpb_codec = lwpb.codec.MessageCodec( pb2file="person.pb2", typename="person_proto.Person" )

def useLWPB(codec):
  """Test protocol buffer serialization with lwpb."""

  lincoln = {
    'name' : 'Abraham Lincoln',
    'birth_year' : 1809,
    'nicknames' : ['Honest Abe', 'Abe'],
    'facts' : [
      { 'name' : 'Born In', 'content' : 'Kentucky' },
      { 'name' : 'Died In', 'content' : 'Washington D.C.' },
      { 'name' : 'Greatest Speech', 'content' : GETTYSBURG },
    ]
  }

  serialized = codec.encode( lincoln )
  newlincoln = codec.decode( serialized )


def useCPickle():
  """Test protocol buffer serialization with cPickle."""

  lincoln = {
    'name' : 'Abraham Lincoln',
    'birth_year' : 1809,
    'nicknames' : ['Honest Abe', 'Abe'],
    'facts' : [
      { 'name' : 'Born In', 'content' : 'Kentucky' },
      { 'name' : 'Died In', 'content' : 'Washington D.C.' },
      { 'name' : 'Greatest Speech', 'content' : GETTYSBURG },
    ]
  }

  serialized = cPickle.dumps( lincoln )
  newlincoln = cPickle.loads( serialized )


lwpb_codec = lwpb.codec.MessageCodec( pb2file="person.pb2", typename="person_proto.Person" )


def main():
  """Runs the PB vs JSON benchmark."""
  print "JSON"
  timer = Timer("useJson()", "from __main__ import useJson")
  print timer.timeit(10000)

  """Runs the PB vs SimpleJSON benchmark."""
  print "SimpleJSON"
  timer = Timer("useSimpleJson()", "from __main__ import useSimpleJson")
  print timer.timeit(10000)

  print "Protocol Buffer (fast)"
  timer = Timer("usePb()", "from __main__ import usePb")
  print timer.timeit(10000)

  print "Protocol Buffer (standard)"
  timer = Timer("useStandardPb()", "from __main__ import useStandardPb")
  print timer.timeit(10000)

  print "Protocol Buffer (lwpb)"
  timer = Timer("useLWPB(lwpb_codec)", "from __main__ import useLWPB, lwpb_codec")
  print timer.timeit(10000)

  print "cPickle"
  timer = Timer("useCPickle()", "from __main__ import useCPickle")
  print timer.timeit(10000)


if __name__ == '__main__':
  main()
