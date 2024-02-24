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
        field.set(n.x, n.y, n.copy(field))
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



def mark_outside(field:Field, loop:list[Node]) -> Field:
    field = clear_non_loop(field, loop)
   
    edge = find_edge_nodes(field, 1)
    for n in field.all_nodes_unsorted():
        n.tag = None
    
    nodes = deque(edge)
    while len(nodes) > 0:
        n = nodes.pop()
        if n.value == pipes.PIPE_NO_PIPE:
            n.value = pipes.PIPE_OUTSIDE
            n.tag = ['outside']
            field.set(n.x, n.y, n)
    
    no_pipes = deque(filter(lambda n: n.value == pipes.PIPE_NO_PIPE, field.all_nodes_unsorted()))
    
    field.fill_empty()

    nodes = deque(edge)
    
    while len(nodes) > 0:
        n = nodes.pop()

        nexts = n.move_nopipe_one()
        for nn in nexts:            
            if nn.tag is None: nn.tag  = []
            if contains(nn.tag, 'outside'): continue # been here before
            if contains(nn.tag, 'move'): continue # been here before
            nn.tag.append('move')
            
            nn.tag.append('outside')
            if nn.value == pipes.PIPE_NO_PIPE:
                nn.value = pipes.PIPE_OUTSIDE
            nodes.append(nn)

        can_sneak_to = n.sneak_one()
        for nn in can_sneak_to:
            if 2 <= nn.x and nn.x <= 3 and nn.y == 6:
                bp = 17
                
            if nn.tag is None: nn.tag  = []
            if contains(nn.tag, 'outside'): continue # been here before
            if contains(nn.tag, 'sneak'): continue # been here before
            nn.tag.append('move')
            
            nn.tag.append('outside')

            if nn.value == pipes.PIPE_NO_PIPE:
                nn.value = pipes.PIPE_OUTSIDE
            nodes.append(nn)

    return field

