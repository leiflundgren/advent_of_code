from collections import deque
from operator import contains

import directions
import fields
import nodes
import pipes

from directions import Direction
from fields import Field
from nodes import  Node
from pipes import  Pipe

def clear_non_loop(orig:Field, loop:list[Node]) -> Field:
    field = Field()    
    for n in loop:
        field.set(n.copy(field))
    return field

def find_loop(start:Node) -> list[Node]:
    assert isinstance(start, Node)
    Node.clear_tags(start.field.all_nodes_unsorted())
    
    loop = []
    n = start
    while True:
        loop.append(n)
        n.tag = True
        neighbors = n.coonnected_neighbors()
        # nexts = list(filter(lambda n: not n.tag, neighbors))
        
        next_node = next(filter(lambda n: not n.tag, neighbors), None)
        if next_node is None:
            if contains(neighbors, start): # has looped
                break
            raise ValueError('Could not move away from node ', n)
        n = next_node
        
    return loop
        
def find_edge_nodes(field:Field, margin:int = 0) -> list[Node]:    
    edge = []
    ((min_x, min_y), (max_x,max_y)) = field.get_bounds()
    

    for x in range(min_x-margin, max_x+margin, +1):
        edge.append(field.get(x, min_y-margin))
    for y in range(min_y-margin, max_y+margin, +1):
        edge.append(field.get(max_x+margin, y))
    for x in range(max_x+margin, min_x-margin, -1):
        edge.append(field.get(x, max_y+margin))
    for y in range(max_y+margin, min_y-margin, -1):
        edge.append(field.get(min_x-margin, y))
    return edge      



def mark_outside_inside(field:Field) -> Field:
    
    l0 = len(field.field)
    field.fill_empty()
    for n in field.all_nodes_unsorted():
        n.tag = []
    l1 = len(field.field)
    
    edge : list[Node] = []
    outside : list[Node] = []
    ((x_min, y_min), (x_max, y_max)) = field.get_bounds()
    for x in range(x_min, 1+x_max):
        edge.append(field.get(x, y_min, True, True))
        edge.append(field.get(x, y_max, True, True))
    for y in range(y_min, 1+y_max):
        edge.append(field.get(x_min, y, True, True))
        edge.append(field.get(x_max, y, True, True))

    for n in edge:
        if n.value == pipes.PIPE_NO_PIPE:
            n.value = pipes.PIPE_OUTSIDE
            n.tag = ['outside']
            outside.append(n)

    print('trivil outside marked:')
    print(field)
    
    nodes = deque(outside)
    
    while len(nodes) > 0:
        n = nodes.pop()

        nexts = n.move_nopipe_one()
        for nn in nexts:
            if contains(nn.tag, 'outside'): continue # been here before
            if contains(nn.tag, 'move'): continue # been here before
            nn.tag.append('move')
            
            nn.tag.append('outside')
            if nn.value == pipes.PIPE_NO_PIPE:
                nn.value = pipes.PIPE_OUTSIDE
            nodes.append(nn)

        # can_sneak_to = n.sneak_one()
        # for nn in can_sneak_to:
        #     if 2 <= nn.x and nn.x <= 3 and nn.y == 6:
        #         bp = 17
                
        #     if nn.tag is None: nn.tag  = []
        #     if contains(nn.tag, 'outside'): continue # been here before
        #     if contains(nn.tag, 'sneak'): continue # been here before
        #     nn.tag.append('move')
            
        #     nn.tag.append('outside')

        #     if nn.value == pipes.PIPE_NO_PIPE:
        #         nn.value = pipes.PIPE_OUTSIDE
        #     nodes.append(nn)


    print('filled outside marked:')
    print(field)
    
    for n in field.all_nodes_unsorted():
        if n.value == pipes.PIPE_NO_PIPE:
            nn.tag.append('inside')
            n.value = pipes.PIPE_INSIDE
    
    return field

def count_inside(field:Field) -> int:
    return len(list(filter(lambda n: n.value == pipes.PIPE_INSIDE, field.all_nodes_unsorted())))

