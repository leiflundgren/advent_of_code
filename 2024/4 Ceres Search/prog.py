from re import X
from directions import Direction
from map import Map, Node, Point
from text_map import TextMap
import tools
from enum import Enum
from typing import Iterable, Iterator, List, Self, Sequence, Tuple


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

def has_x_mas(m : TextMap, x : int, y : int) -> bool :
    X = 'X'; M='M'; A='A'; S='S';


    if A != m.at(x, y): return False
    nw = m.at(x-1, y-1)
    sw = m.at(x-1, y+1)
    ne = m.at(x+1, y-1)
    se = m.at(x+1, y+1)

    l11 = (nw == M and se == S ); l12 = (nw == S and se == M )
    l21 = (ne == M and sw == S ); l22 = (ne == S and sw == M )

    l1 = (nw == M and se == S ) or (nw == S and se == M )
    l2 = (ne == M and sw == S ) or (ne == S and sw == M )

    l01 = l1 and l2
    l02 = l1 and l2

    return ((nw == M and se == S ) or (nw == S and se == M )) and ((ne == M and sw == S ) or (ne == S and sw == M ))
    

def find_all_x_mas(m : TextMap) -> List[Tuple[int, int]]:
    res = []
    for x in range(1, m.width()-1):
        for y in range(1, m.height()-1):
            if has_x_mas(m, x, y):
                res.append((x, y))
    return res