from re import X
import tools
from enum import Enum
from typing import Iterable, Iterator, List, Self, Sequence, Tuple

def parse_line(line: str) -> List[int]:
    return list(map(int, line.split(' ')))

def is_safe(levels : List[int], max_unsafe : int = 0) -> bool:
    return is_safe_dir(levels, -1, max_unsafe) or is_safe_dir(levels, 1, max_unsafe)

def is_safe_dir(levels : List[int], dir : int, max_unsafe : int) -> bool:
    prev = levels[0]
    for n in levels[1:] :
        diff = dir * (prev - n)
        if not ( 0 < diff and diff <= 3 ):
            if max_unsafe == 0:
                return False
            max_unsafe -= 1
        else:
            prev = n

    return True
