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

from functools import reduce

try:
    from collections import OrderedDict
except ImportError:
    # just ignore the order with Python <2.7 for now
    OrderedDict = dict

class CyclicError(Exception):
    pass

def order_dependencies(dependencies):
    """Produce a topologically-sorted list of the given dependencies.

    >>> list(order_dependencies([
    ...     ('a', set(['b', 'c'])),
    ...     ('b', set(['c'])),
    ...     ('c', set()),
    ... ]))
    ['c', 'b', 'a']

    Flat dependencies simply yield the original order.

    >>> list(order_dependencies([
    ...     ('a', set()),
    ...     ('b', set()),
    ...     ('c', set()),
    ... ]))
    ['a', 'b', 'c']

    Nested and diamond dependencies are also supported.

    >>> list(order_dependencies([
    ...     ('a', set()),
    ...     ('b', set(['c', 'd'])),
    ...     ('c', set()),
    ... ]))
    ['a', 'c', 'd', 'b']
    >>> list(order_dependencies([
    ...     ('a', set(['b', 'c'])),
    ...     ('b', set(['d'])),
    ...     ('c', set(['d'])),
    ...     ('d', set()),
    ... ]))
    ['d', 'b', 'c', 'a']

    An empty dependency list results in an empty generator sequence.

    >>> list(order_dependencies([]))
    []

    Cyclic dependencies result in a CyclicError.

    >>> list(order_dependencies([
    ...     ('a', set(['b'])),
    ...     ('b', set(['c'])),
    ...     ('c', set(['a'])),
    ... ]))
    Traceback (most recent call last):
        ...
    CyclicError: A cyclic dependency exists amongst {'a': set(['b']), 'c': set(['a']), 'b': set(['c'])}

    Based on toposort2() by Paddy McCarthy.
    (see http://code.activestate.com/recipes/577413-topological-sort/)
    """
    data = OrderedDict(dependencies)

    # Ignore self dependencies.
    for k, v in data.items():
        v.discard(k)

    # If we're out of data, return (and produce an empty generator sequence).
    if not data:
        return

    # Add top-level keys for any unrepresented values.
    for item in reduce(set.union, data.values()) - set(data.keys()):
        data[item] = set()

    while True:
        ordered = set(item for item, dep in data.items() if not dep)
        if not ordered:
            break
        for dep in sorted(ordered):
            yield dep

        remaining = {}
        for item, dep in data.iteritems():
            if item not in ordered:
                remaining[item] = (dep - ordered)
        data = remaining

    if data:
        raise CyclicError('A cyclic dependency exists amongst %r' % dict(data))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
