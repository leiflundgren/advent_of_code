import tools
from enum import Enum
import stat
from typing import Iterator, Self
import re
from itertools import tee
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



class Scenario:
    def __init__(self, directions:str):
        self.directions = directions
        self.directions_iter = tools.infinite_iterator(directions)
        
        self.nodes : dict[str, Node] = {}
        self.pos : Node = None
        self.start_pos : Node = None
        self.end_pos : Node = None
        

    def __next__(self) -> Node :
        dir = next(self.directions_iter)
        if dir == 'L':
            self.pos = self.pos.left
            return self.pos
        elif dir == 'R':
            self.pos = self.pos.right
            return self.pos
        else:
            raise ValueError(f'Attempt to move in direction "{dir}"')


    def walk_to_end(self) -> int:
        steps = 0
        while self.pos != self.end_pos:
            p0 = self.pos
            p1 = next(self)
            steps=steps+1
            print(f'{steps}:  {p0.name} --> {p1.name}')
        return steps


def parse_scenario(lines:Iterator[str]) -> Scenario:

    directions = next(lines)
    empty_line = next(lines)
    
    sc = Scenario(directions)
        

    def get_node(name:str) -> Node:
        n = sc.nodes.get(name)
        if n is None:
            n = Node(name)
            sc.nodes[name] = n
        return n
    
    def parse_line(s:str) -> Node:
        m = re.search('([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)', s)
        n = get_node(m.group(1))
        l = get_node(m.group(2))
        r = get_node(m.group(3))
        n.left = l
        n.right = r
        return n
    
    lines, second = tee(lines)
    sc.pos = sc.start_pos = parse_line(next(second))
    for line in lines:
        n = parse_line(line)
        sc.end_pos = n
    
    return sc



