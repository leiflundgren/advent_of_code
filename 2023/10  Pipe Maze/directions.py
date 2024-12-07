
from typing import Self


class Direction:
    def __init__(self, dir:str, angle:int):
        self.dir = dir
        self.angle = angle
                
    def __eq__(self, x: object) -> bool:
        return not x is None and self.dir == (x if isinstance(x, str) else x.dir)

    def __repr__(self) -> str:
        return f'dir:{self.dir}'
    def __str__(self) -> str:
        return self.dir

    def opposite(self) -> Self :
        return self.rotate(180)
    def left(self) -> Self :
        return self.rotate(-90)
    def right(self) -> Self :
        return self.rotate(90)

    def rotate(self, angle:int) -> Self:
        idx = Direction.eight_dir.index(self)
        if angle < 0:
            angle = 360 + angle
        if angle % 45 != 0: raise ValueError(f'Angle must be 45 degree multiplier')
        steps = angle//45
        idx = (idx+steps) % len(Direction.eight_dir)
        return Direction.eight_dir[idx]
    
    def offset_dir(self) -> tuple[int, int]:        
        if self == Direction.N: return (0, -1)
        if self == Direction.NE: return (1, -1)
        if self == Direction.E: return (1, 0)
        if self == Direction.SE: return (1, 1)
        if self == Direction.S: return (0, 1)
        if self == Direction.SW: return (-1, 1)
        if self == Direction.W: return (-1, 0)
        if self == Direction.NW: return (-1, -1)
        raise ValueError(f'Innvalid direction {dir}')


angle = 0
N=Direction('N', angle)
angle = angle+45
NE=Direction('NE', angle)
angle = angle+45
E=Direction('E', angle)
angle = angle+45
SE = Direction('SE', angle)
angle = angle+45
S=Direction('S', angle)
angle = angle+45
SW = Direction('SW', angle)
angle = angle+45
W=Direction('W', angle)
angle = angle+45
NW=Direction('NW', angle)

four_dir = [N,E,W,S]
eight_dir = [N, NE, E, SE, S, SW, W, NW]

Direction.eight_dir = eight_dir
Direction.four_dir = four_dir

Direction.N = N
Direction.NE = NE
Direction.E = E
Direction.SE = SE
Direction.S = S
Direction.SW = SW
Direction.W = W
Direction.NW = NW


#def angle_dir(d1:str, d2:str) -> str
# 
def direction(p1:tuple[int,int], p2:tuple[int,int]) -> str:
    (x1, y1) = p1
    (x2, y2) = p2
    if y1 != y2:
        return N if y1 > y2 else S
    if x1 != x2:
        return S if x1 > x2 else E
    raise ValueError(f'Innvalid direction {p1}->{p2}')

