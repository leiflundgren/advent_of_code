
from collections import namedtuple
from typing import Self

class Mapping:
    def __init__(self):
        self.Mapping = namedtuple("Mapping", "dst src len")
        self.mappings = []
        
    def add_mapping(self, dest:int, source:int, len:int):
        self.mappings.append( self.Mapping(dest, source, len) )
        return self
    
    def find_src(self, src:int):
        for m in self.mappings:
            if m.src <= src and src < m.src+m.len:
                return m
        return None

    def find_dst(self, d:int):
        for m in self.mappings:
            if m.dst <= d and d < m.dst+m.len:
                return m
        return None
            
    def src_to_dst(self, n:int) -> int :
        m = self.find_src(n)
        if m is None:
            return n
        
        offset = n-m.src
        return m.dst+offset
    

    def dst_to_src(self, n:int) -> int :
        m = self.find_dst(n)
        if m is None:
            return n
        
        offset = n-m.dst
        return m.src+offset
    
    def source_values(self) -> list[int] :
        return list(map(lambda m: m.src, self.mappings))

    def dest_values(self) -> list[int] :
        return list(map( lambda m: m.dst, self.mappings))
            

    def split_at(self, point : int) -> Self:
        res = []
        for m in self.mappings:
            if m.src <= point and point < m.src + m.len:
                s0 = m.src
                d0 = m.dst
                s1 = point
                l0 = s1 - s0
                l1 = m.len - l0
                d1 = d0 + l0
                
                res.append( self.Mapping(d0, s0, l0) )
                res.append( self.Mapping(d1, s1, l1) )
            else:
                res.append(m)
        self.mappings = res
        
