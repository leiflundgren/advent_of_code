from collections import deque
from contextlib import redirect_stdout
from itertools import count
import itertools
from operator import contains
import queue
from re import S
import tools
import copy
from enum import Enum
from typing import Iterable, Iterator, Self, Sequence, Tuple
from directions import Direction

def create_matrix(rows:int, cols:int, v):
    return [([v]*cols) for i in range(rows)]

color_Red = '91m'
color_Green = '92m'
color_Yellow = '93m'
color_LightPurple = '94m'
color_Purple = '95m'
color_Cyan = '96m'
color_LightGray = '97m'
color_Black = '98m'
color_white = '00m'


def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

def format_with_color(s:str, color:str) -> str:
    if color == '00m':
        return s
    else:
        return f"\033[{color}{s}\033[00m"
    

class Element:
    def __init__(self, c:str, color:str = color_white):
        self.c = c
        self.color = color

    def __str__(self): return self.c
    
    def __repr__(self):
    #     return format_with_color(self.c, self.color)
        return self.c    
        
    def __eq__(self, __value: object) -> bool:
        return self.c == (__value if isinstance(__value, str) else __value.c)
    
    def asColorCoded(self) -> str:
        return format_with_color(self.c, self.color)

class Matrix:
    def __init__(self, name:str, src : list[str], dir:Direction = Direction.N):
        assert isinstance(name, str)
        self.name = name
        self.data : list[list[Element]] = [ [Element(c) for c in s] for s in src]
        self.dir = dir
        self.lines_equals = Matrix.lines_exactly_equal
        for (x,y) in self.get_points():
            self.get(x,y).pos = (x,y)

    def clone(self) -> Self:
        data = copy.deepcopy(self.data)
        return Matrix(self.name, data, self.dir)

    # get 1-indexed
    def getLine(self, i : int) -> list[Element]:
        return self.data[i-1]

    def get(self, t1, t2 = None) -> Element:
        (x,y) = t1 if isinstance(t1, tuple) else (t1, t2)
        return self.data[y-1][x-1]

    def set(self, x, y, v, color:str = None):
        el = self.data[y-1][x-1]
        el.c = v
        if not color is None:
            el.color = color

    def get_width(self):
        return len(self.data[0])
    def get_height(self):
        return len(self.data)
        
    def as_plain_text(self) -> str:
        return '\n'.join(map(lambda row: ''.join(map(lambda el: el.c, row)), self.data))
    def as_color_text(self) -> str:
        return '\n'.join(map(lambda row: ''.join(map(lambda el: el.asColorCoded(), row)), self.data))

    def __str__(self) -> str:
        return '\n'.join(map(lambda row: ''.join(row), self.data))
    
    def __repr__(self) -> str:
        return f'{self.name} dir:{self.dir}   \n' + str(self)

    def hashstr(self) -> str:
        #hashstr = [''.join(s) for s in [''.join(line) for line in self.data]]
        # hashstr2 = ''.join([''.join(line) for line in self.data])
        hashstr = "".join(["".join(map(str, row)) for row in self.data])
        return hashstr
    
    def __hash__(self) -> int:
        return hash(self.hashstr())

    def __eq__(self, v: object) -> bool:
        b = self.name == v.name \
            and self.dir == v.dir \
            and self.get_height() == v.get_height() \
            and self.get_width() == v.get_width()
        if not b: return False
        
        for (x,y) in self.get_points():
            if self.get(x,y) != v.get(x,y):
                return False
        return True
    
    def line_range(self) -> Iterable[int]:
        return range(1, self.get_height()+1)
    
    def get_points(self) -> Iterable[tuple[int,int]]:
        for y in range(1, 1+self.get_height()):
            for x in range(1, 1+self.get_width()):
                yield (x,y)

    @staticmethod
    def lines_exactly_equal(x:str, y:str) -> bool:
        return x == y
    @staticmethod
    def lines_1_difference(x:str, y:str) -> bool:
        
        diffs = 0
        for (cx, cy) in zip(x, y):
            if cx != cy:
                ++diffs
        return diffs == 1

    def rotate(self) -> Self:
        # def rotated_array(array):
        #     new_array = create_matrix(self.get_width(), self.get_height(), '?')
        #     for i in range(array.shape[0]):
        #         for j in range(array.shape[1]):
        #             t = array.shape[0]-j-1          # To Start with last row and first column
        #             new_array[i, j] = array[t, i]
        #     return new_array
        
        def rotate_matrix(src: list[list[str]]) -> list[list[str]]: 
            w = len(src[0])
            h = len(src)
            
            new_matrix = [['?' for j in range(w)] for i in range(h)]
            for i in range(w):
                for j in range(h):
                    new_matrix[j][h-1-i] = src[i][j]
            return new_matrix


        m = Matrix(self.name, rotate_matrix(self.data), self.dir.rotate(-90))
        # m_h = m.get_height()
        # m_w = m.get_width()

        # for x in range(1, 1+self.get_width()):
        #     for y in range(1, 1+self.get_height()):
        #         t = self.get_width()-y-1
        #         v = self.get(t, x)
        #         m.set(x, y, v)
                
        return m
        # y = list(map(lambda i: ''.join([ self.data[j][i] for j in range(self.get_height()) ]), range(len(self.data[0]))))
        # return Matrix(self.name, y, self.dir)

    def find_next(self, pos:tuple[int,int], dir0:Direction) -> list[tuple[int, int]]:
         
        (px, py) = pos
        el = self.get(pos)
        dirs = dir0.move_light_beam(el.c)
        offsets = [d.offset_dir() for d in dirs ]
        
        offset_pos = [ (px+ox,py+oy) for (ox,oy) in offsets]        
        
        res = []
        for ((x, y), dir) in zip(offset_pos, dirs):
            if x>=1 and y >= 1 and x <= self.get_width() and y <= self.get_height():
                res.append(((x,y), dir))
        
        return res
    
    def trace_path(self, pos:tuple[int,int], dir:Direction) -> list[tuple[tuple[int, int], Direction]]:
        res = []
        work = deque()
        work.append((pos, dir))
        
        while len(work) > 0:
            (pos, dir) = work.pop()
            
            if contains(res, (pos, dir)):
                continue
            
            res.append((pos, dir))
            
            next_ls = self.find_next(pos, dir)
            work += next_ls
            
        return res

    def color_mark(self, points:list[tuple[int,int]], color:str):
        for (x,y) in points:
            self.get(x,y).color = color

    def count_empty_tiles(self, points:list[tuple[int,int]]):
        sum_ =0
        
        for ((x,y),d) in points:
            el = self.get(x,y).c
            if el == '.':
                sum_ += 1
            elif el == Direction.char_vertial and d.is_vertical():
                sum_ += 1
            elif el == Direction.char_horizontal and d.is_horizontal():
                sum_ += 1
            else:
                pass
                
        return sum_

    # loosing information about direction (uniq points)
    @staticmethod 
    def path_to_points(input : list[tuple[tuple[int, int], Direction]]) -> list[tuple[int, int]]:
        res = set()
        
        for (pos, dir) in input:
            res.add(pos)
            
        return list(res)


