from re import X
import tools
from enum import Enum
from typing import Iterable, Iterator, List, Self, Sequence, Tuple

def parse_line(line: str) -> List[int]:
    return list(map(int, line.split(' ')))

def is_safe(levels : List[int], max_unsafe : int ) -> bool:
    return is_safe_dir(levels, -1, max_unsafe) or is_safe_dir(levels, 1, max_unsafe)

def is_safe_dir(levels : List[int], dir : int, max_unsafe : int) -> bool:
    
    # i=0
    # while True:
    #     n0 = levels[i]
    #     for i1 in range(1, 1+max_unsafe):
    #         n = levels[i+i1]
    #         diff = dir * (n0 - n)
    #         if not ( 0 < diff and diff <= 3 ):
    #             if max_unsafe == 0:
    #                 return False
    #             max_unsafe -= 1
    #         else:
    #             prev = n


    #         pass

    def check_safe(n1, n2):
        diff = dir * (n1-n2)
        return ( 0 < diff and diff <= 3 )


    prev = levels[0]
    pos = 1
    if not check_safe(levels[0], levels[1]):
        if max_unsafe == 0:
            return False
        max_unsafe -= 1
        prev = levels[1]
        pos = 2


    for n in levels[pos:] :
        if not check_safe(prev, n):
            if max_unsafe == 0:
                return False
            max_unsafe -= 1
        else:
            prev = n

    return True
