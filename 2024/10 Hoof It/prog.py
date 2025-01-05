from re import X
from directions import Direction
from map import Map, Node, Point, Vector
from text_map import TextMap
import tools
from enum import Enum
from typing import Dict, Generator, Iterable, Iterator, List, Self, Sequence, Tuple


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

class WalkResult(Enum):
    UNKNOWN=1
    LEFT_MAP=2
    LOOP=3

class Guard(object):
    OBSTACLE = '#'
    CLEAR = '.'
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

    def clear_history(self, start_pos:Vector) -> None:
        self.history = [] # create new, leave old in mem
        self.history_dict = {}
        self.set_pos(start_pos)

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

    def move_one(self) -> WalkResult:
        p = self.pos();
        v_ = self.next_pos()
        visits_to_point_before = self.history_dict.get(v_.pos)
        if visits_to_point_before is not None and v_ in visits_to_point_before:
            print(f'found loop')
            return WalkResult.LOOP
        elif not self.map.is_inside(v_.pos.x, v_.pos.y):
            return WalkResult.LEFT_MAP
        else:
            self.set_pos(v_)
            return WalkResult.UNKNOWN

    def walk_path(self) -> WalkResult:
        while True:
            r = self.move_one()
            if r != WalkResult.UNKNOWN:
                return r
            pass

    def count_unique_positions(self) -> int:
        poss = [ v.pos for v in self.history ]
        uniq = set()

        for p in poss:
            uniq.add(p)
        return len(uniq)

    # Returns list of where to add obstacle
    def modify_path_to_create_loops(self) -> List[Point]:
        res = []
        for p in self.modify_path_to_create_loops_yield():
            res.append(p)
        return res

    def modify_path_to_create_loops_yield(self) -> Generator[Tuple[int, Point], None, None]:

        gtmp = Guard(self.history[0], self.map)

        to_test = set([v.pos for v in self.history[1:]])

        # skip first pos, since guard is already there
        for (n, pos) in zip(tools.natural_numbers(), to_test):
            # clear history, set to start pos
            gtmp.clear_history(self.history[0])

            # mark point as obstable
            gtmp.map.set(pos.x, pos.y, Guard.OBSTACLE)

            r = gtmp.walk_path()

            # clear point as obstable
            gtmp.map.set(pos.x, pos.y, Guard.CLEAR)
            
            if r == WalkResult.LOOP:
                yield (n, pos)

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