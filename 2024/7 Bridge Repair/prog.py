import copy
from itertools import combinations
from directions import Direction
from map import Map, Node, Point, Vector
from text_map import TextMap
import tools
from enum import Enum
from typing import Dict, Generator, Iterable, Iterator, List, Self, Sequence, Tuple

class Measure(object):
    def __init__(self, result:int, args:List[int]):
        self.result = result
        self.args = args


def parse(txt: str) -> List[Measure]:
    lines = txt.strip('\r\n').splitlines()
    res = []
    for line in lines:
        # 190: 10 19
        numbers = line.split(' ')
        sum = int(numbers[0].rstrip(':'))
        args = [ int(x) for x in numbers[1:] ]
        res.append(Measure(sum, args))
    return res

class Operator(object):
    def __init__(self, symbol:str):
        self.symbol = symbol

    def __repr__(self) -> str:
        return f'op:{self.symbol}'

    def operate(self, x:int, y:int) -> int:
        raise NotImplementedError("Base class, operator is not overridden")


class AddOperator(Operator):
    def __init__(self):
        super().__init__('+')

    def operate(self, x:int, y:int) -> int:
        return x + y

class MultiplicateOperator(Operator):
    def __init__(self):
        super().__init__('*')

    def operate(self, x:int, y:int) -> int:
        return x * y

all_operators = [ AddOperator(), MultiplicateOperator() ]

def generate_combinations(symbols:List, length:int) -> List:
    base_ls = [None] * length
    cnt = len(symbols) ** length
    #res = [base_ls] * cnt
    res = [base_ls] 

    for i in range(length):
        #res = list(res) + list(res)
        base = res
        res = []
        for s in symbols:
            ls = copy.deepcopy(base)
            for r in ls:
                r[i] = s
            res += ls

    return res

def calculate_result(args:List[int], operators:List[Operator]) -> int:
    if len(args) != 1+ len(operators): 
        raise ValueError(f'Need len(args) == 1+len(opers), got {len(args)} and {len(operators)}')

    res : int = args[0]
    for (op, arg) in zip(operators, args[1:]):
        v = op.operate(res, arg)
        res = v
    return res

class Worker(object):
    def __init__(self):
        self.combinations : Dict[int, List[Operator]] = {}

    def get_combinations(self, length:int) -> List[Operator]:
        op = self.combinations.get(length)
        if op is None:
            op = generate_combinations(all_operators, length)
            self.combinations[length] = op
        return op

    def find_matching(self, m : Measure) -> List[Operator]:
        combinations = self.get_combinations(len(m.args)-1)

        for opers in combinations:
            res = calculate_result(m.args, opers)
            if res == m.result:
                return opers

        return None

    def sum_result_of_matching(self, ms : List[Measure]) -> int:
        res = 0
        for m in ms:            
            correct = self.find_matching(m)
            if correct is not None:
                res += m.result

        return res