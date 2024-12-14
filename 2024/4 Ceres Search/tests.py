from typing import List
import unittest
from directions import Direction
from map import Map, Node, Point
import prog
import tools

import prog 

pattern1 = \
'''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX'''

PATTERN = "XMAS"
LEN = len(PATTERN)-1

    
class Tests(unittest.TestCase):
    def test_tools(self):
        n0 = Node(Point(1,1))

        self.assertEqual(1, n0.pos.x)
        self.assertEqual(1, n0.pos.y)
        self.assertEqual(Point(1,1), n0.pos)


        m = Map.create(10, 10)

        (mmin, mmax) = m.bounds

        self.assertEqual(mmin, (0,0))
        self.assertEqual(mmax, (9,9))

        n = m.get(Point(1,1))
        
        path = n.path(Direction.E, 0)
        self.assertEqual(1, len(path))
        self.assertEqual(Point(1,1), path[0].pos)

        path = n.path(Direction.E, 3)
        self.assertEqual(4, len(path))
        self.assertEqual(Point(1,1), path[0].pos)
        self.assertEqual(Point(4,1), path[-1].pos)

        m = prog.parse_map(pattern1)
        n = m.get(Point(0,0))
        all_paths = prog.get_all_paths_from(n, LEN)
        self.assertEqual(3, len(all_paths))
        
        
        n = m.get(Point(3,4))
        all_paths = prog.get_all_paths_from(n, LEN)
        self.assertEqual(8, len(all_paths))
        good_paths = prog.find_all_match(PATTERN, all_paths)
        self.assertEqual(0, len(good_paths))

        n = m.get(Point(6,4))
        all_paths = prog.get_all_paths_from(n, LEN)
        self.assertEqual(8, len(all_paths))
        good_paths = prog.find_all_match(PATTERN, all_paths)
        self.assertEqual(2, len(good_paths))
 
        sum = prog.count_all_matches_map(PATTERN, m)
        self.assertEqual(18, sum)

if __name__ == '__main__':
    unittest.main()
    
