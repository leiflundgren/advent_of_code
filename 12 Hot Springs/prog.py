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

    def __init__(self, springs:list[tuple[str, int]], arrangement:list[int]):
        self.springs = springs
        self.arrangement = arrangement

    def __str__(self):
        return f'{self.springs}  {self.arrangement}'
        
    def reduce(self):
        while True:
            print(self)
            
            nxt_front = self.reduce_dir(0)
            nxt_back = (self if nxt_front is None else nxt_front).reduce_dir(-1)
            
            if not nxt_back is None:
                return nxt_back.reduce()
            elif not nxt_back is None:
                return nxt_front.reduce()
            else:
                return self
        
    def reduce_dir(self, dir:int) -> (bool, Self):
        def copy_except(ls:list, dir:int) -> list:
            return ls[1:] if dir == 0 else ls[:-1]
        

        EMPTY = Springs.EMPTY
        SPRING = Springs.SPRING 
        UNKNOWN = Springs.UNKNOWN 
        
        if len(self.springs) == 0:
            return None
                    
        rev = -1 if dir == 0 else 0
        (c, cnt) = self.springs[dir]
        if c == EMPTY:
            changed = Springs(copy_except(self.springs, dir), self.arrangement)
            print(changed)
            return changed
        
        arr = self.arrangement[dir]
        if c == SPRING:
            changed = Springs(copy_except(self.springs, dir), copy_except(self.arrangement, dir))
            print(changed)
            return changed
        
        if c == UNKNOWN and cnt == arr: 
            changed = Springs(copy_except(self.springs, dir), copy_except(self.arrangement, dir))
            print(changed)
            return changed

        return None
    
def parse_springs(str:str):
    def parse_springs(s:str) -> list[tuple[str, int]]:
        ls : list[tuple[str, int]] = []
        for c in s:
            if len(ls)==0:
                    ls.append((c, 1))
                    continue
                
            (chr, cnt) = ls[-1]
            if chr == c:
                ls[-1] = (chr, 1+cnt)
            else:
                    ls.append((c, 1))
        return ls
        
    def parse_arrangement(s:str) -> list[int]:
        return list(map(lambda s: int(s), s.split(',')))
        
    space = str.index(' ')
    springs = parse_springs(str[:space])
    arrangement = parse_arrangement(str[space+1:])
    return Springs(springs, arrangement)

