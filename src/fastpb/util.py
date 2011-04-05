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

from collections import defaultdict

try:
    from collections import OrderedDict
except ImportError:
    # just ignore the order with Python <2.7 for now
    OrderedDict = dict

def order_dependencies(dependencies):
    """Produce an ordered list of the given dependencies.

    >>> order_dependencies([
    ...     ('a', ('b', 'c')),
    ...     ('b', ('c', )),
    ...     ('c', ()),
    ... ])
    ['c', 'b', 'a']

    Flat dependencies simply yield the original order.

    >>> order_dependencies([
    ...     ('a', ()),
    ...     ('b', ()),
    ...     ('c', ()),
    ... ])
    ['a', 'b', 'c']

    Diamond dependencies are also supported.

    >>> order_dependencies([
    ...     ('a', ('b', 'c')),
    ...     ('b', ('d',)),
    ...     ('c', ('d',)),
    ...     ('d', ()),
    ... ])
    ['d', 'b', 'c', 'a']

    Recursive depdencies (i.e. loops) result in a RuntimeError.

    >>> order_dependencies([
    ...     ('a', ('b')),
    ...     ('b', ('c',)),
    ...     ('c', ('a',)),
    ... ])
    Traceback (most recent call last):
        ...
    RuntimeError: recursive dependency detected
    """
    depends_on = OrderedDict()
    dependent_off = defaultdict(set)
    
    for item, deps in dependencies:
        depends_on[item] = set()
        for dep in deps:
            dependent_off[dep].add(item)
            depends_on[item].add(dep)
    
    result = []
    while depends_on:
        # collect items wihout any dependencies
        for item, dependens in depends_on.iteritems():
            if not dependens: # item without dependencies
                result.append(item)
                del depends_on[item]
                if item in dependent_off:
                    # item resolved -> remove from dependents
                    for dependents in dependent_off[item]:
                        depends_on[dependents].remove(item)
                break # start again to keep general order of dependencies
        else:
            raise RuntimeError('recursive dependency detected')

    return result

if __name__ == "__main__":
    import doctest
    doctest.testmod()
