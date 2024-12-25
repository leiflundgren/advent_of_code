from typing import List
import unittest
from directions import Direction
from map import Map, Node, Point
import prog
from text_map import TextMap
import tools
#from colorama import Fore, Back, Style
#from termcolor import colored, cprint

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

def prRed(skk): print("\033[91m {}\033[00m" .format(skk), end='')
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk), end='')
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk), end='')
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk), end='')
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk), end='')
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk), end='')
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk), end='')
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk), end='')
    
class Tests(unittest.TestCase):
    def test_1(self):
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

    def test_2(self):

        m = TextMap.parse_text('''
M.S
.A.
M.S
''')
        self.assertTrue(prog.has_x_mas(m, 1, 1))
        self.assertFalse(prog.has_x_mas(m, 1, 0))

        m = TextMap.parse_text('''
M.S
.Y.
M.S
''')
        self.assertFalse(prog.has_x_mas(m, 1, 1))

        m = TextMap.parse_text(pattern1)
        self.assertTrue(prog.has_x_mas(m, 2, 1))
        self.assertFalse(prog.has_x_mas(m, 2, 2))

        x_es = prog.find_all_x_mas(m)
        

        print(x_es)

        for y in range(m.height()):
            for x in range(m.width()):
                pr = prRed if any( p == (x,y) for p in x_es) else prBlack
                pr(m.at(x, y) + ' ')
            print()

        self.assertEqual(9, len(x_es))


if __name__ == '__main__':
    unittest.main()
    
