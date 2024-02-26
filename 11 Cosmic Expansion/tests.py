import unittest
import prog
from prog import Map

unittest.TestLoader.sortTestMethodsUsing = None


def scenario1(): return \
'''
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''.strip()


def scenario2(): return [1, 3, 6, 10, 15, 21]
def scenario3(): return [10, 13, 16, 21, 30, 45]


    
class Tests(unittest.TestCase):
    def test_basics1(self):
        m = Map(scenario1())
        
        g5 = (1, 5)
        g8 = (0, 9)
        g9 = (4, 9)
        
        self.assertEqual(Map.GALAXY, m.get(g5))
        self.assertEqual(Map.GALAXY, m.get(g8))
        self.assertEqual(Map.GALAXY, m.get(g9))

        self.assertFalse(m.is_empty_horizonal(2))
        self.assertTrue(m.is_empty_horizonal(3))
        self.assertFalse(m.is_empty_vertical(1))
        self.assertTrue(m.is_empty_vertical(8))
        
        self.assertEqual(1, m.cost_horizontal[0])
        self.assertEqual(2, m.cost_horizontal[8])
        self.assertEqual(1, m.cost_vertical[0])
        self.assertEqual(2, m.cost_vertical[3])
        
        self.assertEqual(3, m.cost((0,0), (0,3)))
        self.assertEqual(3, m.cost((0,2), (0,4)))
   
        self.assertEqual(2, m.cost((3,0), (3,2)))
   
        self.assertEqual(4, m.cost((0,0), (2,2)))
        self.assertEqual(4, m.cost((0,0), (3,0)))
        self.assertEqual(5, m.cost((0,0), (0,4)))
        self.assertEqual(9, m.cost((0,0), (3,4)))
        
        pairs = m.get_galaxie_pairs()
        self.assertEqual(36, len(pairs))
        
        sum = m.sum_dist_pairs()
        self.assertEqual(374, sum)
        

if __name__ == '__main__':
    unittest.main()
    
