fast-python-pb: Fast Python Protocol Buffers
=====================

Thin wrapper on top of the C++ protocol buffer implementation resulting in significantly faster protocol buffers in
Python.


### Why:

We wanted a fast implementation of protocol buffers that still felt like Python, hence this implementation.

For our use case, this module is up to 15 times faster than the standard one and 10 times as fast as
Python's json serializer.


### Status:

This is a very early stage project.  It works for our needs.  We haven't verified it works beyond that.  Issue reports
and patches are very much appreciated!

For example, it only supports strint, int32, int64, double, and sub message members at this time.


### Pre-requisites:

Install [protocol buffers](http://code.google.com/p/protobuf/)


### Installation:

    git clone https://github.com/Cue/fast-python-pb.git

    cd fast-python-pb

    python setup.py install


### Usage:

    protoc --fastpython_out /output/path --cpp_out /output/path --proto_path your/path your/path/file.proto


### Example:

You can see the example in action in the benchmark directory.

    // person.proto
    package person_proto;

    message Fact {
      required string name = 1;

      required string content = 2;
    }

    message Person {
      required string name = 1;

      required int32 birth_year = 2;

      repeated string nicknames = 3;

      repeated Fact facts = 4;
    }


```python
# example.py
import person_proto

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
```

### One more thing

It's simple, but not that simple. The biggest caveat is that protobuf objects embedded in
other protobuf objects are mutable, but all changes to them are discarded. If you want to
build a protobuf with other protobufs in it, build them separately. To illustrate:

```python
import addressbook_proto

entry = addressbook_proto.Entry(name='Gillian Baskin')
entry.birthplace = addressbook_proto.Location(state='Minnesota', town='Duluth')

# Now, to modify it. Don't do this:
entry.birthplace.town = 'New Town'
# Instead, do this:
birthplace = entry.birthplace
birthplace.town = 'New Town'
entry.birthplace = birthplace
```

There are also several methods for serializing and deserializing. Here's a list:

`ParseFromString(str)` parses from a serialized protobuf stream.

`ParseFromLongString(str)` has the same effect as `ParseFromString(str)`, but is faster
for long strings and slower for short ones. This isn't a huge difference, but could be
important if you're dealing with very large protobufs.

`SerializeToString()` returns the serialized form of the protobuf, as a string.

`SerializeMany(protobufs)` takes a sequence of protobuf objects and serializes them to a
single string. The length of each protobuf is marked, so this can be serialized back to a
list of protobufs.

`ParseMany(str, callback)` takes a string in the format produced by `SerializeMany`, and
calls `callback` with each protobuf object, in order. You can use this to build a list of
protobufs like this:

```python
people = []
addressbook_proto.Person.ParseMany(serializedPeople, people.append)
print people  # Will be a list of Person protobuf objects
```

### Authors:

[Greplin, Inc.](http://www.greplin.com)

[Alan Grow](https://github.com/acg)

[Oliver Tonnhofer](https://github.com/olt)

[Joe Shaw](https://github.com/joeshaw)
