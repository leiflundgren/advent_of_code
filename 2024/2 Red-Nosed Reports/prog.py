from re import X
import tools
from enum import Enum
from typing import Iterable, Iterator, List, Self, Sequence, Tuple

def parse_line(line: str) -> List[int]:
    return list(map(int, line.split(' ')))

def is_safe(levels : List[int]) -> bool:
    return is_safe_dir(levels, -1) or is_safe_dir(levels, 1)

def is_safe_dir(levels : List[int], dir : int) -> bool:
    prev = levels[0]
    for n in levels[1:] :
        diff = dir * (prev - n)
        if not ( 0 < diff and diff <= 3 ):
            return False
        prev = n

    return True
