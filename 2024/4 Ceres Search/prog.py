from re import X
from directions import Direction
from map import Map, Node, Point
import tools
from enum import Enum
from typing import Iterable, Iterator, List, Self, Sequence, Tuple


def parse_map(txtmap: str) -> Map:
    lines = txtmap.splitlines()
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
    return list(tools.find_all( [ n.path(d, len, pmin, pmax) for d in Direction.four_dir ], not_none))

def find_all_match(pattern : str, paths : List[List[Node]]) -> List[List[Node]]:
    def match(path : List[Node]) -> bool :
        if len(pattern) != len(path): 
            return False

        for c, n in zip(pattern, path):
            if c != n.value: 
                return False

        return True
    return list(tools.find_all(paths, match))