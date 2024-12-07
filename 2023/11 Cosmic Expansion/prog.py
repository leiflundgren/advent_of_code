import tools
from enum import Enum
from typing import Iterator, Self
import re
from itertools import tee
import functools
from copy import deepcopy


class Springs:
    
    EMPTY = '.'
    SPRING = '#'
    UNKNOWN = '?'

    def __init__(self, str:str):
        def parse_springs(s:str) -> list[tuple[str, int]]:
            ls : list[tuple[str, int]] = []
            for c in s:
                if len(ls)>0 and ls[-1][0] == c:
                    ls[-1][1] = 1+ls[-1][1]
                else:
                     ls.append((c, 1))
            pass
        def parse_arrangement(s:str) -> list[int]:
            return list(map(lambda s: int(s), s.split(',')))
        space = str.index(' ')
        self.springs = str[:space]
        self.arrangement = parse_arrangement(str[space+1:])

    def reduce(self):
        changed = True
        while changed:
            print(f'{self.springs}')
            changed = self.reduce_dir(1) or self.reduce_dir(-1)
        
    def reduce_dir(self, dir:int):
        EMPTY = Springs.EMPTY
        SPRING = Springs.SPRING 
        UNKNOWN = Springs.UNKNOWN 

        changed = True
        while True:
            c = self.springs[dir]
            if c == EMPTY:
                del self.springs[dir]
                print(f'{self.springs}')
                continue
        
            if c == SPRING:
                del self.springs[dir]                
                print(f'{self.springs}')
                continue


            changed = False