from directions import Direction
from map import Map, Node, Point, Point
from text_map import TextMap
import tools
from enum import Enum
from typing import Dict, Generator, Iterable, Iterator, List, Self, Sequence, Tuple


def get_all_paths_from(n : Node, len : int) -> List[List[Node]] :
    (pmin, pmax) = n.map.bounds
    def not_none(x):
        return not x is None
    return list(tools.find_all( [ n.path(d, len, pmin, pmax) for d in Direction.eight_dir], not_none))

def find_all_match(pattern : str, paths : List[List[Node]]) -> List[List[Node]]:
    def match(path : List[Node]) -> bool :
        if len(pattern) != len(path): 
            return False

        for c, n in zip(pattern, path):
            if c != n.value: 
                return False

        return True
    return list(tools.find_all(paths, match))

def count_all_matches_map(pattern : str, m : Map) -> int:
    res = 0
    for n in m.values():
        paths = get_all_paths_from(n, len(pattern)-1)
        matches = find_all_match(pattern, paths)
        l = len(matches)
        res += l
    return res

class WalkResult(Enum):
    UNKNOWN=1
    LEFT_MAP=2
    LOOP=3

class Path(object):
    OBSTACLE = '#'
    CLEAR = '.'
    

    def __init__(self, map : TextMap) -> None:
        self.map = map

    def at(self, p:Point) -> int:
        return self.map.at(p.x, p.y)

    def find_start_pos(self) -> Iterator[Point]:
        for (x, y, p) in self.map.nodes():
            if p == 0:
                yield Point(x, y)

    def next_pos(self, p:Point) -> List[Point]:
        v_ = self.at(p)
        res = []
        for d in Direction.four_dir:
            (dx, dy) = d.offset_dir()
            p_ = Point.add_points(p, Point(dx, dy))

            c = self.map.at(p_.x, p_.y)
            if c == 1+v_:
                res.append(p_)

        return res
      
    def walk_path(self, start : Point) -> List[List[Point]]:
        def walker(history : List[Point]) -> List[List[Point]]:
            last = history[-1]
            v = self.at(last)
            if v == 9:
                return [history] # one solution
            next = self.next_pos(last)
            res = []
            for n in next:
                paths = walker(history + [n])
                res.extend(paths)
            return res

        return walker([start])

    def generate_paths(self) -> List[List[Point]]:
        res = []
        for p in self.find_start_pos():
            for path in self.walk_path(p):
                endv = self.at(path[-1])
                if endv == 9:
                    res.append(path)
        return res

    def count_unique_positions(self) -> int:
        poss = [ p.pos for p in self.history ]
        uniq = set()

        for p in poss:
            uniq.add(p)
        return len(uniq)

    def to_string_map(m : TextMap, points : List[Point]) -> str:
        mp = TextMap.create_empty(m.width(), m.height(), -1)

        for p in points:
            mp.set(p.x, p.y, m.at(p.x, p.y))
        return str(mp)