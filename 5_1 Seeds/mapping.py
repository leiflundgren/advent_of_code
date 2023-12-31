

class Mapping:
    def __init__(self):
        self.mappings = []
        
    def add_mapping(self, source:int, target:int, len:int):
        self.mappings.append( (source, target, len))
    
    def find_mapping(self, src:int):
        for (s,t,l) in self.mappings:
            if s <= src and src < s+l:
                return (s,t,l)
        return None
            
    def lookup(self, n:int):
        r = self.find_mapping(n)
        if r is None:
            return n
        
        (src, target, len) = r
        offset = n-src
        return target+offset
    

    