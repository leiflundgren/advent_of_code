
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
    
    def is_vertical(self) -> bool:
        return self == Direction.N or self == Direction.S
    def is_horizontal(self) -> bool:
        return self == Direction.E or self == Direction.W

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

    def mirror(self, typ:str) -> Self:
        if typ != '╱' and typ != '╲':
            raise ValueError(f'Mirror should be one of ╲, ╱  got "{typ}"')
        
        if self == Direction.N:
            return  Direction.E if typ == '╱' else Direction.W
        elif self == Direction.E:
            return  Direction.N if typ == '╱' else Direction.S
        elif self == Direction.S:
            return  Direction.W if typ == '╱' else Direction.E
        elif self == Direction.W:
            return  Direction.S if typ == '╱' else Direction.N
        else:
            raise ValueError(f'Mirror only handles N/W/S/E got "{self}"')
            
    def splitter(self, typ:str) -> list[Self]:
        if typ != '|' and typ != '⎯':
            raise ValueError(f'Splitter should be one of |, -  got "{typ}"')
        
        if self == Direction.N or self == Direction.S:
            return [self] if typ == '|' else [Direction.W, Direction.E]
        elif self == Direction.E or self == Direction.W:
            return [self] if typ == '⎯' else [Direction.N, Direction.S]
        else:
            raise ValueError(f'Mirror only handles N/W/S/E got "{self}"')
            
    def move_light_beam(self, typ:str) -> list[Self]:
        if typ == '.':
            return [self]
        elif typ == '╱' or typ == '╲':
            return [self.mirror(typ)]
        elif typ == '|' or typ == '⎯':
            return self.splitter(typ)
        else:
            raise ValueError(f'Mirror only handles N/W/S/E got "{typ}"')
        
    @classmethod
    @property
    def N(cls):
        return Direction('N', 0)
    @classmethod
    @property
    def NE(cls):
        return Direction('NE', 45)
    @classmethod
    @property
    def E(cls):
        return Direction('E', 90)
    @classmethod
    @property
    def SE(cls):
        return Direction('SE', 135)
    @classmethod
    @property
    def S(cls):
        return Direction('S', 180)
    @classmethod
    @property
    def SW(cls):
        return Direction('SW', 225)
    @classmethod
    @property
    def W(cls):
        return Direction('W', 270)
    @classmethod
    @property
    def NW(cls):
        return Direction('NW', 315)

    @classmethod
    @property
    def four_dir(cls):
        return [Direction.N,Direction.E,Direction.W,Direction.S]
    @classmethod
    @property
    def eight_dir(cls):
        return [Direction.N, Direction.NE, Direction.E, Direction.SE, Direction.S, Direction.SW, Direction.W, Direction.NW]

    @classmethod
    @property
    def char_vertial(cls): return '|'
    
    @classmethod
    @property
    def char_horizontal(cls): return '⎯'
    
    @classmethod
    @property
    def char_forward_angle(cls): return '╱'
    
    @classmethod
    @property
    def char_back_angle(cls): return '╲'
    

#def angle_dir(d1:str, d2:str) -> str
# 
def direction(p1:tuple[int,int], p2:tuple[int,int]) -> str:
    (x1, y1) = p1
    (x2, y2) = p2
    if y1 != y2:
        return Direction.N if y1 > y2 else Direction.S
    if x1 != x2:
        return Direction.S if x1 > x2 else Direction.E
    raise ValueError(f'Innvalid direction {p1}->{p2}')

