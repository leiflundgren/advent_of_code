
from collections import namedtuple
from typing import Self

class Mapping:
    def __init__(self, name):
        self.name = name
        self.Mapping = namedtuple("Mapping", "dst src cnt")
        self.mappings = []
          
    def add_mapping(self, dest:int, source:int, cnt:int):
        def get_src(m : self.Mapping ) -> int:
            return m.src

        if cnt == 0: ##  dont add empty ranges
            return self

        assert(cnt > 0)
        
        if source == 0:
            for m in self.mappings:
                if m.src == 0:
                    bp = 17
                    

        self.mappings.append( self.Mapping(dest, source, cnt) )
        self.mappings.sort(key=get_src)
        return self
    

    def add_missing_holes(self):
        ## leave last as exception
        for i in range(0, len(self.mappings)-1):
            curr = self.mappings[i]
            

            nxt = self.mappings[i+1]
            
            end_curr = curr.src + curr.cnt
            missing_len = nxt.src - end_curr
            if missing_len > 0:
                self.add_mapping(end_curr, end_curr, missing_len)
        

    def dist_to_next_src(self, n:int):
        for m in self.mappings:
            if m.src > n:
                return m.src-n
        return None
        

    def find_src(self, src:int):
        for m in self.mappings:
            if m.src <= src and src < m.src+m.cnt:
                return m
        return None

    def find_dst(self, d:int):
        for m in self.mappings:
            if m.dst <= d and d < m.dst+m.cnt:
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
        splitted = False
        pre = self.str_ranges()
        if point == 0:
            bp = 17
        
        # m = self.find_src(point)
        # if not m is None:
        #     self.mappings.remove(m)

        for m in self.mappings:
            if point == m.src: 
                return #exists

        if point < self.mappings[0].src: # new minimum
            self.add_mapping(0, 0, point)
            self.add_mapping(point, point, self.mappings[0].src - point)
            return
            
        last = self.mappings[-1]
        if point > last.src + last.cnt: # new max
            s0 = last.src+last.cnt;
            d0 = last.src+last.cnt;
            l0 = point - s0
            self.add_mapping(s0, d0, l0)
            return


        for i in range(len(self.mappings)):
            
            m = self.mappings[i]

            if m.src > point:
                prev = self.mappings[i-1]

                s0 = prev.src+prev.cnt
                d0 = s0
                l0 = point - s0
                s1 = s0+l0
                d1 = s1
                l1 = m.src - point

                del self.mappings[i]
                self.add_mapping(d0, s0, l0)
                self.add_mapping(d1, s1, l1)
                splitted = True
                break
    
            # Use < to ignore if m already splits a src
            elif m.src < point and point < m.src + m.cnt:
                s0 = m.src
                d0 = m.dst
                l0 = point - m.src

                s1 = s0 + l0
                d1 = d0 + l0
                l1 = m.src + m.cnt - point

                del self.mappings[i]
                self.add_mapping(d0, s0, l0)
                self.add_mapping(d1, s1, l1)
                splitted = True
                break
        
        if splitted:
            print(f'\nSplitted {self.name} on {point}\n' + pre + "\n--------\n" + self.str_ranges())
        else:
            print(f'\nNot-Splitted {self.name}\n' + self.str_ranges())

        
    def __str__(self):
        return f'{self.name} map:\r\n' + self.str_ranges()

    def str_ranges(self):
        return '\n'.join( map(lambda t: f'{t.dst} {t.src} {t.cnt}', self.mappings))
    
    def translate_dst_to_src(self, lst):
        return list(map(lambda p: self.dst_to_src(p), lst))
    
    def points_within_some_range(self, points:list[int]) -> list[int]:
        return list(filter(lambda p: not self.find_src(p) is None, points))
    