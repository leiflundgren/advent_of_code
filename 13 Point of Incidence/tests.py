import unittest
import prog
import tools
from prog import Matrix

pattern1 = \
'''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.'''.splitlines()

pattern2 = \
'''#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''.splitlines()


    
class Tests(unittest.TestCase):
    def test_parse(self):
        map1 = Matrix(pattern1)
        print()
        print(map1)
        self.assertEqual([3], map1.find_equal_lines())
        self.assertEqual([], map1.find_mirrors())
        
        rot1 = map1.rotate()
        print()
        print(rot1)
        
        self.assertEqual([5], rot1.find_equal_lines())
        self.assertEqual([5], rot1.find_mirrors())

        sum1 = map1.sum_lines()
        self.assertEqual(5, sum1)


        map2 = Matrix(pattern2)
        print()
        print(map2)
        self.assertEqual([4], map2.find_equal_lines())
        self.assertEqual([4], map2.find_mirrors())

        rot2 = map2.rotate()
        print()
        print(rot2)
        self.assertEqual([3, 7], rot2.find_equal_lines())
        self.assertEqual([], rot2.find_mirrors())
        
        sum2 = map2.sum_lines()
        self.assertEqual(400, sum2)
        

        

if __name__ == '__main__':
    unittest.main()
    
