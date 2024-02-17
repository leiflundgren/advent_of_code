from email.charset import add_alias
import tools
from enum import Enum
import stat
from typing import Iterator, Self
import re
from itertools import tee
import functools
from copy import deepcopy

def all_zero(ls:list[int]) -> bool:
    for n in ls:
        if n != 0:
            return False
    return True

def int_derivate(input:list[int]) -> list[int] :
    if len(input) < 2:
        return []
    res = input[0:-1] # allocate range
    for i in range(0, len(input)-1):
        res[i] = input[i+1]-input[i]
    return res

def create_derivates(ls:list[int]) -> list[list[int]] :
    all_derivates = [ls]
    while not all_zero(all_derivates[-1]):
        dx = int_derivate(all_derivates[-1])
        all_derivates.append(dx)
    return all_derivates
    
def calc_next(all_derivates : list[list[int]] ) -> list[list[int]] :
    all_derivates = deepcopy(all_derivates)
    all_derivates[-1].append(0) # first step
    all_derivates[-1].insert(0, 0) # first step
    for i in range(len(all_derivates)-2, -1, -1):
        dx_ls = all_derivates[i+1]
        ls = all_derivates[i]
        next_el = ls[-1] + dx_ls[-1]
        ls.append(next_el)
        
        prev_el = ls[0] - dx_ls[0]
        ls.insert(0, prev_el)
    return all_derivates



class Predictor:
    def __init__(self, input:list[int]):
        self.input = input
        self.all_derivates = create_derivates(self.input)
        self.next_ls = calc_next(self.all_derivates)
        self.next_el = self.next_ls[0][-1]
        self.prev_el = self.next_ls[0][0]
        
    
    
