import unittest
import prog
import tools
from prog import Matrix
from directions import Direction

org1 = \
'''
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''.strip().splitlines()

north_tilt1 = \
'''
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
'''.strip().splitlines()



    
class Tests(unittest.TestCase):
    def test__rotate(self):
        org = m = Matrix("org1", org1, Direction.N)

        print(f'{m.name} dir:{m.dir} \n{m}\n')
        m = m.rotate()

        print(f'{m.name} dir:{m.dir} \n{m}\n')
        m = m.rotate()

        print(f'{m.name} dir:{m.dir} \n{m}\n')
        m = m.rotate()

        print(f'{m.name} dir:{m.dir} \n{m}\n')
        m = m.rotate()
        
        self.assertListEqual(org.data, m.data)

    def test_dot1(self):
        m = Matrix("org1", org1)
        print(f'calc {m.name} dir=N\n{m}\n')
        
        force_org1 = Matrix.calc_force(m, Direction.N)

        m = Matrix("north_tilt1", north_tilt1)
        force_north_tilt1 = Matrix.calc_force(m, Direction.N)


        self.assertEqual(104, force_org1)
        self.assertEqual(136, force_north_tilt1)
        

if __name__ == '__main__':
    unittest.main()
    
