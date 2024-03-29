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

    def assertMatrixEquals(self, m1:Matrix, m2:Matrix):
        # self.assertEqual(m1.name, m2.name)
        self.assertEqual(m1.dir, m2.dir)
        self.assertEqual(m1.get_height(), m2.get_height())
        self.assertEqual(m1.get_width(), m2.get_width())
        for (x,y) in m1.get_points():
            self.assertEqual(m1.get(x,y), m2.get(x,y), f'Differ at [{x},{y}] {m1.get(x,y)} != {m2.get(x,y)}')

    def test_dot1(self):
        m = Matrix("org1", org1)
        print(f'calc {m.name} dir=N\n{m}\n')
        
        force_org1 = Matrix.calc_force(m, Direction.N)

        mTiltN = Matrix("north_tilt1", north_tilt1)
        force_north_tilt1 = Matrix.calc_force(mTiltN, Direction.N)


        self.assertEqual(104, force_org1)
        self.assertEqual(136, force_north_tilt1)
        

        tilted = Matrix.tilt(m, Direction.N)
        print(f'tilt {tilted.name} dir={tilted.dir}\n{tilted}')
        
        self.assertMatrixEquals(mTiltN, tilted)

        

if __name__ == '__main__':
    unittest.main()
    
