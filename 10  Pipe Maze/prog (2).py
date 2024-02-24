from collections import deque
from collections.abc import Iterable
import itertools
from operator import contains
import typing
import tools
from enum import Enum, StrEnum
from typing import Iterator, Self
import re
from itertools import tee
import functools
from copy import deepcopy

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
    
    def has_directions(self, dir_or_iter:str) -> bool :        
        def inner(dir):
            if dir == N: return self.has_N
            if dir == S: return self.has_S
            if dir == E: return self.has_E
            if dir == W: return self.has_W
            raise ValueError(f'Innvalid direction {dir}')
        
        if isinstance(dir_or_iter, Direction):
            return inner(dir_or_iter)
        elif dir_or_iter is str:
            return inner(dir_or_iter)
        else:
            for dir in dir_or_iter:
                has = inner(dir)
                if has is False:
                    return False
            return True
    
    def blocks(self, dir:Direction) -> bool:
        if dir == N or dir == S:
            return self.has_E and self.has_W
        if dir == E or dir == W:
            return self.has_N and self.has_S
        raise ValueError(f'Innvalid direction {dir}')
        
       

    @staticmethod
    def directions_connect(p1: Self, dir: str, p2: Self) -> bool:
        return p1.has_directions(dir) and p2.has_directions(dir.opposite())

PIPE_VERTICAL = Pipe('|', '┃', 'N-S', True, False, False, True, True) # is a vertical pipe connecting north and south.
PIPE_HORIZONTAL = Pipe('-', '━', 'W-E', True, True, True, False, False) # is a horizontal pipe connecting east and west.
PIPE_BEND_N_E = Pipe('L', '┖', 'N-E', True, False, True, True, False) # is a 90-degree bend connecting north and east.
PIPE_BEND_N_W = Pipe('J', '┛', 'N-W', True, True, False, True, False) # is a 90-degree bend connecting north and west.
PIPE_BEND_S_W = Pipe('7', '┒', 'S-W', True, True, False, False, True) # is a 90-degree bend connecting south and west.
PIPE_BEND_S_E = Pipe('F', '┎', 'S-E', True, False, True, False, True) # is a 90-degree bend connecting south and east.
PIPE_NO_PIPE = Pipe('.', '·', 'empty', False, False, False, False, False) # is ground; there is no pipe in this tile.
PIPE_START = Pipe('S', 'S', 'start', True, True, True, True, True) # is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
PIPE_OUTSIDE = Pipe('O', 'O', 'outside', False, False, False, False, False) 
PIPE_INSIDE = Pipe('I', 'I', 'inside', False, False, False, False, False) 

ALL_PIPES = [ PIPE_VERTICAL,PIPE_HORIZONTAL,PIPE_BEND_N_E ,PIPE_BEND_N_W ,PIPE_BEND_S_W ,PIPE_BEND_S_E ,PIPE_NO_PIPE ,PIPE_START ]


# None used to make Start connect to anything
def can_connect_horizontal(left:Pipe, right:Pipe) -> bool:
    return (left.has_E is None or left.has_E) and (right.has_W is None or right.has_W)
def can_connect_vertical(top:Pipe, bottom:Pipe) -> bool:
    return (top.has_S is None or top.has_S) and (bottom.has_N is None or bottom.has_N)
    

