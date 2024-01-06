

import os

from pathlib import Path
from mapping import Mapping
from seed_map import SeedMap
import range

seeds = Mapping("seeds")

seed_to_soil = Mapping("seed_to_soil")
soil_to_fertilizer = Mapping("soil_to_fertilizer") 
fertilizer_to_water = Mapping("fertilizer_to_water") 
water_to_light = Mapping("water_to_light") 
light_to_temperature = Mapping("light_to_temperature") 
temperature_to_humidity = Mapping("temperature_to_humidity") 
humidity_to_location = Mapping("humidity_to_location") 




input = os.path.join(os.path.dirname(__file__), 'input.txt')
lines = Path(input).read_text().splitlines()

assert(lines[0].startswith('seeds:'))
for r in range.parse_seeds_from_str(lines[0][6:].strip()):
    seeds.add_mapping(r.num, r.num, r.len)
lines = lines[2:]

def lookup_mapping(name):
    if name == 'seed-to-soil': return seed_to_soil;
    if name == 'soil-to-fertilizer': return soil_to_fertilizer
    if name == 'fertilizer-to-water': return fertilizer_to_water
    if name == 'water-to-light': return water_to_light
    if name == 'light-to-temperature': return light_to_temperature
    if name == 'temperature-to-humidity': return temperature_to_humidity
    if name == 'humidity-to-location': return humidity_to_location
    raise ValueError('Unknown name ' + name)

m = Mapping()
for l in lines:
    if len(l) == 0:
        continue
    
    # seed-to-soil map:
    map = l.find('map:')
    if map > 0:
        name = l[0:map-1]
        m = lookup_mapping(name)
        continue
    
    # 1383244180 2567207479 366571891
    num = l.strip().split(' ')
    m.add_mapping(int(num[0]), int(num[1]), int(num[2]))


seed_map = SeedMap(seeds, seed_to_soil, soil_to_fertilizer,fertilizer_to_water,water_to_light,light_to_temperature,                temperature_to_humidity,humidity_to_location ) 

print('min loc:', seed_map.seed_with_lowest_location())    
