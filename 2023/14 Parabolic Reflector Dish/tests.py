from math import e
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


After_1_cycle = \
'''
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....
'''.strip().splitlines()

After_2_cycles = \
'''
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O
'''.strip().splitlines()

After_3_cycles = \
'''
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
'''.strip().splitlines()
    
class Tests(unittest.TestCase):

    def test__rotate(self):
        print('==============\n test spinning')

        small = Matrix('small', '123\n456\n789'.splitlines())
        print(f'{small.name} dir={small.dir}\n{small}')

        small = small.rotate()
        print(f'{small.name} dir={small.dir}\n{small}')
        small = small.rotate()
        print(f'{small.name} dir={small.dir}\n{small}')
        small = small.rotate()
        print(f'{small.name} dir={small.dir}\n{small}')
        small = small.rotate()
        print(f'{small.name} dir={small.dir}\n{small}')

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

    def assertMatrixEquals(self, m1:Matrix, m2:Matrix, check_name=False, check_dir=True):
        if check_name:
            self.assertEqual(m1.name, m2.name)
        if check_dir:
            self.assertEqual(m1.dir, m2.dir)
        self.assertEqual(m1.get_height(), m2.get_height())
        self.assertEqual(m1.get_width(), m2.get_width())
        for (x,y) in m1.get_points():
            self.assertEqual(m1.get(x,y), m2.get(x,y), f'{m1.name},{m2.name} Differ at [{x},{y}] {m1.get(x,y)} != {m2.get(x,y)}')

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
        
        org_S = m = Matrix("south", org1).rotate().rotate()        
        tilted_S = Matrix.tilt(org_S, Direction.S)
        org_N = tilted_S.rotate().rotate()
        
        print(f'{org_N.name} dir={org_N.dir}\n{org_N}')
        
        self.assertMatrixEquals(mTiltN, mTiltN)
        



    def test_tilt_E(self):
        start = '''
.....#....
....#.O..#
...O.##...
O..#...O..
O.O....O#.
O.#..O.#.#
OO...#....
OO....O...
#O...###..
#O..O#..O.'''.strip().splitlines()

        expected_e = Matrix('expect_e',
'''
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....'''.strip().splitlines(),
Direction.S)
        


    def test_dot2(self):
        
        print('==============\n test spinning dot2')


        c0 = Matrix("org1", org1, Direction.N)
        print(f'calc {c0.name} dir={c0.dir}\n{c0}\n')

        m = c0
        for dir in [Direction.N,Direction.W,Direction.S,Direction.E]:
            m = Matrix.tilt(m, dir)        
            print(f'{m.name} tilt={dir} dir={m.dir}\n{m}\n')



        c1 = Matrix.spin_cycle(c0)
        c1.name = 'c1'
        print(f'calc {c1.name} dir={c1.dir}\n{c1}\n')
        self.assertMatrixEquals(Matrix('c1', After_1_cycle), c1, check_dir=False)
        
        c2 = Matrix.spin_cycle(c1)     
        c2.name = 'c2'
        print(f'calc {c2.name} dir={c2.dir}\n{c2}\n')
        self.assertMatrixEquals(Matrix('c2', After_2_cycles), c2, check_dir=False)
        
        c3 = Matrix.spin_cycle(c2)  
        c3.name = 'c3'
        print(f'calc {c3.name} dir={c3.dir}\n{c3}\n')
        self.assertMatrixEquals(Matrix('c3', After_3_cycles), c3, check_dir=False)

        i = 0
        cached = {}
        m2 = c0
        force_2 = -1
        m_last = None
        max_spins = 1000000000
        extra_spins = -1
        for i in range(max_spins):
        
            k1 = m2.hashstr()
            cnt = cached.get(k1)
            force_2 = Matrix.calc_force(m2, Direction.N, False)
            if cnt is None:
                print(f'force_2:{force_2} after {i} spin cycles ')    ## sum1:19608  sum2:26180
                cached[k1] = i
            elif extra_spins < 0:
                cycle = i-cnt
                print(f'force_2:{force_2} after {i} spin cycles (cycle detected, at {cnt} len={cycle})')    ## sum1:19608  sum2:26180                
                max_spins -= cnt
                extra_spins = max_spins % cycle   -1              
            elif extra_spins > 0:
                print(f'force_2:{force_2} after {i} spin cycles (need {extra_spins} more)')    ## sum1:19608  sum2:26180                
                extra_spins -= 1
            else: # extra_spins == 0:
                force_2 = Matrix.calc_force(m_last, Direction.N, False)
                print(f'force_2:{force_2} after {i} spin cycles (cnt={cnt}, diff={i-cnt})')    ## sum1:19608  sum2:26180                
                break


            m3 = Matrix.spin_cycle(m2, False)
        
            if m3 == m2:
                break
            m2 = m3
            m_last = m2
        
            print(f'\nstep {i}\n{m2}')
        
        print(f' force_2:{force_2} after {i} spin cycles (cnt={cnt}, diff={i-cnt})')    ## sum1:19608  sum2:26180
        self.assertEqual(64, force_2)
            

if __name__ == '__main__':
    unittest.main()
    
