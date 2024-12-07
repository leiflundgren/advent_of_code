from typing import Self

import directions

from directions import Direction

N = directions.N
E = directions.E
S = directions.S
W = directions.W

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
            
    def __strr__(self) -> str:
        return self.print_char
    def __repr__(self) -> str:
        return f'pipe {self.name} {self.print_char}'
    
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
        left = dir.rotate(90)
        right = dir.rotate(-90)
        return self.has_directions([left, right])

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

def parse_pipe(c:str) -> Pipe:
    for p in ALL_PIPES:
        if p.parse_char == c:
            return p
    raise ValueError('Unknown pipe', c)

# None used to make Start connect to anything
# def can_connect_horizontal(left:Pipe, right:Pipe) -> bool:
#     return (left.has_E is None or left.has_E) and (right.has_W is None or right.has_W)
# def can_connect_vertical(top:Pipe, bottom:Pipe) -> bool:
#     return (top.has_S is None or top.has_S) and (bottom.has_N is None or bottom.has_N)

def can_connect(p1:Pipe, p2:Pipe, dir:Direction) -> bool :
    return p1.has_directions(dir) and p2.has_directions(dir.opposite())
    
def parse_pipe(c:str) -> Pipe:
    for p in ALL_PIPES:
        if p.parse_char == c:
            return p
    raise ValueError('Unknown pipe', c)

def from_directions(dirs : list[Direction]) -> Pipe:
    for p in ALL_PIPES:
        if p.has_pipe and p.has_directions(dirs):
            return p
    return None 