



from typing import Dict, List, Self, Tuple

from directions import Direction


class Point(object):
    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y

    @staticmethod
    def create(a, *argv):
        if isinstance(a, Point): 
            return a
        if isinstance(a,tuple):
            return Point(a[0], a[1])
        if isinstance(a,int):
            return Point(a, argv[0])
        raise TypeError('cannot make a point out of ' + str(a))

    @staticmethod
    def add_points(p1 : Self, p2 : Self) -> Self:
        q1 = Point.create(p1)
        q2 = Point.create(p2)
        return Point(q1.x+q2.x, q1.y+q2.y)

    ### @len, if 0, result is 1 Point, if N, result is N+1 points
    def path_dir(self, dir : Direction, len : int) -> List[Self] :
        offset = dir.offset_dir()
        pos = self
        res = [pos]
        for i in range(len):
            pos = Point.add_points(pos, offset)
            res.append(pos)
        return res

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash(self.x) + 3* hash(self.y)

    def __repr__(self) -> str:
        return f'({self.x},{self.y})'

class Node(object):
    def __init__(self, pos : Point):
        self.pos = pos
        self.map = None
        pass
        
    def __hash__(self) -> int:
        return hash(self.pos)

    def __repr__(self) -> str:
        return self.pos.__repr__()

    def path(self, dir : Direction, len : int) -> List[Self]:
        points = self.pos.path_dir(dir, len)
        return [ self.map.get(p) for p in points ]

class Map(object):
    def __init__(self):
        self.map : Dict[Tuple[int, int], Node] = {}
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
        n.map = self

    def get(self, p : Point):
        return self.map[p]



