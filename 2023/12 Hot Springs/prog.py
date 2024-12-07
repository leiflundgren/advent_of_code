from pickle import FALSE
import tools
from enum import Enum
from typing import Iterable, Iterator, Self, Sequence, Tuple
import re
from itertools import tee
import functools
from copy import deepcopy
from tools import ListIter
from list_on_list import ListOnList

class Springs:
    
    NULL = ''
    EMPTY = '.'
    SPRING = '#'
    UNKNOWN = '?'
    
    instanceSeed = 0

    def __init__(self, springs:Sequence[tuple[str, int]], arrangment:Sequence[int]):
        
        self.springs = ListOnList(springs) if isinstance(springs, list) else springs
        self.arrangment = ListOnList(arrangment) if isinstance(arrangment, list) else arrangment
        assert isinstance(self.springs, ListIter) or isinstance(self.springs, ListOnList)
        assert isinstance(self.arrangment, ListIter) or isinstance(self.arrangment, ListOnList)
        self.id = ++Springs.instanceSeed

    def revstr(self) -> str:
        return ('rev' if self.springs.is_reversed else 'fwd')

    def __str__(self):
        return Springs.makestring(self.springs, self.arrangment)

    def __repr__(self):
        return 'Springs: ' + str(self)
    
    def __hash__(self) -> int:
        return tools.hashOfList(self.springs)
    
    @staticmethod
    def equals(x : Self, y : Self) -> bool:
        if len(x.springs) != len(y.springs): return False
        if len(x.arrangment) != len(y.arrangment): return False
        if x.springs != y.springs : return False
        if x.arrangment != y.arrangment: return False
        return True

    def __eq__(self, other):
        return Springs.equals(self, other)

    def sum_springs_and_unknown(self) -> int:
        if len(self.springs) == 0: return 0
        
        if isinstance(self.springs[0], tuple):        
            return sum(map(lambda t: t[1], self.springs))
        else:
            return len(self.springs)
        
    def sum_arrangement(self) -> int:
        return sum(self.arrangment)

    def is_empty(self):
        return 0 == len(self.springs) or 0 == len(self.arrangment)
    def not_empty(self):
        return not self.is_empty()
    
    def get_reversed(self):
        return Springs(self.springs.get_reversed(), self.arrangment.get_reversed())

    def get_spring_at(self, idx:int) -> str:
        return self.springs[idx][0] if idx < len(self.springs) else ''

    def get_spring(self, idx:int) -> Tuple[str, int]:
        return self.springs[idx] if idx < len(self.springs) else ('',0)

    def get_arragment(self, idx:int) -> int:
        return self.arrangment[idx] if idx < len(self.arrangment) else 0

    def pop_arragment(self) -> Self:
        return Springs(self.springs, self.arrangment.slice_front())
    def pop_spring(self) -> Self:
        return Springs(self.springs.slice_front(), self.arrangment)
    def pop_both(self) -> Self:
        return Springs(self.springs.slice_front(), self.arrangment.slice_front())

    def __copy__(self):
        return self.copy(True)
    def copy(self, deep_copy = False) -> Self:
        return self.sub(0, len(self.springs), 0, len(self.arrangment), deep_copy)

    def sub(self, spring_begin, spring_end ,arr_begin, arr_end, deep_copy = False) -> Self:
        if deep_copy:
            return Springs(ListIter(self.springs.inner[spring_begin:spring_end]), ListIter(self.arrangment.inner[arr_begin:arr_end]))
        else:
            return Springs(ListOnList(self.springs.inner[spring_begin:spring_end]), ListOnList(self.arrangment.inner[arr_begin:arr_end]))

    def pretty_str(self) -> str:
        pre = ''    
        if len(self.springs) > 0:
            pre = ''.join(map(lambda t: t[0]*t[1], self.springs))
        
        return f'{pre}  {self.arrangment}'

    @staticmethod
    def makestring(springs:Sequence[tuple[str, int]], arrangment:Sequence[int]) -> str:
        
        pre = ''
        try :
            if len(springs) > 0 and isinstance(springs[0], tuple):
                pre = ''.join(map(lambda t: t[0]*t[1], springs))
        except:
            bp = 17
        return  pre + f'  {springs}     {arrangment}'
        
    def reduce(self, id = None) -> bool:
        
        EMPTY = Springs.EMPTY
        SPRING = Springs.SPRING 
        UNKNOWN = Springs.UNKNOWN 
        
        print("start:            " + str(self))
        any_reduce = False
        reduced = True
        while reduced and self.springs.not_empty() and self.arrangment.not_empty():
            def reductor(tup) -> bool:
                (name, method) = tup
                if not method(): return False
                
                self.join_springs()
                print(name, str(self))

                for s in self.springs:
                    (ch, cnt) = s
                    assert cnt > 0, "Spring count should be positive"

                return True

            reducers = [
                ("sum-match         ", self.reduce_sum_match),
                ("fwd-empty-front   ", self.reduce_front_empty),
                ("first spring      ", self.reduce_first_spring),
                ("back-first spring ", self.get_reversed().reduce_first_spring),
                ("front_mix_matches ", self.reduce_front_mix_matches),
                ("back_mix_matches  ", self.get_reversed().reduce_front_mix_matches),
                ("back-empty-front  ", self.get_reversed().reduce_front_empty),
                ("fwd-count-match   ", self.reduce_front_spring_matches),
                ("back-count-match  ", self.get_reversed().reduce_front_spring_matches),
                ("match-max         ", self.reduce_max),
                ("orphan            ", self.reduce_orphan_empty),
                ("just one emptry   ", self.reduce_wildcard_allow_just_one_empty),
            ]
            reduced = any(map(reductor, reducers))
            any_reduce = any_reduce or reduced
          
        print("reduced: ", str(self))
        return any_reduce

    def reduce_sum_match(self) -> bool:
        if self.sum_springs_and_unknown() == self.sum_arrangement():
            self.springs = ListIter([])
            self.arrangment = ListIter([])
            return True
        return False

    def reduce_front_empty(self) -> bool:
        if self.springs.is_empty() or self.arrangment.is_empty():
            return False

        (spring, cnt) = self.springs.front()
        if spring == Springs.EMPTY:
            self.springs.pop();
            return True   
        return False
    
    def reduce_front_spring_matches(self) -> bool:
        if self.springs.is_empty() or self.arrangment.is_empty():
            return False

        (spring, cnt) = self.springs.front()
        if spring == Springs.SPRING and cnt == self.arrangment.front():
            self.springs.pop();
            self.arrangment.pop();
            return True   
        return False

    def reduce_front_mix_matches(self) -> bool:
        if self.springs.is_empty() or self.arrangment.is_empty():
            return False

        arr = self.arrangment[0]
        sum = 0
        last = '\0'
        for i in range(len(self.springs)):
            (chr, cnt) = self.springs[i]
            if chr != Springs.SPRING and chr != Springs.UNKNOWN:
                return False
            if last == Springs.SPRING and chr != Springs.UNKNOWN:
                return False
            if last == Springs.UNKNOWN and chr != Springs.SPRING:
                return False
            sum = sum + cnt
            
            # sum match perfectly
            # or eat a few unknowns, leave the rest 
            if sum == arr and chr == Springs.SPRING and last == Springs.UNKNOWN \
                or sum >= arr and chr == Springs.UNKNOWN and last == Springs.SPRING:
                
                #check i=[0,j] matches cond
                # start with spring or all all unknown are only 1 long
                # (check we have some spring, not only unknown)
                    
                    self.arrangment.pop()
                    for j in range(i):
                        self.springs.pop()
                    self.springs[0] = (Springs.UNKNOWN, sum-arr)            

                    
                    return True   
            
            last = chr
        return False


    def reduce_front(self) -> bool:
        EMPTY = Springs.EMPTY
        SPRING = Springs.SPRING 
        UNKNOWN = Springs.UNKNOWN 

        if self.springs.is_empty() or self.arrangment.is_empty():
            return False

        (spring, cnt) = self.springs.front()
        arr = self.arrangment.front() if self.arrangment.not_empty() else 0


        (reduced_fwd, pop_springs, pop_arragement) = Springs.can_reduce(spring, cnt, arr)
        if reduced_fwd:
            if pop_springs: self.springs.pop()
            if pop_arragement: self.arrangment.pop()


            if spring == Springs.SPRING and len(self.springs) > 0:
                (frnt, cnt) = self.springs[0]
                if frnt == Springs.UNKNOWN: # next idx must be empty
                    self.springs[0] = (frnt, cnt-1)
                    self.springs.insert(0, (Springs.EMPTY, 1))
                
            
            return True
            
        return False

    def reduce_max(self) -> bool:
        if self.is_empty() : return False
        
        max_a = max(self.arrangment)
        max_s = max(self.springs, key=lambda s: s[1] if s[0] == Springs.SPRING or s[0] == Springs.UNKNOWN else 0)
        
        if max_a == max_s[1]:
            s_idx = self.springs.index(max_s)

            self.arrangment.remove(max_a)
            self.springs.remove(max_s)
            
            #we also know that left+right side must be empty.
            (ch, cnt) = self.springs[0]
            if ch == Springs.UNKNOWN:
                self.springs[0] = (ch, cnt-1)
                self.springs.insert(0, (Springs.EMPTY, 1))

            
            return True            

        return False
        
    def reduce_orphan_empty(self) -> bool:        
        if self.is_empty() : return False
    
    # first_non_wildcard = self.springs.index_cond(lambda s: s[0] != Springs.UNKNOWN)
        # if first_non_wildcard < 0:
        #     return False
        # (spring, cnt) = self.springs[first_non_wildcard]
        
        # for i in range(first_non_wildcard-1, -1, -1):
        #     (unknown, cnt2) = self.springs[i]
        #     if 
        #     self.springs.pop(i)
        #     self.arrangment.pop(i)
        # return True
        
        arr = self.arrangment.front()
        changed = False
        
        (ch, cnt) = self.springs.front()
        if ch == Springs.UNKNOWN and cnt < arr:
            self.springs.pop()
            
            return True
        
        return False

    def reduce_wildcard_allow_just_one_empty(self) -> bool:
        if len(self.arrangment) < 2 or self.arrangment.is_empty():
            return False
        
        a1 = self.arrangment[0]
        a2 = self.arrangment[1]
        
        (char, cnt) = self.springs[0]

        if char == Springs.UNKNOWN and (a1 == 1 or a2 == 1) and (a1 + a2 + 1 == cnt):
            # Only room for 1 empty between springs
            self.arrangment.pop()
            self.arrangment.pop()
            self.springs.pop()
            
            #self.change_before_after_to(1, Springs.EMPTY)
            if len(self.springs) > 0:
                (frnt, cnt) = self.springs[0]
                if frnt == Springs.UNKNOWN:
                    self.springs.insert(0, (Springs.EMPTY, 1))
                    self.springs[1] = (Springs.UNKNOWN, cnt-1)

            
            return True
        
        return False

    def reduce_first_spring(self) -> bool:
        if len(self.springs) < 2 or self.arrangment.is_empty():
            return False
        (chr0, cnt0) = self.springs[0]
        (chr1, cnt1) = self.springs[1]
        arr = self.arrangment[0]
        # we must have 1 empty, then all springs
        if chr0 == Springs.UNKNOWN and chr1 == Springs.SPRING and (cnt0+cnt1 - 1) == arr:
            self.springs.pop()
            self.springs.pop()
            self.arrangment.pop()
            
            # now next after, must be empty
            if self.springs.not_empty():
                (nxt, cnt) = self.springs[0]
                self.springs[0] = (nxt, cnt-1)
                self.springs.insert(0, (Springs.EMPTY, 1))

            
            return True
        
        return False
    # def change_before_after_to(self, idx:int, chr:str) -> None:
    #     if idx +1 < len(self.springs):
    #         (c_old, cnt) = self.springs[idx+1]
    #         if c_old == Springs.UNKNOWN:
    #             if cnt ==1:
    #                 self.springs[idx+1] = (chr, 1)
    #             else:
    #                 self.springs[idx] = (c_old, cnt-1)
    #                 self.springs.insert(idx, (chr, 1))
                    
    #     if idx >= 1:
    #         (c_old, cnt) = self.springs[idx]
    #         if c_old == Springs.UNKNOWN:
    #             if cnt ==1:
    #                 self.springs[idx+1] = (chr, 1)
    #             else:
    #                 self.springs[idx+1] = (c_old, cnt-1)
    #                 self.springs.insert(idx+2, (chr, 1))
                         
    # if we have two of the same kind, join them
    # return true if changed
    def join_springs(self) -> bool:
        changed = False
        idx = 0
        
        while idx < len(self.springs):
            (chr0, cnt0) = self.springs[idx]
            if cnt0 == 0:
                self.springs.pop(idx)
                changed = True
                continue


            if idx+1 < len(self.springs):
                (chr1, cnt1) = self.springs[idx+1]
                if chr0 == chr1:
                    self.springs[idx] = (chr0, cnt0+cnt1)
                    self.springs.pop(idx+1)
                    changed = True
                    continue

            idx=idx+1
        return changed
    
    def five_fold(self):
        unknown = [(Springs.UNKNOWN, 1)]
        springs = self.springs.get_inner()
        arr = self.arrangment.get_inner()
        five_springs = springs + unknown +springs + unknown +springs + unknown +springs + unknown +springs
        five_arr = arr+arr+arr+arr+arr
        return Springs(five_springs, five_arr)
                    
def parse_springs(s:str) -> Springs:
    def parse_springs_(s:str) -> list[tuple[str, int]]:
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
        
    if s == '???.????...???#?#? 2,4,2,4':
        bp = 17

    space = s.index(' ')
    springs = parse_springs_(s[:space])
    arrangment = parse_arrangment(s[space+1:])
    return Springs(ListIter(springs), ListIter(arrangment))

