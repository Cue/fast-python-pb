fast-python-pb
=====================

Running the benchmark
----------------------------

The latest results on my MacBook pro are:

    JSON
    2.87792301178

    SimpleJSON
    0.56374001503

    Protocol Buffer (fast)
    0.24841094017

    Protocol Buffer (standard)
    3.93004989624

    cPickle
    0.637856960297


### How to run the benchmark

Start all commands in this directory, unless otherwise specified.


Create the fast python pb version:

    mkdir /tmp/personproto

    protoc --fastpython_out /tmp/personproto --cpp_out /tmp/personproto person.proto

    cd /tmp/personproto

    python setup.py install

    cd -


Create the native python version:

    protoc --python_out . person.proto

Compile the .proto for lwpb:

    protoc person.proto -o person.pb2

Run the benchmark:

    python benchmark.py
