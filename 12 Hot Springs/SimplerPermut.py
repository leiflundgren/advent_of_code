
from typing import Dict
from prog import Springs
from list_on_list import ListOnList
import tools

class Perm2:
    def __init__(self, use_cache:bool):
        self.use_cache = use_cache

    def calc_permutations(self, scen:Springs) -> int:
        self.cache : Dict[Springs, int] = {}
        expanded_strings = []
        for (chr, cnt) in scen.springs:
            if chr == Springs.SPRING:
                expanded_strings.append( (chr, cnt))
            else:
                for i in range(cnt):
                    expanded_strings.append( (chr, 1))
                    
        return self.calc(Springs(ListOnList(expanded_strings), ListOnList(tools.get_inner_list(scen.arrangment))))

    def calc(self, scen : Springs) -> int:
        p = self.calc_inner(scen)
        print(f'{scen.pretty_str()} --> {p}')
        if p == 1:
            bp = 17
        return p


    def calc_inner(self, scen : Springs) -> int:
        arr = scen.get_arragment(0)
        (chr, cnt) = scen.get_spring(0)
        
        if chr == Springs.EMPTY:
           return self.calc(scen.pop_spring())
        
        if arr == 0:
            if chr == Springs.UNKNOWN:
                return self.calc(scen.pop_spring())
            if chr == Springs.NULL:
                return 1 
            else:
                return 0
        if chr == Springs.NULL: # since len(arr)>0 we failed to place something
            return 0

        if self.use_cache:
            cached = self.cache.get(scen, None)
            if not cached is None:
                return cached
    


        if chr == Springs.SPRING:
            return self.calc_assume_spring(scen)

        # Two cases, either Empty or Spring!
        cnt_spring = self.calc_assume_spring(scen)
        cnt_empty = self.calc_assume_empty(scen)
        
        if self.use_cache:
            self.cache[scen] = cnt_spring + cnt_empty

        return cnt_spring + cnt_empty

    def calc_assume_empty(self, scen : Springs) -> int:
        
        assert Springs.UNKNOWN == scen.get_spring_at(0)

        return self.calc(scen.pop_spring())

        # SPRING
    def calc_assume_spring(self, scen : Springs) -> int:
        
        assert Springs.UNKNOWN == scen.get_spring_at(0) or Springs.SPRING == scen.get_spring_at(0)
        
        if str(scen).startswith('#?#?#?  '):
            bp = 17
            
        arr = scen.get_arragment(0)
        scen0 = scen
        to_eat = arr      
        pos = 0
        scen1 = []
        for pos in tools.natural_numbers(0):
            (chr, cnt) = scen.get_spring(0)
            if chr == Springs.EMPTY or chr == Springs.NULL:
                # failed to match
                return 0
            scen1.append(scen)
            scen = scen.pop_spring()
            to_eat = to_eat - cnt
            if to_eat < 0:
                return 0
            if to_eat == 0:
                break

        (after, cnt) = scen.get_spring(0)
        if after == Springs.SPRING:
            # after an arr, must be empty
            return 0
        assert cnt == 1 or after == Springs.NULL
        assert after == Springs.EMPTY or after == Springs.UNKNOWN or after == Springs.NULL
        scen2 = scen
        scen = scen.pop_both()
        return self.calc(scen)

