



from typing import Dict, List, Self, Tuple

from directions import Direction
from point import Point



class Node(object):
    def __init__(self, pos : Point, value : str = None):
        self.pos = pos
        self.map = None
        self.value = value
        self.bounds = (Point(0,0), Point(-1, -1))
        pass
        
    def __hash__(self) -> int:
        return hash(self.pos)

    def __repr__(self) -> str:
        return str(self.value) + ':' + self.pos.__repr__()

    def path(self, dir : Direction, len : int, bounds_min : Point = None, bounds_max : Point = None) -> List[Self]:
        points = self.pos.path_dir(dir, len, bounds_min, bounds_max)
        return None if points is None else [ self.map.get(p) for p in points ]

class Map(object):
    def __init__(self):
        self.map : Dict[Tuple[int, int], Node] = {}
        self.bounds = (Point(0, 0), Point(-1, -1))
        
        pass

    @staticmethod 
    def create(width : int, height : int) -> Self:
        m = Map()
        for x in range(width):
            for y in range(height):
                m.add(Node(Point(x,y)))
        return m

    def add(self, n : Node):
        self.map[n.pos] = n
        (pmin, pmax) = self.bounds
        self.bounds = (Point.min(pmin, n.pos), Point.max(pmax, n.pos))
        n.map = self

    def get(self, p : Point):
        return self.map[p]

    def values(self) -> List[Node]:
        return self.map.values()



