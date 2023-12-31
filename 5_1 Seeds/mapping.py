
from collections import namedtuple

class Mapping:
    def __init__(self):
        self.Mapping = namedtuple("Mapping", "dst src len")
        self.mappings = []
        
    def add_mapping(self, dest:int, source:int, len:int):
        self.mappings.append( self.Mapping(dest, source, len) )
    
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
            
    def lookup_src(self, n:int) -> int :
        m = self.find_src(n)
        if m is None:
            return n
        
        offset = n-m.src
        return m.dst+offset
    

    def lookup_dst(self, n:int) -> int :
        m = self.find_dst(n)
        if m is None:
            return n
        
        offset = n-m.dst
        return m.src+offset
    

        