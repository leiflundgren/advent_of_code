import unittest
from mapping import Mapping
from seed_map import SeedMap

seeds = [ 79 ,14 ,55 ,13]

seed_to_soil = Mapping()
seed_to_soil.add_mapping( 50, 98, 2)
seed_to_soil.add_mapping( 52, 50, 48)

soil_to_fertilizer = Mapping() \
.add_mapping( 0, 15, 37)\
.add_mapping( 37, 52, 2)\
.add_mapping( 39, 0, 15)

fertilizer_to_water = Mapping() \
.add_mapping( 49, 53, 8) \
.add_mapping( 0, 11, 42) \
.add_mapping( 42, 0, 7) \
.add_mapping( 57, 7, 4) 

water_to_light = Mapping() \
.add_mapping( 88, 18, 7) \
.add_mapping( 18, 25, 70)

light_to_temperature = Mapping() \
.add_mapping( 45, 77, 23) \
.add_mapping( 81, 45, 19) \
.add_mapping( 68, 64, 13)

temperature_to_humidity = Mapping() \
.add_mapping( 0, 69, 1) \
.add_mapping( 1, 0, 69)

humidity_to_location = Mapping() \
.add_mapping( 60, 56, 37) \
.add_mapping( 56, 93, 4)

seed_map = SeedMap(seeds, seed_to_soil, soil_to_fertilizer,fertilizer_to_water,water_to_light,light_to_temperature,                temperature_to_humidity,humidity_to_location ) 


class Tests(unittest.TestCase):

    def test_mappings(self):
        m = Mapping()
        m.add_mapping(50, 98, 2)
        
        self.assertEqual(97, m.src_to_dst(97))
        self.assertEqual(50, m.src_to_dst(98))
        self.assertEqual(51, m.src_to_dst(99))
        self.assertEqual(100, m.src_to_dst(100))


        self.assertEqual(49, m.dst_to_src(49))
        self.assertEqual(98, m.dst_to_src(50))
        self.assertEqual(99, m.dst_to_src(51))
        self.assertEqual(52, m.dst_to_src(52))
        
    def test_seed_soil(self):
        self.assertEqual(81, seed_map.seed_to_soil(79))

    def test_seed_location_lookup(self):
        self.assertEqual(82, seed_map.seed_to_loc(79))
        self.assertEqual(43, seed_map.seed_to_loc(14))
        self.assertEqual(86, seed_map.seed_to_loc(55))
        self.assertEqual(35, seed_map.seed_to_loc(13))
        
    def test_seed_min_location(self):
        self.assertEqual(35, seed_map.seed_with_lowest_location())
        


if __name__ == '__main__':
    unittest.main()
    
