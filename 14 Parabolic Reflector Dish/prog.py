from contextlib import redirect_stdout
from itertools import count
import itertools
from re import S
import tools
import copy
from enum import Enum
from typing import Iterable, Iterator, Self, Sequence, Tuple
from directions import Direction

def create_matrix(rows:int, cols:int, v):
    return [([v]*cols) for i in range(rows)]

class Matrix:
    def __init__(self, name:str, src : list[str], dir:Direction = Direction.N):
        assert isinstance(name, str)
        self.name = name
        self.data = list(map(lambda s: list(s), src))
        self.dir = dir
        self.lines_equals = Matrix.lines_exactly_equal

    def clone(self) -> Self:
        data = copy.deepcopy(self.data)
        return Matrix(self.name, data, self.dir)

    # get 1-indexed
    def getLine(self, i : int) -> list[str]:
        return self.data[i-1]

    def get(self, x, y):
        return self.data[y-1][x-1]

    def set(self, x, y, v):
        self.data[y-1][x-1] = v

    def get_width(self):
        return len(self.data[0])
    def get_height(self):
        return len(self.data)
        
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

    @staticmethod
    def tilt(m:Self, dir:Direction, debug_print:bool = True) -> Self:
        m = m.clone() 
        org_dir = m.dir
        
        rots_done = 0
        while m.dir != dir:
            m = m.rotate()
            rots_done += 1
        if rots_done and debug_print:
            print(f'rotated {m.name} dir={m.dir}\n{m}\n')
            

        for (x,y) in m.get_points():
            
            if y == 1: continue # first line, already tilted

            if m.get(x,y) == 'O':
                empty = y
                for i in range(y-1, 0, -1):
                    if m.get(x, i) == '.':
                        empty = i
                    else:
                        break
                if empty < y: # move it
                    m.set(x, y, '.')
                    m.set(x, empty, 'O')
        
        if rots_done > 0:
            if debug_print:
                print(f'before re-rotated {m.name} dir={m.dir}\n{m}\n')
            while m.dir != org_dir:
                m = m.rotate()
                
            # rots_needed = 4-rots_done
            # while rots_needed > 0:
            #     m = m.rotate()
            #     rots_needed -= 1
            if debug_print:
                print(f'rotated {m.name} dir={m.dir}\n{m}\n')

        return m

    @staticmethod
    def calc_force(m, d:Direction, debug_print:bool = True) -> int:
        while d != Direction.S:
            m = m.rotate()
            d = d.rotate(90)
            if debug_print:
                print(f'calc {m.name} dir {m.dir}\n{m}\n')
            
        F = 0
        for row in m.line_range():
            #F += line * itertools.count(filter(lambda chr: chr=='O', m.getLine(line)))
            line = m.getLine(row)
            for chr in line:
                if chr == 'O':
                    F += row
                            
        return F
    

    @staticmethod
    def spin_cycle(m:Self, debug_print:bool = True) -> Self:
        for dir in [Direction.N,Direction.W,Direction.S,Direction.E]:
            m = Matrix.tilt(m, dir, debug_print)
        return m


    @staticmethod
    def spin_many_times_force_north(m:Self, spin_count:int, debug_print:bool = True) -> int:
        def print_debug(s:str):
            if debug_print:
                print(s)
                
        i = 0
        cached = {}
        m2 = m
        force_2 = -1
        m_last = None
        max_spins = spin_count
        extra_spins = -1
        for i in range(max_spins):
        
            k1 = m2.hashstr()
            cnt = cached.get(k1)
            # force_2 = Matrix.calc_force(m2, Direction.N, False)
            if cnt is None:
                print_debug(f'force_2:{force_2} after {i} spin cycles ')    ## sum1:19608  sum2:26180
                cached[k1] = i
            elif extra_spins < 0:
                cycle = i-cnt
                print(f'after {i} spin cycles (cycle detected, at {cnt} len={cycle})')    ## sum1:19608  sum2:26180                
                max_spins -= cnt
                extra_spins = max_spins % cycle   -1              
            elif extra_spins > 0:
                print_debug(f'force_2:{force_2} after {i} spin cycles (need {extra_spins} more)')    ## sum1:19608  sum2:26180                
                extra_spins -= 1
            else: # extra_spins == 0:
                force_2 = Matrix.calc_force(m_last, Direction.N, False)
                print(f'force_2:{force_2} after {i} spin cycles (cnt={cnt}, diff={i-cnt})')    ## sum1:19608  sum2:26180                
                return force_2


            m3 = Matrix.spin_cycle(m2, False)
        
            if m3 == m2:
                break
            m2 = m3
            m_last = m2
        
            print_debug(f'\nstep {i}\n{m2}')        