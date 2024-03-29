import tools
from enum import Enum
from typing import Iterable, Iterator, Self, Sequence, Tuple


class Matrix:
    def __init__(self, name:str, src : list[str], mode:int = 1):
        assert isinstance(name, str)
        self.name = name
        self.data = list(map(lambda s: list(s), src))
        self.mode = mode
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
        y = list(map(lambda i: ''.join([ self.data[j][i] for j in range(self.get_height()) ]), range(len(self.data[0]))))
        return Matrix(self.name, y, self.mode)

    def find_mirror_lines(self) -> list[int]:
        equal_lines = self.find_equal_lines()
        return list(filter(lambda line: self.check_if_mirror(line), equal_lines))
                
    def find_equal_lines(self) -> list[int]:
        res = []
        for i in range(1, self.get_height()):
            l1 = self.getLine(i)
            l2 = self.getLine(i+1)
            if self.lines_equals(l1, l2):
                res.append(i)
        return res
    
    def check_if_mirror(self, line:int) -> bool:
        (p1, p2) = (line, line+1)
        while p1 > 0 and p2 <= self.get_height():
            l1 = self.getLine(p1)
            l2 = self.getLine(p2)
            if not self.lines_equals(l1, l2):
                return False
            
            p1 = p1-1
            p2 = p2+1
        return True
    
    def find_mirrors(self, expected_diffs: int) -> list[int]:
        
        lines = range(1, (self.get_height()))

        return list(filter(lambda n: expected_diffs == self.count_mirror_faults(n), lines))
            
    def sum_lines(self, expected_diffs: int, check_columns:bool = True) -> int:
        rows = self.find_mirrors(expected_diffs)
        columns = self.rotate().find_mirrors(expected_diffs) if check_columns else [0]
        
        return sum(columns) + 100*sum(rows)
    
    def count_mirror_faults(self, line:int) -> bool:
        def count_line_diffs(l1, l2):
            sum_ = 0
            for (x,y) in zip(l1, l2):
                if x != y:
                    sum_ += 1
            return sum_

        (p1, p2) = (line, line+1)
        if p1 <= 0 or p2 > self.get_height():
            return 100000
        
        sum_ = 0
        while p1 > 0 and p2 <= self.get_height():
            l1 = self.getLine(p1)
            l2 = self.getLine(p2)
            diffs = count_line_diffs(l1, l2)
            
            sum_ += diffs
            p1 = p1-1
            p2 = p2+1
        return sum_