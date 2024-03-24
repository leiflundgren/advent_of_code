import tools
from enum import Enum
from typing import Iterable, Iterator, Self, Sequence, Tuple


class Matrix:
    def __init__(self, src : list[str], lines_equals = None):
        self.data = src
        self.lines_equals = (Matrix.lines_exactly_equal if lines_equals is None else lines_equals)
        
    # get 1-indexed
    def getLine(self, i : int) -> str:
        return self.data[i-1]

    def __len__(self) -> int:
        return len(self.data)
    def __str__(self) -> str:
        return '\n'.join(self.data)
    
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
        y = list(map(lambda i: ''.join([ self.data[j][i] for j in range(len(self)) ]), range(len(self.data[0]))))
        return Matrix(y)
                
    def find_equal_lines(self) -> list[int]:
        res = []
        for i in range(1, len(self)):
            if self.lines_equals(self.getLine(i), self.getLine(i+1)):
                res.append(i)
        return res
    
    def check_if_mirror(self, line:int) -> bool:
        (p1, p2) = (line, line+1)
        while p1 > 0 and p2 <= len(self):
            l1 = self.getLine(p1)
            l2 = self.getLine(p2)
            if not self.lines_equals(l1, l2):
                return False
            
            p1 = p1-1
            p2 = p2+1
        return True
    
    def find_mirrors(self) -> list[int]:
        return list(filter(lambda n: self.check_if_mirror(n), self.find_equal_lines()))
            
    def sum_lines(self) -> int:
        rows = self.find_mirrors()
        columns = self.rotate().find_mirrors()
        
        return sum(columns) + 100*sum(rows)