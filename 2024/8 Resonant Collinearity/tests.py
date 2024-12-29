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
..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
'''.strip()


class Tests(unittest.TestCase):


    def test0_basic(self):
        m = TextMap.parse_text(pattern1)   
        w = prog.Worker(m)

        a_ = w.by_freq['a']
        self.assertEqual(2, len(a_))

        h_ = w.by_freq['#']
        self.assertEqual(2, len(h_))

        (i1, i2) = prog.find_interference_nodes(a_[0], a_[1])
        self.assertIn(i1, h_)
        self.assertIn(i2, h_)

        

    def test1(self):
        m = TextMap.parse_text(
'''
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''.strip())


        w = prog.Worker(m)
        points = list(w.find_interference_point())
        self.assertEqual(14, len(points))

        # need_append = [m for m in measures if m not in matching1]
        # self.assertEqual(len(measures)-len(matching1), len(need_append))

        # w.clear([prog.AddOperator(), prog.MultiplicateOperator(), prog.ConcatenateOperator()])
        # matching2 = w.filter_of_matching(need_append) 
        # sum_3 = w.sum_results(matching2)
        # sum_2 = sum_1 + sum_3
        # self.assertEqual(11387, sum_2)
        pass


if __name__ == '__main__':
    unittest.main()
    
