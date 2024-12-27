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
'''
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''.strip()

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
        m = TextMap.parse_text(pattern1)   
        v = prog.Guard.find_guard_pos(m)

        g = prog.Guard(v, m)
        g.walk_path()

        # def color_select(x: int, y:int, d:Direction) -> str:
        #     return prRed if Point(x,y) in g.history else prBlack

        #m.print(color_select)
        g.print_path(prBlack, prRed)

        cnt = g.count_unique_positions()
        self.assertEqual(41, cnt)

        #test 2

        mods = g.modify_path_to_create_loops()
        self.assertEqual(6, len(mods))

if __name__ == '__main__':
    unittest.main()
    
