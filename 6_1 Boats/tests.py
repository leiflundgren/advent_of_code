from math import exp
from os import access

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
    def test_race_1(self):
        race1 : race.Race = create_races().races[0]
        self.assertEqual(0, race1.calc_dist(0))
        self.assertEqual(6, race1.calc_dist(1))
        self.assertEqual(10, race1.calc_dist(2))
        self.assertEqual(12, race1.calc_dist(3))
        self.assertEqual(12, race1.calc_dist(4))
        self.assertEqual(10, race1.calc_dist(5))
        self.assertEqual(6, race1.calc_dist(6))
        self.assertEqual(0, race1.calc_dist(7))

if __name__ == '__main__':
    unittest.main()
    
