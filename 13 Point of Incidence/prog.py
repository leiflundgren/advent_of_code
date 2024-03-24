import tools
from enum import Enum
from typing import Iterable, Iterator, Self, Sequence, Tuple

class Matrix:
    def __init__(self, src : list[str]):
        self.data = src
        

    def __str__(self) -> str:
        return '\n'.join(self.data)
    
    def rotate(self) -> Self:
        y = list(map(lambda i: ''.join([ self.data[j][i] for j in range(len(self.data)) ]), range(len(self.data[0]))))
        return Matrix(y)
                


