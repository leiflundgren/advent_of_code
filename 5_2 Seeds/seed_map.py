from typing import Iterable, cast
from range import Range
from mapping import Mapping
from node_walker import NodeWalker

def namestr(obj, namespace = None):
    if namespace is None: namespace = globals()
    return [name for name in namespace if namespace[name] is obj]

class SeedMap:
    def __init__(self, 
                 seeds : Mapping, 
                 seed_to_soil : Mapping,
                soil_to_fertilizer : Mapping,
                fertilizer_to_water : Mapping,
                water_to_light : Mapping,
                light_to_temperature : Mapping,
                temperature_to_humidity : Mapping,
                humidity_to_location : Mapping ) :
      
        self.map_seeds = seeds
        self.map_seed_to_soil = seed_to_soil
        self.map_soil_to_fertilizer = soil_to_fertilizer
        self.map_fertilizer_to_water = fertilizer_to_water
        self.map_water_to_light = water_to_light
        self.map_light_to_temperature = light_to_temperature
        self.map_temperature_to_humidity = temperature_to_humidity
        self.map_humidity_to_location = humidity_to_location
        self.maps = [ self.map_seeds,             self.map_seed_to_soil,             self.map_soil_to_fertilizer,             self.map_fertilizer_to_water,             self.map_water_to_light,             self.map_light_to_temperature,             self.map_temperature_to_humidity,             self.map_humidity_to_location ]
        

    def seed_to_soil(self, seed) -> int:
        return self.map_seed_to_soil.src_to_dst(seed)
    
    def seed_to_loc(self, seed) -> int:
        src = seed
        for map in self.maps:
            dst = map.src_to_dst(src)
            # print(f"{name}[{src}] --> {dst}")
            src = dst
        
        return src
    

    def seed_with_lowest_location(self) -> int:
        min_dist = 0x7fffffff

        for m in self.map_seeds.mappings:
            loc0 = self.seed_to_loc(m.src)
            loc1 = self.seed_to_loc(m.src + m.len)
            
            if loc0 < min_dist or loc1 < min_dist:
                print(f'Range {m.src}--{m.src+m.len} gives {loc0}/{loc1} which is lower than {min_dist}')
                for s in range(loc0, loc1):
                    loc = self.seed_to_loc(s)
                    print(f'seed {s} --> loc {loc}')
                    if loc < min_dist:
                        min_dist = loc
        
        return min_dist
    
    def split_mappings(self):
        far: Mapping
        near: Mapping
        for i in range(len(self.maps)-1, 0, -1):
            far = self.maps[i]
            near = self.maps[i-1]
            far_name = far.name
            near_name = near.name
            
            for dst in far.source_values():
                src = near.dst_to_src(dst)
                near.split_at(src)
            
            pass
        self.dump_lengths()
        
    def dump_lengths(self):
        for m in self.maps:
            print(f'mapping {m.name} has {len(m.mappings)} parts')
            
    def create_walkers(self) -> NodeWalker :
        def recurse(it : Iterable[Mapping]) -> NodeWalker:
            try:
                mapping = next(it)
            except StopIteration:
                return None
            nxt = recurse(it)
            nw = NodeWalker(mapping, nxt)
            if not nxt is None:
                nxt.pre = nw
            return nw
        length = len(self.maps)
        return recurse(iter(self.maps))

    def create_debug_matrix(self, begin, end, headers):
        
        res = []
        if headers:
            res.append(list(map(lambda m: m.name , self.maps)))
        for i in range(begin, end):
            src = i
            line = []
            for m in self.maps:
                dst = m.src_to_dst(src)
                src = dst
                line.append(dst)
            res.append(line)
        return res

    def dist_to_next_change(self, n:int) -> int:
        min_dist = 0x7fffffff
        src = n
        for m in self.maps:
            
            dist = m.next_src(src)
            if dist is None: continue
            min_dist = min(min_dist, dist)
            
            dst = m.

        return min_dist
    
    def change_spots(self, start:int) -> list[int] :
        points = []
        p = start
        while True:
            p = self.next_change(p)
            if p == 0x7fffffff:
                break
            points.append(p)
        return points
        
