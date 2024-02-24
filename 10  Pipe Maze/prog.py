from collections import deque
from collections.abc import Iterable
from dataclasses import field
import itertools
from operator import contains
import typing
from xmlrpc.client import TRANSPORT_ERROR
import tools
from enum import Enum, StrEnum
from typing import Iterator, Self
import re
from itertools import tee
import functools
from copy import deepcopy


def direction(p1:tuple[int,int], p2:tuple[int,int]) -> str:
    (x1, y1) = p1
    (x2, y2) = p2
    if y1 != y2:
        return 'N' if y1 > y2 else 'S'
    if x1 != x2:
        return 'S' if x1 > x2 else 'E'
    raise ValueError(f'Innvalid direction {p1}->{p2}')

def opposite_direction(dir:str) -> bool :
    if dir == 'N': return 'S'
    if dir == 'S': return 'N'
    if dir == 'E': return 'W'
    if dir == 'W': return 'E'


class Pipe:
    def __init__(self, parse_char:str, print_char:str, name:str, has_pipe:bool, has_W:bool, has_E:bool, has_N:bool, has_S:bool):
        self.parse_char = parse_char
        self.print_char = print_char
        self.name = name
        self.has_pipe = has_pipe
        self.has_E = has_E
        self.has_W = has_W
        self.has_N = has_N
        self.has_S = has_S
            
    def __repr__(self) -> str:
        return self.print_char
    
    def has_direction(self, dir:str) -> bool :        
        def inner():
            if dir == 'N': return self.has_N
            if dir == 'S': return self.has_S
            if dir == 'E': return self.has_E
            if dir == 'W': return self.has_W
            raise ValueError(f'Innvalid direction {dir}')
        
        has = inner()
        return has is None or has # None is wildcard
    
    @staticmethod
    def directions_connect(p1: Self, p2: Self) -> bool:
        if p1.x == p2.x and p2.y == p1.y: return False # same nodes
        if abs(p1.x-p2.x) != 1 or abs(p1.y-p2.y) != 1: return False
        
        dir = direction(p1, p2)
        return p1.has_direction(dir) and p2.has_direction(opposite_direction(dir))

PIPE_VERTICAL = Pipe('|', '┃', 'N-S', True, False, False, True, True) # is a vertical pipe connecting north and south.
PIPE_HORIZONTAL = Pipe('-', '━', 'W-E', True, True, True, False, False) # is a horizontal pipe connecting east and west.
PIPE_BEND_N_E = Pipe('L', '┖', 'N-E', True, False, True, True, False) # is a 90-degree bend connecting north and east.
PIPE_BEND_N_W = Pipe('J', '┛', 'N-W', True, True, False, True, False) # is a 90-degree bend connecting north and west.
PIPE_BEND_S_W = Pipe('7', '┒', 'S-W', True, True, False, False, True) # is a 90-degree bend connecting south and west.
PIPE_BEND_S_E = Pipe('F', '┎', 'S-E', True, False, True, False, True) # is a 90-degree bend connecting south and east.
PIPE_NO_PIPE = Pipe('.', '·', 'empty', False, False, False, False, False) # is ground; there is no pipe in this tile.
PIPE_START = Pipe('S', 'S', 'start', None, None, None, None, None) # is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
PIPE_OUTSIDE = Pipe('O', 'O', 'outside', False, False, False, False, False) 
PIPE_INSIDE = Pipe('I', 'I', 'inside', False, False, False, False, False) 

ALL_PIPES = [ PIPE_VERTICAL,PIPE_HORIZONTAL,PIPE_BEND_N_E ,PIPE_BEND_N_W ,PIPE_BEND_S_W ,PIPE_BEND_S_E ,PIPE_NO_PIPE ,PIPE_START ]

def parse_pipe(c:str) -> Pipe:
    for p in ALL_PIPES:
        if p.parse_char == c:
            return p
    raise ValueError('Unknown pipe', c)

# None used to make Start connect to anything
def can_connect_horizontal(left:Pipe, right:Pipe) -> bool:
    return (left.has_E is None or left.has_E) and (right.has_W is None or right.has_W)
def can_connect_vertical(top:Pipe, bottom:Pipe) -> bool:
    return (top.has_S is None or top.has_S) and (bottom.has_N is None or bottom.has_N)
    

Node = typing.NewType('Node', None)

def sort_nodes_cmp(n1:Node, n2:Node) -> int:

    if n1.y != n2.y: return n2.y - n1.y
    return n2.x - n1.x

def sort_nodes(nodes : Iterable[Node]) -> Iterable[Node] :
    return sorted(nodes, key=functools.cmp_to_key(sort_nodes_cmp))

