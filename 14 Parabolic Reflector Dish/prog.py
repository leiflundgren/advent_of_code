from itertools import count
import itertools
import tools
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
    
    def line_range(self) -> Iterable[int]:
        return range(1, self.get_height()+1)

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


        m = Matrix(self.name, rotate_matrix(self.data), self.dir.rotate(90))
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
    def calc_force(m, d:Direction) -> int:
        while d != Direction.S:
            m = m.rotate()
            d = d.rotate(90)
            print(f'calc {m.name} dir {m.dir}\n{m}\n')
            
        F = 0
        for row in m.line_range():
            #F += line * itertools.count(filter(lambda chr: chr=='O', m.getLine(line)))
            line = m.getLine(row)
            for chr in line:
                if chr == 'O':
                    F += row
                            
        return F
