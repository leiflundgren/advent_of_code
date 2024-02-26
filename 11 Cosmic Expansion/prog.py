import tools
from enum import Enum
from typing import Iterator, Self
import re
from itertools import tee
import functools
from copy import deepcopy


class Map:
    
    EMPTY = '.'
    GALAXY = '#'

    def __init__(self, str:str, empty_cost:int = 2):
        self.raw_map = str.split()
        self.height = len(self.raw_map)
        self.width = len(self.raw_map[0])
        
        self.empty_cost = empty_cost
        self.cost_vertical = list(map(lambda n: empty_cost if self.is_empty_horizonal(n) else 1, range(self.height)))
        self.cost_horizontal = list(map(lambda n: empty_cost if self.is_empty_vertical(n) else 1, range(self.width)))
        
        self.galaxies = []
        for y in range(self.height):
            for x in range(self.width):
                if self.raw_map[y][x] == Map.GALAXY:
                    self.galaxies.append((x, y))
        self.pairs = []
            
    def is_empty_horizonal(self, n:int) -> bool:
        return all(map(lambda c: c == Map.EMPTY, self.raw_map[n]))
    def is_empty_vertical(self, n:int) -> bool:
        return all(map(lambda line: line[n] == Map.EMPTY, self.raw_map))
    
    def get(self, coord: tuple[int,int]) -> str:
        (x,y) = coord
        return self.raw_map[y][x]
    
    def cost(self, coord1 : tuple[int,int], coord2 : tuple[int,int]) -> int:
        (x1,y1) = coord1
        (x2,y2) = coord2

        # length is same if mirrored
        if x1 > x2: (x1, x2) = (x2, x1)
        if y1 > y2: (y1, y2) = (y2, y1)

        return \
            sum(map(lambda x:self.cost_horizontal[x], range(x1, x2))) \
            + sum(map(lambda y:self.cost_vertical[y], range(y1, y2)))
    
    def get_galaxie_pairs(self):
        if len(self.pairs) == 0:
            for g1 in range(len(self.galaxies)-1):
                for g2 in range(g1+1, len(self.galaxies)):
                    if g1 != g2:
                        self.pairs.append((self.galaxies[g1], self.galaxies[g2]))
        return self.pairs
                    

    def sum_dist_pairs(self):
        pairs = self.get_galaxie_pairs()
        return sum(map( lambda pair: self.cost(*pair), pairs))
            

