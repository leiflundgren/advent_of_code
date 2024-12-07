import math
import pipes
import typing
import directions

Node = typing.NewType("Node", None)


class Field:
    
    def __init__(self, node_iter = None):
        from nodes import Node
        def add_nodes(iterNodes):
            if iterNodes is None:
                pass
            elif isinstance(iterNodes, Node):
                self.set(iterNodes)
            else:
                for it in iterNodes:
                    add_nodes(it)
       
        self.field : dict[tuple[int, int], Node] = {}
        
        add_nodes(node_iter)
        self.set_bounds()
        
    def copy(self):
        return Field(self.all_nodes_unsorted())

    def get(self, x:int, y:int, create_if_not_found=True, store_if_not_found=False) -> Node:
        from nodes import Node

        if x is tuple:
            return self.get(x[0], x[1], y, create_if_not_found)

        # if outside, return a freshly minted no-pipe
        n = self.field.get((x, y), None)
        if n is None and create_if_not_found:
            n = Node(self, pipes.PIPE_NO_PIPE, x, y)
            if store_if_not_found:
                self.set(n)                
        return n

    def set(self, n:Node) -> None:
        self.field[n.coord()] = n
        n.field = self
        self.bounds = None
            
    def get_bounds(self)  -> tuple[tuple[int, int], tuple[int,int]]:
        if self.bounds is None:
            self.set_bounds()
        return self.bounds

    def set_bounds(self) -> None:
        if 0 == len(self.field):
            self.bounds = ((0,0), (0,0))
            return
        
        first = next(iter(self.field.values()))
        max_x = min_x = first.x
        max_y = min_y = first.y
        for n in self.field.values():
            min_x = min(n.x,min_x)
            min_y = min(n.y,min_y)
            max_x = max(n.x,max_x)
            max_y = max(n.y,max_y)
            
        self.bounds = ((min_x, min_y), (max_x, max_y))

    def inside_bounds(self, x:int, y:int) -> bool:
        ((min_x, min_y), (max_x,max_y)) = self.get_bounds()
        return min_x <= x and x <= max_x and min_y <= y and y <= max_y

    def all_nodes_sorted(self) -> list[Node]:
        from nodes import sort_nodes
        return list(sort_nodes(self.field.values()))
    def all_nodes_unsorted(self) -> list[Node]:
        return list(self.field.values())
    
    def get_all_coords(self) -> list[tuple[int, int]] :
        ((min_x, min_y), (max_x,max_y)) = self.get_bounds()
        ls = []
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                ls.append((x, y))
        return ls
                
    # empty nodes are not in dictionary. Fill them
    def fill_empty(self):
        from nodes import Node
        
        coords = self.get_all_coords()
        for (x, y) in coords:
            self.get(x, y, True, True)
    

    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self) -> str:
        def y_to_str(ls: list[Node]) -> str:
            return ''.join(map(lambda n: n.print_char, ls))
        def magnitude_order(num):
            if num == 0:
                return 0

            absnum = abs(num)
            order = math.log10(absnum)
            res = math.floor(order)

            return res
        
        ((min_x, min_y), (max_x,max_y)) = self.get_bounds()
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        
        field = []
        for y in range(min_y, 1+max_y):
            field.append( [pipes.PIPE_NO_PIPE] * (max_x+1-min_x))
        

        # xlen = max_x -min_x + 1
        # ylen = max_y -min_y + 1
        # line = PIPE_NO_PIPE.print_char * xlen + '\n'
        # field = line * ylen
        
        for n in self.field.values():
            field[n.y-min_y][n.x-min_x] = n.value

        lines = list(map(y_to_str, field))
        for i in range(len(lines)):
            lines[i] = f'{i:4} {lines[i]}'
        lines.append('')
        lines.append('  ' + '0123456789'*(width//10))
        return '\n'.join(lines)
    
    def get_start_pos(self) -> Node:
        return next(filter(lambda n: n.value == pipes.PIPE_START, self.field.values()), None)
    
    def nodes_between(self, n1:Node, n2:Node) -> list[Node]:
        if n1 is n2:
            return []
        if n1.x != n2.x and n1.y != n2.y: # only straight lines
            return []
        if n1.x == n2.x: # vertical
            return [ self.get(n1.x, y) for y in range(min(n1.y, n2.y)+1, max(n1.y, n2.y)) ]
        else: #horizontal
            return [ self.get(x, n1.y) for x in range(min(n1.x, n2.x)+1, max(n1.x, n2.x)) ]
 
    # direction to move from n1 to n2
    def direction(self, n1:Node, n2:Node) -> str:
        if n1.x != n2.x and n1.y != n2.y: # only straight lines
            return None 
        if n1.x == n2.x and n1.y == n2.y: # same nodes
            return None 
            
        if n1.x == n2.x:
            return S if n1.y < n2.y else N
        elif n1.y == n2.y:
            return E if n1.x < n2.x else W
        else: 
            return None

    def path_between(self, n1:Node, n2:Node) -> bool:
        dir = self.direction(n1, n2)
        if dir is None: return False
        n = n1
        while not n is None and n != n2:
            n = n.sneak(dir)
        return not n is None

        # between = self.nodes_between(n1, n2)
        # if len(between) == 0: return False
    
        # is_horizontal = n1.x == n2.x
        # if is_horizontal:
        #     return all(map(lambda n: n.value.has_E or n.value.has_W, between))
        # else:
        #     return all(map(lambda n: n.value.has_N or n.value.has_S, between))
    # Returns a Node, not added to field
    def find_start_pipe(self, n:Node) -> pipes.Pipe:
        should_have_directions = []
        for dir in directions.Direction.four_dir:
            op_dir = dir.opposite()
            nb = n.move_dir(dir)
            if nb.inside_bounds() and nb.value.has_directions(op_dir):
                should_have_directions.append(dir)
        return pipes.from_directions(should_have_directions)
        
def ParseField(str_field:str) -> Field:
    from nodes import Node

    lines = str_field.split('\n')
    y_len = len(lines)
    x_len = len(lines[0])
    
    has_outer = all(map(lambda c: c=='.', lines[0]))

    field = Field()
    for y in range(y_len):
        for x in range(x_len):
            p = pipes.parse_pipe(lines[y][x])
            n = Node(field, p, x, y)
            field.set(n)
    return field
        