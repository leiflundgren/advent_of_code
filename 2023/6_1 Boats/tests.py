from math import exp
from os import access
from tkinter import SEL

import unittest

import race
unittest.TestLoader.sortTestMethodsUsing = None

def create_races():
    return race.Races() \
        .add_race(race.Race(7, 9)) \
        .add_race(race.Race(15, 40)) \
        .add_race(race.Race(30, 200))


# Function to print the matrix
def printMatrix(m):
    for line in m:
        for col in line:
            if isinstance(col, int):
                print('{:2d}'.format(col), end=' ')
            else:
                print(col, end=' ')
        print()


    
class Tests(unittest.TestCase):
    def test_1_race_1(self):
        race1 : race.Race = create_races().races[0]
        self.assertEqual(0, race1.calc_dist(0))
        self.assertEqual(6, race1.calc_dist(1))
        self.assertEqual(10, race1.calc_dist(2))
        self.assertEqual(12, race1.calc_dist(3))
        self.assertEqual(12, race1.calc_dist(4))
        self.assertEqual(10, race1.calc_dist(5))
        self.assertEqual(6, race1.calc_dist(6))
        self.assertEqual(0, race1.calc_dist(7))

    def test_2_find_all_records(self):
        best_1st = [3, 4] 
        ways_1st = 2
        ways_2nd = 8
        ways_3rd = 9
        
        races = create_races()

        best_loadtimes = []
        for r in races.races:
            best_loadtimes.append(r.find_loadtimes_better_than(r.mindist))
        
        len1 = len(best_loadtimes[0])
        len2 = len(best_loadtimes[1])
        len3 = len(best_loadtimes[2])
        
        self.assertEqual(4, len1)
        self.assertEqual(8, len2)
        self.assertEqual(9, len3)

        self.assertEqual(288, len1*len2*len3)


 
if __name__ == '__main__':
    unittest.main()
    
