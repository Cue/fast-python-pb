fast-python-pb
=====================

Running the benchmark
----------------------------

The latest results on my MacBook pro are:

    JSON
    2.80698990822

    Protocol Buffer
    0.247446775436

    Protocol Buffer (native)
    3.82191610336


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
