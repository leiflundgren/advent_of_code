import tools
from enum import Enum
from typing import Iterable, Iterator, Self
import re
from itertools import tee
import functools
from copy import deepcopy
from tools import ListIter


class Springs:
    
    EMPTY = '.'
    SPRING = '#'
    UNKNOWN = '?'
    
    instanceSeed = 0

    def __init__(self, springs:ListIter[tuple[str, int]], arrangment:ListIter[int]):
        assert isinstance(springs, ListIter)
        assert isinstance(arrangment, ListIter)
        self.springs = springs
        self.arrangment = arrangment
        self.id = ++Springs.instanceSeed

    def __str__(self):
        return Springs.makestring(self.springs, self.arrangment)

    def __repr__(self):
        return 'Springs: ' + str(self)
    
    def is_empty(self):
        return 0 == len(self.springs)
    def not_empty(self):
        return 0 != len(self.springs)
    
    def get_reversed(self):
        return Springs(self.springs.get_reversed(), self.arrangment.get_reversed())

    @staticmethod
    def makestring(springs:ListIter[tuple[str, int]], arrangment:ListIter[int]) -> str:
        return f'{springs}     {arrangment}'
        
    def reduce(self):
        
        EMPTY = Springs.EMPTY
        SPRING = Springs.SPRING 
        UNKNOWN = Springs.UNKNOWN 

        reduced = True
        while reduced:
            reduced = any([
                self.reduce_front(),
                self.get_reversed().reduce_front(),
                self.reduce_max(),
            ])
            
    def reduce_front(self) -> bool:
        EMPTY = Springs.EMPTY
        SPRING = Springs.SPRING 
        UNKNOWN = Springs.UNKNOWN 

        if self.springs.is_empty() :
            return False

        (spring, cnt) = self.springs.front()
        arr = self.arrangment.front() if self.arrangment.not_empty() else 0

        (reduced_fwd, pop_springs, pop_arragement) = Springs.can_reduce(spring, cnt, arr)
        if reduced_fwd:
            if pop_springs: self.springs.pop()
            if pop_arragement: self.arrangment.pop()
            print(self)
            return True
            
        return False

    def reduce_max(self) -> bool:
        if self.is_empty() : return False
        
        max_a = max(self.arrangment)
        max_s = max(self.springs, key=lambda s: s[1] if s[0] == Springs.SPRING or s[0] == Springs.UNKNOWN else 0)
        
        if max_a == max_s[1]:
            self.springs.remove(max_s)
            self.arrangment.remove(max_a)
            print(self)
            return True            
        else:
            return False

    # returns (can_reduce, consume_spring, consume_arr)
    @staticmethod
    def can_reduce(spring:str, cnt:int, arr:int) -> (bool, bool, bool):
        
        EMPTY = Springs.EMPTY
        SPRING = Springs.SPRING 
        UNKNOWN = Springs.UNKNOWN 
     
        if spring == EMPTY:
            # use we have not called next of arrangment yet
            return (True, True, False)

        if spring == SPRING:
            return (True, True, True)
        
        # if spring == UNKNOWN and cnt == arr: 
        #     return (True, True, True)
        
        return (False, False, False)

                            
    
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
        
    def parse_arrangment(s:str) -> list[int]:
        return list(map(lambda s: int(s), s.split(',')))
        
    print('Parse: ', str)
    space = str.index(' ')
    springs = parse_springs(str[:space])
    arrangment = parse_arrangment(str[space+1:])
    return Springs(ListIter(springs), ListIter(arrangment))

