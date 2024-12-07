from copy import copy
from struct import calcsize
from typing import Dict, TypeVar
from prog import Springs
import tools
from list_on_list import ListOnList
T = TypeVar('T')


# if arrangement take X and fields is X+1
# returns number possible arrangements, 0 if not calculated
def permut_one_free(scen:Springs) -> int:
    if scen.sum_arrangement() + 1 == scen.sum_springs():
        return 2
    return 0

class Permutor:
    def __init__(self):
        self.cache : Dict[Springs, int] = {}
        self.can_reduce : Dict[Springs, Springs] = {}

    def calc_permutations(self, scen:Springs) -> int:
        expanded_strings = []
        for (chr, cnt) in scen.springs:
            for i in range(cnt):
                expanded_strings.append( (chr, 1))
        return self.calc(Springs(ListOnList(expanded_strings), ListOnList(tools.get_inner_list(scen.arrangment))))

    def calc(self, scen : Springs, attempt_reduce = True) -> int:
        
        springs : ListOnList[tuple[str, int]] = scen.springs if isinstance(scen ,Springs) else scen
        arrangment:ListOnList[int] = scen.arrangment
        
        if len(arrangment) == 0:
            if len(springs) == 0:
                return 1 
            else:
                return 0
        if len(springs) == 0: # since len(arr)>0 we failed to place something
            return 0

        cached = self.cache.get(scen, None)
        if not cached is None:
            return cached
    
        if attempt_reduce:
            reduced = self.can_reduce.get(scen, None)
            if reduced:
                return self.calc(reduced, attempt_reduce=False)

            cpy = scen.copy(True)
            if cpy.reduce():
                self.can_reduce[scen] = cpy
                return self.calc(cpy, attempt_reduce=False)

        arr = arrangment.front()
        (chr, cnt) = springs.front()
        
        # Two cases, either Empty or Spring!
        cnt_spring = self.calc_assume_spring(springs, arrangment)
        cnt_empty = self.calc_assume_empty(springs, arrangment)
        
        self.cache[scen] = cnt_spring + cnt_empty

        return cnt_spring + cnt_empty

    def calc_assume_empty(self, springs : ListOnList[tuple[str, int]], arrangment:ListOnList[int]) -> int :
        assert Springs.UNKNOWN == springs.front()[0]

        # EMPTY

        (chr, n) = springs.front()

        try:
            old = springs
            springs = springs[1:] # pop
        except StopIteration:
            bp= 17

        return self.calc(Springs(springs, arrangment))

        # SPRING
    def calc_assume_spring(self, springs : ListOnList[tuple[str, int]], arrangment:ListOnList[int]) -> int :
        assert Springs.UNKNOWN == springs.front()[0]
        

        arr = arrangment.front()
        sum = 0
        for i in range(len(springs)): 
            chr = springs[i]
            sum = sum + 1
            if sum < arr: continue

            springs = sub_list(springs, i)
            
            if chr == Springs.SPRING and springs.not_empty() and springs.front()[0] == Springs.SPRING:
                # Had to use part of next springs-section. Illegal. 0 possibilities
                return 0
            
            return self.calc(Springs(springs, sub_list(arrangment, 1)))

        if sum < arr: 
            # Not enoughs springs
            return 0
        
        bp_what_shouldI_return = 17

def sub_list(ls : list[T], start:int) -> ListOnList[T]:
    return ListOnList(ls, start)

