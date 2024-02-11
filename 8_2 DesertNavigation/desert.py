import itertools
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
        self.loop_length = -1

    def __str__(self) -> str:
        return f'{self.name} ({str(self.left)}, {str(self.right)})'

    def __repr__(self) -> str:
        return f'Node {str(self)}'

    def __hash__(self) -> int:
        return hash(self.value) 
    def __eq__(self, __value: object) -> bool:
        return self.value == __value.value
    def __cmp__(self, other: object) -> int:
        return self.value - other.value
    
    def move(self, dir:str, dbg_print:bool = False) -> Self:
        n = None
        if dir == 'L':
            n = self.left
        elif dir == 'R':
            n = self.right
        else:
            raise ValueError(f'Attempt to move in direction "{dir}"')  
        
        if dbg_print: print(f'{self.name} {dir} --> {n.name}')
        return n
    
    @staticmethod
    def count_moves_to_ending(n: Self, directions:str, dbg_print:bool = False) -> int:
        for i in tools.natural_numbers(0):
            if n.name[-1] == 'Z': return i
            
            d = directions[i%len(directions)]
            nxt = n.move(d, dbg_print)
            n = nxt
            



class Scenario:
    def __init__(self, directions:str, end_char:str = 'Z'):
        self.directions = directions
        self.directions_iter = tools.infinite_iterator(directions)
        
        self.nodes : dict[str, Node] = {}
        self.pos : list[Node] = None
        self.start_pos : list[Node] = None
        self.end_pos : list[Node] = None
        self.end_char = end_char
        
        self.print_move = False
        
    def nodes_ending_with(self, ending, nodes:list[Node] = None) -> list[Node]:
        if nodes is None: nodes = self.nodes.values()
        return list(filter(lambda n: n.value.endswith(ending), nodes))
        
    def at_end_pos(self) -> bool:
        return self.pos == self.end_pos

    def move(self, pos: list[Node], dir:str) -> list[Node]:
        return list(map(lambda n: n.move(dir), pos))

    def walk_to_end(self) -> int:
        steps = 0
        while self.pos != self.end_pos:
            dir = next(self.directions_iter)
            
            p0 = self.pos
            p1 = self.move(p0, dir)
            steps=steps+1
            print(f'{steps}:  {Scenario.print_pos(p0)} -- {dir} --> {Scenario.print_pos(p1)}')
        return steps

    # def find_loops(self) -> list[int]:
    #     looped = []
    #     pos = self.start_pos
    #     for i, dir in zip(tools.natural_numbers(), self.directions_iter):            
    #         ends = self.nodes_ending_with(self.end_char, pos)
    #         for n in ends:
    #             n.loop_length = i
                
    #         looped += ends
    #         pos = list(itertools.filterfalse(set(ends).__contains__, pos))
    #         if len(pos) == 0 :
    #             break

    #         next_pos = list(map(lambda n: n.move(dir, self.print_pos), pos))
    #         pos = next_pos            
                          
    #     return looped

    def find_loops(self, dbg_print:bool = False) -> list[int]:
        return list(map(lambda n: Node.count_moves_to_ending(n, self.directions, dbg_print), self.start_pos))

    def __repr__(self) -> str:
        return f'Scen {str(self)}'
    def __str__(self) -> str:
        return f'pos: [ {Scenario.print_pos(self.pos)} ]'
    @staticmethod
    def print_pos(pos_ls : list[Node])->str:
        return ", ".join(map(lambda n: n.name, pos_ls))
        


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
        m = re.search('(\w{3}) = \((\w{3}), (\w{3})\)', s)
        n = get_node(m.group(1))
        l = get_node(m.group(2))
        r = get_node(m.group(3))
        n.left = l
        n.right = r
        return n
    
    #lines, second = tee(lines)
    #sc.pos = sc.start_pos = parse_line(next(second))
    for line in lines:
        n = parse_line(line)
        #sc.end_pos = n
    
    sc.pos = sc.start_pos = sc.nodes_ending_with('A')
    sc.end_pos = sc.nodes_ending_with('Z')

    return sc



