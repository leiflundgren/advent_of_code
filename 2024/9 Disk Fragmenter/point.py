
from typing import List, Self

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
       
    @staticmethod
    def diff_points(p1 : Self, p2 : Self) -> Self:
        q1 = Point.create(p1)
        q2 = Point.create(p2)
        return Point(q1.x-q2.x, q1.y-q2.y)

    @staticmethod
    def max(p1 : Self, p2 : Self) -> Self:
        q1 = Point.create(p1)
        q2 = Point.create(p2)
        return Point(max(q1.x,q2.x), max(q1.y,q2.y))
    @staticmethod
    def min(p1 : Self, p2 : Self) -> Self:
        q1 = Point.create(p1)
        q2 = Point.create(p2)
        return Point(min(q1.x,q2.x), min(q1.y,q2.y))

    @staticmethod
    def equals(p1 : Self, p2 : Self) -> Self:
        q1 = Point.create(p1)
        q2 = Point.create(p2)
        return q1.x == q2.x and q1.y == q2.y
        
    def in_bounds(self, pmin : Self, pmax : Self) -> bool:
        return pmin.x <= self.x and pmin.y <= self.y and self.x <= pmax.x and self.y <= pmax.y

    def abs(self) -> Self:
        return Point(abs(self.x), abs(self.y))

    def neg(self) -> Self:
        return Point(-self.x, -self.y)


    ### @len, if 0, result is 1 Point, if N, result is N+1 points
    def path_dir(self, dir : Direction, len : int, bounds_min : Self = None, bounds_max : Self = None) -> List[Self] :
        if bounds_min is None != bounds_max is None: raise ValueError("Specify both min and max bounds, or none")

        offset = dir.offset_dir()
        pos = self
        res = [pos]
        for i in range(len):
            pos = Point.add_points(pos, offset)

            if not bounds_min is None and not bounds_max is None and not pos.in_bounds(bounds_min, bounds_max):
                return None

            res.append(pos)
        return res

    def __eq__(self, other) -> bool:
        return Point.equals(self, other)

    def __hash__(self) -> int:
        return hash(self.x) + 3* hash(self.y)

    def __repr__(self) -> str:
        return f'({self.x},{self.y})'

class Vector(object):
    def __init__(self, pos : Point, dir : Direction):
        self.pos = pos
        self.dir = dir

    def __eq__(self, other) -> bool:
        return Point.equals(self.pos, other.pos) and self.dir == other.dir

    def __hash__(self) -> int:
        return hash(self.pos.x) + 3* hash(self.pos.y) + 7*hash(self.dir)

    def __repr__(self) -> str:
        return f'({self.dir} {self.pos.x},{self.pos.y})'
