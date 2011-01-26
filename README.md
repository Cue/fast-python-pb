fast-python-pb
=====================

Fast Python Protocol Buffers
----------------------------

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

    git clone https://github.com/Greplin/fast-python-pb.git

    cd fast-python-pb

    python setup.py install


### Usage:

    protoc --fastpython_out /output/path --cpp_out /output/path --proto_path your/path your/path/file.proto


### Example:

You can see the example in action in the benchmark directory.

person.proto

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


example.py

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



### Authors:

[Greplin, Inc.](http://www.greplin.com)
