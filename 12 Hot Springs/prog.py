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

    def __init__(self, springs:list[tuple[str, int]], arrangment:list[int]):
        self.springs = springs
        self.arrangment = arrangment

    def __str__(self):
        return Springs.makestring(self.springs, self.arrangment)
    
    @staticmethod
    def makestring(springs:list[tuple[str, int]], arrangment:list[int]) -> str:
        return f'{springs}     {arrangment}'
        
    def reduce(self):
        springs = self.springs
        arrangment = self.arrangment
        print(self)
        
        reduced_fwd = reduced_back = True
        
        while reduced_fwd or reduced_back:

            (reduced_fwd, pop_springs, pop_arragement) = Springs.can_reduce(springs[0][0], springs[0][1], arrangment[0])
            if reduced_fwd:
                if pop_springs: springs.pop(0)
                if pop_arragement: arrangment.pop(0)
                print(Springs.makestring(springs, arrangment))
               
            if len(springs) > 0 and len(arrangment) > 0:
                (reduced_back, pop_springs, pop_arragement) = Springs.can_reduce(springs[-1][0], springs[-1][1], arrangment[-1])
                if reduced_back:
                    if pop_springs: springs.pop(-1)
                    if pop_arragement: arrangment.pop(-1)
                    print(Springs.makestring(springs, arrangment))

        return Springs(springs, arrangment)
    

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

