from re import X
from directions import Direction
from map import Map, Node, Point, Vector
from text_map import TextMap
import tools
from enum import Enum
from typing import Dict, Iterable, Iterator, List, Self, Sequence, Tuple


def parse_map(txtmap: str) -> Map:
    lines = txtmap.strip('\r\n').splitlines()
    m = Map()
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            c = line[x]
            m.add(Node(Point(x, y), c))
    return m

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

class Guard(object):
    OBSTACLE = '#'
    GUARD_MARK = '^'

    def find_guard_pos(map: TextMap) -> Vector:
        for x in range(map.width()):
            for y in range(map.height()):
                c = map.at(x, y)
                if c == Guard.GUARD_MARK:
                    return Vector(Point(x, y), Direction.N)

    def __init__(self, vec : Vector, map : TextMap) -> None:
        self.map = map
        self.history : List[Vector] = []
        self.history_dict : Dict[Point, List[Vector]] = {}
        
        self.set_pos(vec)

    def pos(self): return self.vec.pos
    def dir(self): return self.vec.dir
    
    def set_pos(self, v:Vector) -> None:
        self.vec = v
        self.history.append(v)
        self.history_dict.setdefault(v.pos, []).append(v)

    def next_pos(self) -> Vector:
        d_ = self.dir()
        for attempt in range(4):
            (dx, dy) = d_.offset_dir()
            p_ = Point.add_points(self.pos(), Point(dx, dy))

            c = self.map.at(p_.x, p_.y)
            if c != Guard.OBSTACLE:
                return Vector(p_, d_)

            # Turn right
            d_ = d_.right()

        raise ValueError(f'Could not move from {self.pos()}. Seems boxed in!')

    def move_one(self) -> bool:
        p = self.pos();
        v_ = self.next_pos()
        if any( v == v_ for v in self.history):
            print(f'found loop')
            return False
        elif self.map.is_inside(v_.pos.x, v_.pos.y):
            self.set_pos(v_)
            return True
        else:
            return False

    def walk_path(self):
        while self.move_one():
            pass

    def count_unique_positions(self) -> int:
        poss = [ v.pos for v in self.history ]
        uniq = set()

        for p in poss:
            uniq.add(p)
        return len(uniq)

    def print_path(self, def_print, highlight_print):
        for y in range(self.map.height()):
            for x in range(self.map.width()):
                c = self.map.at(x, y)
                pr = def_print
                  
                p = Point(x,y)
                v = self.history_dict.get(p)
                if v is not None:
                    pr = highlight_print
                    c = v[0].dir.to_arrow()
                                        
                pr(c + ' ')
            print()