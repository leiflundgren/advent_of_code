import copy
from itertools import combinations
from directions import Direction
from point import Point, Vector
from map import Map, Node
from text_map import TextMap
import tools
from enum import Enum
from typing import Dict, Generator, Iterable, Iterator, List, Self, Sequence, Set, Tuple

def find_interference_nodes(p1 : Point, p2 : Point) -> Tuple[Point, Point] :
    if p1.y > p2.y: return find_interference_nodes(p2, p1)

    dist = Point.diff_points(p2, p1)
    i1 = Point.diff_points(p1, dist)
    i2 = Point.add_points(p2, dist)
    return (i1, i2)

def all_pairs(col : List[Point]) -> Iterator[Tuple[Point, Point]]:
    for p1 in col:
        for p2 in col:
            if p1 != p2:
                yield (p1, p2)

class Worker(object):
    def __init__(self, m : TextMap):
        self.set_map(m)

    def set_map(self, m : TextMap) -> None:
        self.map = m
        self.by_freq : Dict[str, List[Point]] = {}

        for (p, val) in self.map.nodes():
            if val != '.':
                self.by_freq.setdefault(val, []).append(p)


    def find_interference_point(self) -> Iterator[Point] :
        seen : Set[Point] = set()
        for (hz, p_ls) in self.by_freq.items():
            for (p1, p2) in all_pairs(p_ls):
                for i in find_interference_nodes(p1, p2):
                    if not i in seen and self.map.contains(i):
                        seen.add(i)
                        yield i
