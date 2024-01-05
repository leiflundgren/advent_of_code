from typing import cast
from range import Range
from mapping import Mapping

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
        

    def seed_to_soil(self, seed) -> int:
        return self.map_seed_to_soil.src_to_dst(seed)
    
    def seed_to_loc(self, seed) -> int:
        maps = [
            (self.map_seed_to_soil, 'map_seed_to_soil'),
            (self.map_soil_to_fertilizer, 'map_soil_to_fertilizer'),
            (self.map_fertilizer_to_water, 'map_fertilizer_to_water'),
            (self.map_water_to_light, 'map_water_to_light'),
            (self.map_light_to_temperature, 'map_light_to_temperature'),
            (self.map_temperature_to_humidity, 'map_temperature_to_humidity'),
            (self.map_humidity_to_location, 'map_humidity_to_location'),
        ]
        src = seed
        for (map, name) in maps:
            dst = map.src_to_dst(src)
            print(f"{name}[{src}] --> {dst}")
            src = dst
        
        return src
    

    def seed_with_lowest_location(self) -> int:
        min_seed = 0
        min_dist = 0x7fffffff

        for seed in self.all_seed_numbers():
            loc = self.seed_to_loc(seed)
            
            if loc < min_dist:
                min_seed = seed
                min_dist = loc
        
        return min_dist
    