from typing import List
import unittest
from directions import Direction
import prog
import tools
#from colorama import Fore, Back, Style
#from termcolor import colored, cprint

import prog 

pattern1 = \
'''
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''

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

    def test_basics(self):
        (orders, pjobs) = prog.parse(pattern1)

        self.assertEqual(21, len(orders))
        self.assertEqual(6, len(pjobs))

    def test1(self):
        (orders, pjobs) = prog.parse(pattern1)
        sc = prog.Scenario(orders, pjobs)

        correct_jobs = sc.jobs_in_correct_order()
        self.assertEqual(3, len(correct_jobs))

        sum_ = sum( j.middle_page() for j in correct_jobs)

        self.assertEqual(143, sum_)


if __name__ == '__main__':
    unittest.main()
    