class Field:
    def __init__(self, field_matrix : list[list[Node]] = None):
        self.field : dict[tuple[int, int], Node] = {}
        
        if not field_matrix is None:
            for ls in field_matrix:
                for n in ls:
                    if not n is None:
                        self.set(n.x, n.y, n)
                        
        self.set_bounds()

    def get(self, x:int, y:int) -> Node:
        # if outside, return a freshly minted no-pipe
        return self.field.get((x, y), Node(self, PIPE_NO_PIPE, x, y))

    def set(self, x:int, y:int, n:Node) -> None:
        self.field[(x, y)] = n
        self.bounds = None
    
    def get_bounds(self)  -> tuple[tuple[int, int], tuple[int,int]]:
        if self.bounds is None:
            self.set_bounds()
        return self.bounds

    def set_bounds(self) -> None:
        if 0 == len(self.field):
            self.bounds = ((0,0), (0,0))
            return
        
        first = next(iter(self.field.values()))
        max_x = min_x = first.x
        max_y = min_y = first.y
        for n in self.field.values():
            min_x = min(n.x,min_x)
            min_y = min(n.y,min_y)
            max_x = max(n.x,max_x)
            max_y = max(n.y,max_y)
            
        self.bounds = ((min_x, min_y), (max_x, max_y))

    def is_inside_bounds(self, x:int, y:int) -> bool:
        ((min_x, min_y), (max_x,max_y)) = self.get_bounds()
        return min_x <= x and x <= max_x and min_y <= y and y <= max_y

    def all_nodes(self) -> list[Node]:
        return list(sort_nodes(self.field.values()))
    
    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        def y_to_str(ls: list[Node]) -> str:
            return ''.join(map(lambda n: str(n), ls))

        ((min_x, min_y), (max_x,max_y)) = self.get_bounds()
        
        field = []
        for y in range(min_y, 1+max_y):
            field.append( [PIPE_NO_PIPE] * (max_x+1-min_x))
        

        # xlen = max_x -min_x + 1
        # ylen = max_y -min_y + 1
        # line = PIPE_NO_PIPE.print_char * xlen + '\n'
        # field = line * ylen
        
        for n in self.field.values():
            field[n.y-1][n.x-1] = n

        lines = list(map(y_to_str, field))
        return '\n'.join(lines)
    
    def get_start_pos(self) -> Node:
        return next(filter(lambda n: n.value == PIPE_START, self.all_nodes()), None)
    
    def nodes_between(self, n1:Node, n2:Node) -> list[Node]:
        if n1 is n2:
            return []
        if n1.x != n2.x and n1.y != n2.y: # only straight lines
            return []
        if n1.x == n2.x: # vertical
            return [ self.get(n1.x, y) for y in range(min(n1.y, n2.y)+1, max(n1.y, n2.y)) ]
        else: #horizontal
            return [ self.get(x, n1.y) for x in range(min(n1.x, n2.x)+1, max(n1.x, n2.x)) ]
 
    # direction to move from n1 to n2
    def direction(self, n1:Node, n2:Node) -> str:
        if n1.x != n2.x and n1.y != n2.y: # only straight lines
            return None 
        if n1.x == n2.x and n1.y == n2.y: # same nodes
            return None 
            
        if n1.x == n2.x:
            return 'S' if n1.y < n2.y else 'N'
        elif n1.y == n2.y:
            return 'E' if n1.x < n2.x else 'W'
        else: 
            return None

    def path_between(self, n1:Node, n2:Node) -> bool:
        dir = self.direction(n1, n2)
        if dir is None: return False
        n = n1
        while not n is None and n != n2:
            n = n.sneak(dir)
        return not n is None

        # between = self.nodes_between(n1, n2)
        # if len(between) == 0: return False
    
        # is_horizontal = n1.x == n2.x
        # if is_horizontal:
        #     return all(map(lambda n: n.value.has_E or n.value.has_W, between))
        # else:
        #     return all(map(lambda n: n.value.has_N or n.value.has_S, between))
        
    
