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
            assert False, 'recursive dependency detected'

    return result

class TestOrderDependencies(object):
    def test_tree(self):
        tree = [
            ('a', ('b', 'c')),
            ('b', ('c', )),
            ('c', ()),
        ]
        assert order_dependencies(tree) == ['c', 'b', 'a']
    
    def test_flat(self):
        tree = [
            ('a', ()),
            ('b', ()),
            ('c', ()),
        ]
        assert order_dependencies(tree) == ['a', 'b', 'c']
    
    def test_diamond(self):
        tree = [
            ('a', ('b', 'c')),
            ('b', ('d',)),
            ('c', ('d',)),
            ('d', ()),
        ]
        assert order_dependencies(tree) == ['d', 'b', 'c', 'a']

    def test_loop(self):
        tree = [
            ('a', ('b')),
            ('b', ('c',)),
            ('c', ('a',)),
        ]
        try:
            order_dependencies(tree)
        except AssertionError:
            pass
        else:
            assert False, 'assertion expected'

