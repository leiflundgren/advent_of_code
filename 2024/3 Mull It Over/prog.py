import re
import tools
from enum import Enum
from typing import Iterable, Iterator, List, Self, Sequence, Tuple

def parse_muls(s: str) -> List[str]:
    # mul(1,999)
    # xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

    hits = re.findall('(mul\(\d{1,3},\d{1,3}\))', s)
    return hits

def parse_muls_pairs(s: str) -> List[Tuple[int, int]]:
    # mul(1,999)
    # xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

    hits = re.findall('mul\((\d{1,3}),(\d{1,3})\)', s)
    return [ (int(a),int(b)) for (a,b) in hits ]


def parse_inputs(s:str) -> List[str] :
    # mul_key = 'mul\(\d{1,3},\d{1,3}\)'
    # do_key ='do\(\)'
    # dont_key = 'don\'t\(\)'

    # res = []

    # in_do = True

    # pos = 0
    # while True:
    #     mul = re.match(mul_key, s)
    #     do = re.match(do_key, s)
    #     dont = re.match(dont_key, s)


    key = '((mul\(\d{1,3},\d{1,3}\))|(do\(\))|(don\'t\(\)))'
    inputs = [ t[0] for t in re.findall(key, s) ]

    return inputs

def filter_inputs(inputs : List[str]) -> List[str] :
    in_do = True
    res = []

    for inp in inputs:
        if inp == 'do()':
            in_do = True
        elif inp == '''don't()''':
            in_do = False
        elif in_do:
            res.append(inp)

    return res

def multiply_inputs(inputs : List[Tuple[int, int]]) -> int:
    return sum( [x*y for (x,y) in inputs])