class Field:
    def __init__(self, field_matrix : list[list[Node]] = None):
        self.field : dict[tuple[int, int], Node] = {}
        
        if not field_matrix is None:
            for ls in field_matrix:
                for n in ls:
                    if not n is None:
                        self.set(n.x, n.y, n)
                        
        self.set_bounds()

    def get(self, x:int, y:int, create_if_not_found=True, store_if_not_found=False) -> Node:
        if x is tuple:
            return self.get(x[0], x[1], y, create_if_not_found)

        # if outside, return a freshly minted no-pipe
        n = self.field.get((x, y), None)
        if n is None and create_if_not_found:
            n = Node(self, PIPE_NO_PIPE, x, y)
            if store_if_not_found:
                self.set(x, y, n)                
        return n

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

    def inside_bounds(self, x:int, y:int) -> bool:
        ((min_x, min_y), (max_x,max_y)) = self.get_bounds()
        return min_x <= x and x <= max_x and min_y <= y and y <= max_y

    def all_nodes_sorted(self) -> list[Node]:
        return list(sort_nodes(self.field.values()))
    def all_nodes_unsorted(self) -> list[Node]:
        return list(self.field.values())
    
    def get_all_coords(self) -> list[tuple[int, int]] :
        ((min_x, min_y), (max_x,max_y)) = self.get_bounds()
        ls = []
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                ls.append((x, y))
        return ls
                
    def fill_empty(self):
        coords = self.get_all_coords()
        for (x, y) in coords:
                self.set(x, y, self.get(x, y))
    

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
            field[n.y-min_y][n.x-min_x] = n

        lines = list(map(y_to_str, field))
        for i in range(len(lines)):
            lines[i] = f'{i} {lines[i]}'
        lines.append('')
        lines.append('  0123456789')
        return '\n'.join(lines)
    
    def get_start_pos(self) -> Node:
        return next(filter(lambda n: n.value == PIPE_START, self.field.values()), None)
    
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
            return S if n1.y < n2.y else N
        elif n1.y == n2.y:
            return E if n1.x < n2.x else W
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

    def coord(self) -> tuple[int, int] :
        return (self.x, self.y)
    
    def inside_bounds(self) -> bool:
        return self.field.inside_bounds(self.x, self.y)

    @staticmethod
    def clear_tags(thing) -> None:
        if isinstance(thing, Node):
            thing.tag = None
        else:
            for n in thing:
                Node.clear_tags(n)

    def coord_dir(self, dir:Direction) -> Self:
        if dir == N: return (self.x, self.y-1)
        if dir == NE: return (self.x+1, self.y-1)
        if dir == E: return (self.x+1, self.y)
        if dir == SE: return (self.x+1, self.y+1)
        if dir == S: return (self.x, self.y+1)
        if dir == SW: return (self.x-1, self.y+1)
        if dir == W: return (self.x-1, self.y)
        if dir == NW: return (self.x-1, self.y-1)
        raise ValueError(f'Innvalid direction {dir}')

    def move_dir(self,dir:Direction) -> Self:
        (x,y) = self.coord_dir(dir)
        return self.field.get(x, y)
    
    def move_nopipe(self,dir:Direction) -> Self:
        n = self.move_dir(dir)
        return n if n.inside_bounds() and n.value == PIPE_NO_PIPE else None


    def connect(self, dir:Direction) -> Self:
        if dir == N: return self.connect_N()
        if dir == S: return self.connect_S()
        if dir == E: return self.connect_E()
        if dir == W: return self.connect_W()
        raise ValueError(f'Innvalid direction {dir}')

    def connect_W(self) -> Self:
        if not self.field.inside_bounds(self.x-1, self.y): return None
        n = self.field.get(self.x-1, self.y)
        return n if can_connect_horizontal(n.value, self.value) else None
    def connect_E(self) -> Self:
        if not self.field.inside_bounds(self.x+1, self.y): return None
        n = self.field.get(self.x+1, self.y)
        return n if can_connect_horizontal(self.value, n.value) else None
    def connect_N(self) -> Self:
        if not self.field.inside_bounds(self.x, self.y-1): return None
        n = self.field.get(self.x, self.y-1)
        return n if can_connect_vertical(n.value, self.value) else None
    def connect_S(self) -> Self:
        if not self.field.inside_bounds(self.x, self.y+1): return None
        n = self.field.get(self.x, self.y+1)
        return n if can_connect_vertical(self.value, n.value) else None

    def connect_one(self) -> list[Self]:
        return list(filter(lambda n: not n is None, map(lambda dir: self.connect(dir), four_dir)))
    
    def find_outside(self) -> list[str]:
        def is_outside_dir(dir:Direction)->Node:
            n = self.move_dir(dir)
            return n.value == PIPE_OUTSIDE

        return list(filter(is_outside_dir, eight_dir))
    
    # strictly for sneaking between two pipes
    def sneak(self, dir:Direction) -> Self:
        dir_left = dir.left()
        dir_op = dir_left.left()
        dir_right = dir_op.left()
                
        if self.value.blocks(dir):
            return None
        
        if self.value.has_pipe and not self.value.has_directions(dir): return None
        
        n = self.move_dir(dir)
        
        if not n.inside_bounds(): return None
        if not n.value.has_pipe: return None
        if self.value.has_directions(dir):
            if not n.value.has_directions(dir_op): return None
        else:
            if not n.value.has_directions(dir): return None


        n_left = n.move_dir(dir_left)
        n_right = n.move_dir(dir_right)
        
        if self.value.has_directions(dir) and n.value.has_directions(dir_op):
            # either left or right  should have same dir
            if not n_left.value.has_directions(dir_op) and not n_right.value.has_directions(dir_op):
                return None
        
        return n
        
        # if not self.value.has_pipe:
        #     if not n.value.has_pipe: return n # without pipes, sneak free
        #     elif n.value.blocks(dir): return None
        #     if n.value.has_directions(dir): # this is an angle maybe we can sneak
        #         if n.value.has_directions(dir_left):
        #             n_right = n.move_dir(dir_right)
        #             if n_right.value.has_directions(dir): # sneak between two
        #                 return n
        #             else: return None
        #         elif n.value.has_directions(dir_right):
        #             n_left = n.move_dir(dir_left)
        #             if n_left.value.has_directions(dir): # sneak between two
        #                 return n
        #             else: return None
        #         else: return None
                
        #     else: return None
        # elif not n.value.has_pipe:
        #     return n
        
        # else:
        #     if not n.value.has_pipe \
        #         and not self.value.has_directions(dir) \
        #         and self.value.has_directions(dir.opposite()): 
        #         return n # leaving pipe, angling away
        #     elif Pipe.directions_connect(self.value, dir, n.value): 
        #         n_left = n.move_dir(dir_left)
        #         n_right= n.move_dir(dir_right)
        #         if n_left.value == PIPE_OUTSIDE or n_right.value == PIPE_OUTSIDE:
        #             return None # nope. move here different path
        #         return n            
        #     else: 
        #         return None

    def move_nopipe_one(self) -> list[Self]:
        ls = []
        for dir in four_dir:
            n = self.move_nopipe(dir)
            if not n is None:
                ls.append(n)
        return ls

    def sneak_one(self) -> list[Self]:
        outsides = list(filter(lambda n: n.values is PIPE_OUTSIDE, map(lambda d: self.move_dir(d), four_dir)))

        ls = []
        for dir in four_dir:
            n = self.sneak(dir)
            if not n is None:
                if n.x==2 and n.y == 4:
                    bp =17
                if n.x==2 and n.y == 5:
                    bp =17
                if n.x==3 and n.y == 5:
                    bp =17
                ls.append(n)
        return ls
        return list(filter(lambda n: not n is None, map(lambda dir: self.sneak(dir), four_dir)))
        
        return list(filter(lambda n: not n is None, map(lambda dir: self.sneak(dir), four_dir)))
    
    def coonnected_neighbors(self) -> list[Self]:
        valid_dir = list( filter( lambda d: not self.connect(d) is None, four_dir))
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
    Node.clear_tags(start.field.all_nodes_unsorted())
    
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
        