def tranform_up3(field:Field) -> Field:
    def transform_node(n:Node, target:Field) -> list[Node]:
        x = 3*n.x
        y = 3*n.y
        nodes = []
        if n.value is pipes.PIPE_VERTICAL:
             nodes = [ 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+0), Node(None, pipes.PIPE_VERTICAL, x+1, y+0), Node(None, pipes.PIPE_NO_PIPE, x+2, y+0), 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+1), Node(None, pipes.PIPE_VERTICAL, x+1, y+1), Node(None, pipes.PIPE_NO_PIPE, x+2, y+1), 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+2), Node(None, pipes.PIPE_VERTICAL, x+1, y+2), Node(None, pipes.PIPE_NO_PIPE, x+2, y+2), 
             ]
             
        elif n.value is pipes.PIPE_HORIZONTAL:
             nodes = [ 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+0), Node(None, pipes.PIPE_NO_PIPE, x+1, y+0), Node(None, pipes.PIPE_NO_PIPE, x+2, y+0), 
                 Node(None, pipes.PIPE_HORIZONTAL, x+0, y+1), Node(None, pipes.PIPE_HORIZONTAL, x+1, y+1), Node(None, pipes.PIPE_HORIZONTAL, x+2, y+1), 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+2), Node(None, pipes.PIPE_NO_PIPE, x+1, y+2), Node(None, pipes.PIPE_NO_PIPE, x+2, y+2), 
             ]
        elif n.value is pipes.PIPE_BEND_N_E:
              nodes = [ 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+0), Node(None, pipes.PIPE_VERTICAL, x+1, y+0), Node(None, pipes.PIPE_NO_PIPE, x+2, y+0), 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+1), Node(None, pipes.PIPE_BEND_N_E, x+1, y+1), Node(None, pipes.PIPE_HORIZONTAL, x+2, y+1), 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+2), Node(None, pipes.PIPE_NO_PIPE, x+1, y+2), Node(None, pipes.PIPE_NO_PIPE, x+2, y+2), 
             ]
        elif n.value is pipes.PIPE_BEND_N_W:
              nodes = [ 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+0), Node(None, pipes.PIPE_VERTICAL, x+1, y+0), Node(None, pipes.PIPE_NO_PIPE, x+2, y+0), 
                 Node(None, pipes.PIPE_HORIZONTAL, x+0, y+1), Node(None, pipes.PIPE_BEND_N_W, x+1, y+1), Node(None, pipes.PIPE_NO_PIPE, x+2, y+1), 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+2), Node(None, pipes.PIPE_NO_PIPE, x+1, y+2), Node(None, pipes.PIPE_NO_PIPE, x+2, y+2), 
             ]
        elif n.value is pipes.PIPE_BEND_S_W:
              nodes = [ 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+0), Node(None, pipes.PIPE_NO_PIPE, x+1, y+0), Node(None, pipes.PIPE_NO_PIPE, x+2, y+0), 
                 Node(None, pipes.PIPE_HORIZONTAL, x+0, y+1), Node(None, pipes.PIPE_BEND_S_W, x+1, y+1), Node(None, pipes.PIPE_NO_PIPE, x+2, y+1), 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+2), Node(None, pipes.PIPE_VERTICAL, x+1, y+2), Node(None, pipes.PIPE_NO_PIPE, x+2, y+2), 
             ]
        elif n.value is pipes.PIPE_BEND_S_E:
              nodes = [ 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+0), Node(None, pipes.PIPE_NO_PIPE, x+1, y+0), Node(None, pipes.PIPE_NO_PIPE, x+2, y+0), 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+1), Node(None, pipes.PIPE_BEND_S_E, x+1, y+1), Node(None, pipes.PIPE_HORIZONTAL, x+2, y+1), 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+2), Node(None, pipes.PIPE_VERTICAL, x+1, y+2), Node(None, pipes.PIPE_NO_PIPE, x+2, y+2), 
             ]
        elif n.value is pipes.PIPE_NO_PIPE:
              nodes = [ 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+0), Node(None, pipes.PIPE_NO_PIPE, x+1, y+0), Node(None, pipes.PIPE_NO_PIPE, x+2, y+0), 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+1), Node(None, pipes.PIPE_NO_PIPE, x+1, y+1), Node(None, pipes.PIPE_NO_PIPE, x+2, y+1), 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+2), Node(None, pipes.PIPE_NO_PIPE, x+1, y+2), Node(None, pipes.PIPE_NO_PIPE, x+2, y+2), 
             ]
        elif n.value is pipes.PIPE_START:
             nodes = [ 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+0), Node(None, pipes.PIPE_NO_PIPE, x+1, y+0), Node(None, pipes.PIPE_NO_PIPE, x+2, y+0), 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+1), Node(None, pipes.PIPE_NO_PIPE, x+1, y+1), Node(None, pipes.PIPE_NO_PIPE, x+2, y+1), 
                 Node(None, pipes.PIPE_NO_PIPE, x+0, y+2), Node(None, pipes.PIPE_NO_PIPE, x+1, y+2), Node(None, pipes.PIPE_NO_PIPE, x+2, y+2), 
             ]
        pass
 
        for n in nodes:
            old = target.get(n.x, n.y, False)
            if not old is None:
                bp = 17
            target.set(n)

    cpy = field.copy()
    start_node = cpy.get_start_pos()
    start_cpy = start_node.copy()
    start_cpy.value = field.find_start_pipe(start_node)
    cpy.set(start_cpy)

    scaled = Field()
    for n in cpy.all_nodes_unsorted():
        transform_node(n, scaled)

    scaled.set_bounds()
    scaled.get(1+3*start_cpy.x, 1+3*start_cpy.y).value = pipes.PIPE_START
    return scaled

def tranform_down3(field:Field) -> Field:
    def transform_node(n:Node) -> Node:
        x = n.x//3
        y = n.y//3
        return Node(None, n.value, x, y)
        
    scaled = Field()
    ((x_min, y_min), (x_max, y_max)) = field.get_bounds()
    for y in range(y_min+1, y_max, 3):
        for x in range(x_min+1, x_max, 3):
            # x,y is middle on a 9-set of nodes.
            scaled.set(transform_node(field.get(x, y)))
            
    return scaled
