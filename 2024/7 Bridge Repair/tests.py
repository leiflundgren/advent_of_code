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
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''.strip()


class Tests(unittest.TestCase):


    def test_basic(self):
        measures = prog.parse(pattern1)
        
        ab = ['a', 'b']
        abc = ['a', 'b', 'c']
#        c0 = prog.generate_combinations(ab, 0)
#        c1 = prog.generate_combinations(ab, 1)
        c2 = prog.generate_combinations(ab, 2)
        c3 = prog.generate_combinations(ab, 3)
        c4 = prog.generate_combinations(ab, 4)
        
        #self.assertEqual(0, c0);
        #self.assertEqual(2, c1);
        self.assertEqual(4, len(c2));
        self.assertEqual(8, len(c3));
        self.assertEqual(16, len(c4));

        self.assertEqual(190, prog.calculate_result([10, 19], [prog.MultiplicateOperator()]))
        self.assertEqual(292, prog.calculate_result([11, 6, 16, 20], [prog.AddOperator(), prog.MultiplicateOperator(), prog.AddOperator()]))


    def test1(self):
        measures = prog.parse(pattern1)

        w = prog.Worker([prog.AddOperator(), prog.MultiplicateOperator()])
        matching1 = w.filter_of_matching(measures)
        self.assertEqual(3, len(matching1))
        sum_1 = w.sum_results(matching1)
        self.assertEqual(3749, sum_1)

        need_append = [m for m in measures if m not in matching1]
        self.assertEqual(len(measures)-len(matching1), len(need_append))

        w.clear([prog.AddOperator(), prog.MultiplicateOperator(), prog.ConcatenateOperator()])
        matching2 = w.filter_of_matching(need_append) 
        sum_3 = w.sum_results(matching2)
        sum_2 = sum_1 + sum_3
        self.assertEqual(11387, sum_2)


if __name__ == '__main__':
    unittest.main()
    
