import tools
from enum import Enum
import stat
from typing import Iterator, Self
import re
from itertools import tee
import functools

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
    all_derivates = []
    while not all_zero(ls):
        pass
    



class Predictor:
    def __init__(self, input:list[int], expected_next: int):
        self.input = input
        self.expected_next = expected_next
        
    
