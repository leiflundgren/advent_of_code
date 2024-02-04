
from enum import Enum
import stat
from typing import Iterator, Self
import re

import functools
from weakref import ReferenceType

class Node:
    def __init__(self, name, left:Self = None, right:Self = None):
        self.name = name
        self.value = name
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.name} ({str(self.left)}, {str(self.right)})'

    def __repr__(self) -> str:
        return f'Node {str(self)}'

    def __hash__(self) -> int:
        return self.value    
    def __eq__(self, __value: object) -> bool:
        return self.value == __value.value
    def __cmp__(self, other: object) -> int:
        return self.value - other.value

def parse_nodes(lines:Iterator[str]) -> dict[Node]:
    nodes : dict[Node] = {}
    
    def get_node(name:str) -> Node:
        n = nodes.get(name)
        if n is None:
            n = Node(name)
            nodes[name] = n
        return n
    
    def parse_line(s:str) -> Node:
        m = re.search('([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)', s)
        n = get_node(m.group(1))
        l = get_node(m.group(2))
        r = get_node(m.group(3))
        n.left = l
        n.right = r
        return n
    
    for line in lines:
        parse_line(line)
    
    return nodes


class Scenario:
    def __init__(self, directions:str, nodes: dict[str, Node]):
        self.directions = directions
        self.nodes = nodes

def parse_scenario(lines:Iterator[str]) -> Scenario:
    directions = next(lines)
    empty_line = next(lines)
    nodes = parse_nodes(lines)
    return Scenario(directions, nodes)

