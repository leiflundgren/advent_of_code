from typing import Self
from mapping import Mapping

class NodeWalker:
    def __init__(self, mapping:Mapping, nxt:Self):
        self.mapping = mapping
        self.pre : Self = None
        self.nxt : Self = nxt
        self.iter = iter(self.mapping.mappings)
        self.next()

    def next(self):
        self.current = next(self.iter)
        self.src = self.current.src
        self.dst = self.mapping.src_to_dst(self.src)

    def find_next_node(self) -> Self:
        if self.nxt is None:
            return self

        node = self.nxt.find_next_node()
        if self.dst < node.src:
            return self
        else:
            return node
        
    def translate_src_to_pre(self):
        if self.pre is None:
            return self.src
        else:
            return self.pre.mapping.dst_to_src(self.src)
