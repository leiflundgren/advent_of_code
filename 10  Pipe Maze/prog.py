import typing
from xmlrpc.client import TRANSPORT_ERROR
import tools
from enum import Enum, StrEnum
from typing import Iterator, Self
import re
from itertools import tee
import functools
from copy import deepcopy

class Pipe:
    def __init__(self, parse_char:str, print_char:str, name:str, has_W:bool, has_E:bool, has_N:bool, has_S:bool):
        self.parse_char = parse_char
        self.print_char = print_char
        self.name = name
        self.has_E = has_E
        self.has_W = has_W
        self.has_N = has_N
        self.has_S = has_S
            
    def __repr__(self) -> str:
        return self.print_char    

PIPE_VERTICAL = Pipe('|', '┃', 'N-S', False, False, True, True) # is a vertical pipe connecting north and south.
PIPE_HORIZONTAL = Pipe('-', '━', 'W-E', True, True, False, False) # is a horizontal pipe connecting east and west.
PIPE_BEND_N_E = Pipe('L', '┖', 'N-E', False, True, True, False) # is a 90-degree bend connecting north and east.
PIPE_BEND_N_W = Pipe('J', '┛', 'N-W', True, False, True, False) # is a 90-degree bend connecting north and west.
PIPE_BEND_S_W = Pipe('7', '┒', 'S-W', True, False, False, True) # is a 90-degree bend connecting south and west.
PIPE_BEND_S_E = Pipe('F', '┎', 'S-E', False, True, False, True) # is a 90-degree bend connecting south and east.
PIPE_NO_PIPE = Pipe('.', '·', 'empty', False, False, False, False) # is ground; there is no pipe in this tile.
PIPE_START = Pipe('S', 'S', 'start', None, None, None, None) # is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

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

class Field:
    def __init__(self, field_matrix : list[list[Node]] = None):
        self.field = field_matrix        
    def get(self, x:int, y:int) -> Node:
        return self.field[y][x]
    def set(self, x:int, y:int, n:Node) -> None:
        self.field[y][x] = n
        

    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        def y_to_str(ls: list[Node]) -> str:
            return ''.join(map(lambda n: n.value.print_char, ls))
        lines = list(map(y_to_str, self.field))
        return '\n'.join(lines)

class Node:
    def __init__(self, field:Field, value:Pipe, x:int, y:int):
        self.field = field
        self.value = value
        self.x = x
        self.y = y
       
    def left(self) -> Self:
        assert(self.x > 0)
        return self.field.get(self.x-1, self.y)
    
    def __str__(self) -> str:
        return f'Node [{self.x},{self.y}] {self.value}'

    def __repr__(self) -> str:
        return f'Node [{self.x},{self.y}] {self.value}'

def ParseField(str_field:str) -> Field:
    lines = str_field.split('\n')
    y_len = len(lines)
    x_len = len(lines[0])
    field = Field()
    field.field = list(map(lambda _: [None]*x_len, [None]*y_len  ))
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            p = parse_pipe(lines[y][x])
            n = Node(field, p, x, y)
            field.set(x, y, n)
    return field
