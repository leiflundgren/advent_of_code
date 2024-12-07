
import functools
import typing
from typing import Iterable, Self

from directions import Direction

Node = typing.NewType('Node', None)

def sort_nodes_cmp(n1:Node, n2:Node) -> int:

    if n1.y != n2.y: return n1.y - n2.y
    return n1.x - n2.x 

def sort_nodes(nodes : Iterable[Node]) -> Iterable[Node] :
    return sorted(nodes, key=functools.cmp_to_key(sort_nodes_cmp))
   
class Node:
    from fields import Field
    from pipes import  Pipe
    import pipes
    
    def __init__(self, field:Field, value:Pipe, x:int, y:int, tag = None):
        self.field = field
        self.value = value
        self.x = x
        self.y = y
        self.tag = tag
       
    def __str__(self) -> str:
        return self.value.print_char

    def __repr__(self) -> str:
        return f'Node [{self.x},{self.y}] {self.value}'
    
    def __eq__(self, __value: object) -> bool:
        return self.x == __value.x and self.y == __value.y

    def copy(self, field:Field = None) -> Self:
        return Node(field, self.value, self.x, self.y, self.tag)

    def coord(self) -> tuple[int, int] :
        return (self.x, self.y)
    
    def inside_bounds(self) -> bool:
        return self.field.inside_bounds(self.x, self.y)

    @staticmethod
    def clear_tags(thing) -> None:
        if isinstance(thing, Node):
            thing.tag = None
        else:
            for n in thing:
                Node.clear_tags(n)

    def coord_dir(self, dir:Direction) -> tuple[int, int]:
        (off_x, off_y) = dir.offset_dir()
        return (self.x + off_x, self.y + off_y)

    def move_dir(self,dir:Direction) -> Self:
        assert not self.field is None, 'Cannot move a node not bound to a field'
        (x,y) = self.coord_dir(dir)
        return self.field.get(x, y)
    
    def move_nopipe(self,dir:Direction) -> Self:
        import pipes
        n = self.move_dir(dir)
        return n if n.inside_bounds() and n.value == pipes.PIPE_NO_PIPE else None


    def connect(self, dir:Direction) -> Self:
        import pipes
        
        (x_off, y_off) = dir.offset_dir()
        (x, y) = (self.x + x_off, self.y + y_off)
        
        if not self.field.inside_bounds(x, y): return None
        n = self.field.get(x, y)
        if not n.inside_bounds(): return None;
        if not pipes.can_connect(self.value, n.value, dir): return None

        return n;

    def connect_one(self) -> list[Self]:
        return list(filter(lambda n: not n is None, map(lambda dir: self.connect(dir), Direction.four_dir)))
    
    def find_outside(self) -> list[str]:
        import pipes
        
        def is_outside_dir(dir:Direction)->Node:
            n = self.move_dir(dir)
            return n.value == pipes.PIPE_OUTSIDE

        return list(filter(is_outside_dir, Direction.eight_dir))
    
    # strictly for sneaking between two pipes
    def sneak(self, dir:Direction, outsside_dir:Direction) -> Self:
        dir_left = dir.left()
        dir_op = dir_left.left()
        dir_right = dir_op.left()
                
        if self.value.blocks(dir):
            return None
        
        if self.value.has_pipe and not self.value.has_directions(dir): return None
        
        n = self.move_dir(dir)
        
        if not n.inside_bounds(): return None
        if not n.value.has_pipe: return None
        if self.value.has_directions(dir):
            if not n.value.has_directions(dir_op): return None
        else:
            if not n.value.has_directions(dir): return None


        n_left = n.move_dir(dir_left)
        n_right = n.move_dir(dir_right)
        
        if self.value.has_directions(dir) and n.value.has_directions(dir_op):
            # either left or right  should have same dir
            if not n_left.value.has_directions(dir_op) and not n_right.value.has_directions(dir_op):
                return None
        
        if n.y == 2 and 2 <= n.x and n.x <= 7:
            bp = 17

        return n
        
        # if not self.value.has_pipe:
        #     if not n.value.has_pipe: return n # without pipes, sneak free
        #     elif n.value.blocks(dir): return None
        #     if n.value.has_directions(dir): # this is an angle maybe we can sneak
        #         if n.value.has_directions(dir_left):
        #             n_right = n.move_dir(dir_right)
        #             if n_right.value.has_directions(dir): # sneak between two
        #                 return n
        #             else: return None
        #         elif n.value.has_directions(dir_right):
        #             n_left = n.move_dir(dir_left)
        #             if n_left.value.has_directions(dir): # sneak between two
        #                 return n
        #             else: return None
        #         else: return None
                
        #     else: return None
        # elif not n.value.has_pipe:
        #     return n
        
        # else:
        #     if not n.value.has_pipe \
        #         and not self.value.has_directions(dir) \
        #         and self.value.has_directions(dir.opposite()): 
        #         return n # leaving pipe, angling away
        #     elif Pipe.directions_connect(self.value, dir, n.value): 
        #         n_left = n.move_dir(dir_left)
        #         n_right= n.move_dir(dir_right)
        #         if n_left.value == pipes.PIPE_OUTSIDE or n_right.value == pipes.PIPE_OUTSIDE:
        #             return None # nope. move here different path
        #         return n            
        #     else: 
        #         return None

    def move_nopipe_one(self) -> list[Self]:
        ls = []
        for dir in Direction.four_dir:
            n = self.move_nopipe(dir)
            if not n is None:
                ls.append(n)
        return ls

    def sneak_one(self, outside:Direction) -> list[Self]:
        import pipes
        
        outsides = list(filter(lambda n: n.value is pipes.PIPE_OUTSIDE, map(lambda d: self.move_dir(d), Direction.four_dir)))

        ls = []
        for dir in Direction.four_dir:
            n = self.sneak(dir, outside)
            if not n is None:
                if n.x==2 and 2 <= n.y and n.y <= 5:
                    bp =17
                if n.x==3 and n.y == 5:
                    bp =17
                ls.append(n)
        return ls
        return list(filter(lambda n: not n is None, map(lambda dir: self.sneak(dir), four_dir)))
        
        return list(filter(lambda n: not n is None, map(lambda dir: self.sneak(dir), four_dir)))
    
    def coonnected_neighbors(self) -> list[Self]:
        valid_dir = list( filter( lambda d: not self.connect(d) is None, Direction.four_dir))
        return list(map( lambda d: self.connect(d), valid_dir))
  