def find_edge_nodes(field:Field, margin:int = 0) -> list[Node]:    
    edge = []
    ((min_x, min_y), (max_x,max_y)) = field.get_bounds()
    

    for x in range(min_x-margin, max_x+margin, +1):
        edge.append(field.get(x, min_y-margin))
    for y in range(min_y-margin, max_y+margin, +1):
        edge.append(field.get(max_x+margin, y))
    for x in range(max_x+margin, min_x-margin, -1):
        edge.append(field.get(x, max_y+margin))
    for y in range(max_y+margin, min_y-margin, -1):
        edge.append(field.get(min_x-margin, y))
    return edge      



def mark_outside(field:Field, loop:list[Node]) -> Field:
    field = clear_non_loop(field, loop)
   
    edge = find_edge_nodes(field, 1)
    for n in field.all_nodes_unsorted():
        n.tag = None
    
    nodes = deque(edge)
    while len(nodes) > 0:
        n = nodes.pop()
        if n.value == PIPE_NO_PIPE:
            n.value = PIPE_OUTSIDE
            n.tag = ['outside']
            field.set(n.x, n.y, n)
    
    no_pipes = deque(filter(lambda n: n.value == PIPE_NO_PIPE, field.all_nodes_unsorted()))
    
    field.fill_empty()

    nodes = deque(edge)
    
    while len(nodes) > 0:
        n = nodes.pop()

        nexts = n.move_nopipe_one()
        for nn in nexts:            
            if nn.tag is None: nn.tag  = []
            if contains(nn.tag, 'outside'): continue # been here before
            if contains(nn.tag, 'move'): continue # been here before
            nn.tag.append('move')
            
            nn.tag.append('outside')
            if nn.value == PIPE_NO_PIPE:
                nn.value = PIPE_OUTSIDE
            nodes.append(nn)

        can_sneak_to = n.sneak_one()
        for nn in can_sneak_to:
            if 2 <= nn.x and nn.x <= 3 and nn.y == 6:
                bp = 17
                
            if nn.tag is None: nn.tag  = []
            if contains(nn.tag, 'outside'): continue # been here before
            if contains(nn.tag, 'sneak'): continue # been here before
            nn.tag.append('move')
            
            nn.tag.append('outside')

            if nn.value == PIPE_NO_PIPE:
                nn.value = PIPE_OUTSIDE
            nodes.append(nn)

    return field