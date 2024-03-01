import tools
from enum import Enum
from typing import Iterable, Iterator, Self
import re
from itertools import tee
import functools
from copy import deepcopy


class Springs:
    
    EMPTY = '.'
    SPRING = '#'
    UNKNOWN = '?'
    
    instanceSeed = 0

    def __init__(self, springs:list[tuple[str, int]], arrangment:list[int]):
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

    @staticmethod
    def makestring(springs:list[tuple[str, int]], arrangment:list[int]) -> str:
        return f'{springs}     {arrangment}'
        
    def reduce(self):
        
        EMPTY = Springs.EMPTY
        SPRING = Springs.SPRING 
        UNKNOWN = Springs.UNKNOWN 

        reduced = True
        while reduced:
            reduced = any([
                self.reduce_ends(),
                self.reduce_max(),
            ])
            
                
    
    def reduce_ends(self) -> bool:
        EMPTY = Springs.EMPTY
        SPRING = Springs.SPRING 
        UNKNOWN = Springs.UNKNOWN 

        print(self)
        
        reduced_fwd = reduced_back = True
        any_change = False
        
        while self.not_empty() and ( reduced_fwd or reduced_back ):

            (spring, cnt) = self.springs[0]
            arr = self.arrangment[0]

            (reduced_fwd, pop_springs, pop_arragement) = Springs.can_reduce(spring, cnt, arr)
            if reduced_fwd:
                if pop_springs: self.springs.pop(0)
                if pop_arragement: self.arrangment.pop(0)
                print(self)
               
            if self.not_empty():
                (spring, cnt) = self.springs[-1]
                arr = self.arrangment[-1]
                (reduced_back, pop_springs, pop_arragement) = Springs.can_reduce(spring, cnt, arr)
                if reduced_back:
                    if pop_springs: self.springs.pop(-1)
                    if pop_arragement: self.arrangment.pop(-1)
                    print(self)
            any_change = any_change or reduced_back or reduced_fwd

        return any_change

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
    return Springs(springs, arrangment)