class Node:
    def __init__(self, field:Field, value:Pipe, x:int, y:int, tag = None):
        assert isinstance(field, Field)
        self.field = field
        self.value = value
        self.x = x
        self.y = y
        self.tag = tag
       
    def __str__(self) -> str:
        return self.value.print_char

    def __repr__(self) -> str:
        return f'Node [{self.x},{self.y}] {self.value}'
    
    def __eq__(self, __value: object) -> bool:
        return self.x == __value.x and self.y == __value.y

    def copy(self, field:Field) -> Self:
        return Node(field, self.value, self.x, self.y, self.tag)

    @staticmethod
    def clear_tags(thing) -> None:
        if isinstance(thing, Node):
            thing.tag = None
        else:
            for n in thing:
                Node.clear_tags(n)

    def move_coords(self, dir:str) -> Self:
        if dir == 'N': return (self.x, self.y-1)
        if dir == 'S': return (self.x, self.y+1)
        if dir == 'W': return (self.x-1, self.y)
        if dir == 'E': return (self.x+1, self.y)
        raise ValueError(f'Innvalid direction {dir}')

    def connect(self, dir:str) -> Self:
        if dir == 'N': return self.connect_N()
        if dir == 'S': return self.connect_S()
        if dir == 'E': return self.connect_E()
        if dir == 'W': return self.connect_W()
        raise ValueError(f'Innvalid direction {dir}')

    def connect_W(self) -> Self:
        if not self.field.is_inside_bounds(self.x-1, self.y): return None
        n = self.field.get(self.x-1, self.y)
        return n if can_connect_horizontal(n.value, self.value) else None
    def connect_E(self) -> Self:
        if not self.field.is_inside_bounds(self.x+1, self.y): return None
        n = self.field.get(self.x+1, self.y)
        return n if can_connect_horizontal(self.value, n.value) else None
    def connect_N(self) -> Self:
        if not self.field.is_inside_bounds(self.x, self.y-1): return None
        n = self.field.get(self.x, self.y-1)
        return n if can_connect_vertical(n.value, self.value) else None
    def connect_S(self) -> Self:
        if not self.field.is_inside_bounds(self.x, self.y+1): return None
        n = self.field.get(self.x, self.y+1)
        return n if can_connect_vertical(self.value, n.value) else None

    def connect_one(self) -> list[Self]:
        # res = []
        # for dir in 'NSEW':
        #     n = self.connect(dir)
        #     res.append(n)
        # return list(filter(lambda n: not n is None, res))
        return list(filter(lambda n: not n is None, map(lambda dir: self.connect(dir), 'NSEW')))
    
    def sneak_W(self)->Self:
        n = self.connect_W()
        if n is None: return None
        if not self.value.has_pipe and not n.value.has_pipe: return n # without pipes, sneak free
        if not n.value.has_E: return None
        return n 
    def sneak_E(self)->Self:
        n = self.connect_E()
        if n is None: return None
        if not self.value.has_pipe and not n.value.has_pipe: return n # without pipes, sneak free
        if not n.value.has_W: return None
        return n 
    def sneak_N(self)->Self:
        n = self.connect_N()
        if n is None: return None
        if not self.value.has_pipe and not n.value.has_pipe: return n # without pipes, sneak free
        if not n.value.has_S: return None
        return n 
    def sneak_S(self)->Self:
        n = self.connect_S()
        if n is None: return None
        if not self.value.has_pipe and not n.value.has_pipe: return n # without pipes, sneak free
        if not n.value.has_N: return None
        return n 
    
    def sneak(self, dir:str) -> Self:
        (x,y) = self.move_coords(dir)
        if not self.field.is_inside_bounds(x,y): return None
        
        n = self.field.get(x,y)

        if not self.value.has_pipe and not n.value.has_pipe: return n # without pipes, sneak free

        if not Pipe.directions_connect(self, n): return None

        return n

    def sneak_one(self) -> list[Self]:
        return list(filter(lambda n: not n is None, map(lambda dir: self.sneak(dir), 'NSEW')))
    
    def coonnected_neighbors(self) -> list[Self]:
        valid_dir = list( filter( lambda d: not self.connect(d) is None, 'NSEW'))
        return list(map( lambda d: self.connect(d), valid_dir))
    
def ParseField(str_field:str) -> Field:
    lines = str_field.split('\n')
    y_len = len(lines)
    x_len = len(lines[0])
    
    has_outer = all(map(lambda c: c=='.', lines[0]))

    field = Field(list(map(lambda _: [None]*x_len, [None]*y_len)))
    for y in range(y_len):
        for x in range(x_len):
            p = parse_pipe(lines[y][x])
            n = Node(field, p, x, y)
            field.set(x, y, n)
    return field

def clear_non_loop(orig:Field, loop:list[Node]) -> Field:
    field = Field()    
    for n in loop:
        field.set(n.x, n.y, n.copy(field))
    return field

def find_loop(start:Node) -> list[Node]:
    assert isinstance(start, Node)
    Node.clear_tags(start.field.all_nodes())
    
    loop = []
    n = start
    while True:
        loop.append(n)
        n.tag = True
        neighbors = n.coonnected_neighbors()
        # nexts = list(filter(lambda n: not n.tag, neighbors))
        
        next_node = next(filter(lambda n: not n.tag, neighbors), None)
        if next_node is None:
            if contains(neighbors, start): # has looped
                break
            raise ValueError('Could not move away from node ', n)
        n = next_node
        
    return loop
        
def find_edge_nodes(field:Field) -> list[Node]:    
    edge = []
    ((min_x, min_y), (max_x,max_y)) = field.get_bounds()
    

    for x in range(min_x, max_x):
        edge.append(field.get(x, min_y))
    for y in range(min_y, max_y):
        edge.append(field.get(max_x, y))
    for x in range(max_x, min_x, -1):
        edge.append(field.get(x, max_y))
    for y in range(max_y, min_y, -1):
        edge.append(field.get(min_x, y))
    return edge      



def mark_outside(field:Field, loop:list[Node]) -> Field:
    field = clear_non_loop(field, loop)
   
    edge = find_edge_nodes(field)
    
    nodes = deque(edge)
    while len(nodes) > 0:
        n = nodes.pop()
        if n.value == PIPE_NO_PIPE:
            n.value = PIPE_OUTSIDE
    
    no_pipes = deque(filter(lambda n: n.value == PIPE_NO_PIPE, field.all_nodes))
    
    nodes = deque(edge)
    while len(nodes) > 0:
        n = nodes.pop()

    

    return field