import tools
from enum import Enum
from typing import Iterable, Iterator, Self, Sequence, Tuple

def split_input(s:str)->list[str]:
    return s.split(',')

def calc_hash(s:str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h = (h%256)
    return h
