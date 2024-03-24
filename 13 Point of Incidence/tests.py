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
        print(map1)
        rot1 = map1.rotate()
        print()
        print(rot1)
        


        map2 = Matrix(pattern2)
        rot2 = map2.rotate()
        
if __name__ == '__main__':
    unittest.main()
    
