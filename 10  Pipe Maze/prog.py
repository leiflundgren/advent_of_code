import typing
import tools
from enum import Enum, StrEnum
from typing import Iterator, Self
import re
from itertools import tee
import functools
from copy import deepcopy

class Pipes(StrEnum):
    VERTICAL = '|' # is a vertical pipe connecting north and south.
    HORIZONTAL = '-' # is a horizontal pipe connecting east and west.
    BEND_N_E = 'L' # is a 90-degree bend connecting north and east.
    BEND_N_W = 'J' # is a 90-degree bend connecting north and west.
    BEND_S_W = '7' # is a 90-degree bend connecting south and west.
    BEND_S_E = 'F' # is a 90-degree bend connecting south and east.
    NO_PIPE = '.' # is ground; there is no pipe in this tile.
    START = 'S' # is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
    
    def __repr__(self) -> str:
    
    switcher = {
    VERTICAL = '|' # is a vertical pipe connecting north and south.
    HORIZONTAL = '-' # is a horizontal pipe connecting east and west.
    BEND_N_E = 'L' # is a 90-degree bend connecting north and east.
    BEND_N_W = 'J' # is a 90-degree bend connecting north and west.
    BEND_S_W = '7' # is a 90-degree bend connecting south and west.
    BEND_S_E = 'F' # is a 90-degree bend connecting south and east.
    NO_PIPE = '.' # is ground; there is no pipe in this tile.
    START = 'S' # is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
    
        }

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
            return ''.join(map(lambda n: n.value.value, ls))
        lines = list(map(y_to_str, self.field))
        return '\n'.join(lines)

class Node:
    def __init__(self, field:Field, value:Pipes, x:int, y:int):
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
            p = Pipes(lines[y][x])
            n = Node(field, p, x, y)
            field.set(x, y, n)
    return field
