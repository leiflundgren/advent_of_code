from operator import contains
import unittest
from prog import Field, clear_non_loop, find_edge_nodes, find_loop, mark_outside, parse_pipe
from prog import ParseField

unittest.TestLoader.sortTestMethodsUsing = None



    
class Tests(unittest.TestCase):
    def test_basics(self):
        pass

    # ·····
    # ·┎━┒·
    # ·┃·┃·
    # ·┖━┛·
    # ·····
    def test_scenario1(self):
        def scenario1(): return \
'''.....
.F-7.
.|.|.
.L-J.
.....'''
        scenario = scenario1()
        field = ParseField(scenario)
        print()
        print(str(field))
        self.assertEqual(parse_pipe('7'), field.get(3, 1).value)
        n11 = field.get(1,1)
        self.assertIsNotNone(n11.connect_E())
        self.assertIsNone(n11.connect_W())
        self.assertIsNone(n11.connect_N())
        self.assertIsNotNone(n11.connect_S())
        
        self.assertEqual(25, len(field.all_nodes()))
        
        n = field.get_start_pos()
        self.assertEqual(None, n)
                
        loop = find_loop(n11)
        self.assertEqual(8, len(loop))
        self.assertEqual(n11, loop[0])
        self.assertEqual(field.get(3,3), loop[4])
        self.assertEqual(4, len(loop)/2)

        ((min_x, min_y), (max_x,max_y)) = field.get_bounds()

        edge = find_edge_nodes(field)
        self.assertEqual(16, len(edge))
        self.assertTrue(contains(edge, field.get(min_x, min_y)))
        self.assertTrue(contains(edge, field.get(min_x, max_y)))
        self.assertTrue(contains(edge, field.get(max_x, min_y)))
        self.assertTrue(contains(edge, field.get(max_x, max_y)))
        
        between1 = field.nodes_between(field.get(1,1), field.get(1,4))
        self.assertEqual(2, len(between1))
        

    # ━┖┃┎┒
    # ┒S━┒┃
    # ┖┃┒┃┃
    # ━┖━┛┃
    # ┖┃━┛┎
    def test_scenario2(self):
        def scenario2(): return \
'''-L|F7
7S-7|
L|7||
-L-J|
L|-JF'''


        scenario = scenario2()
        field = ParseField(scenario)
        print(str(field))
        n = field.get_start_pos()
        ns = field.get(1,1)
        self.assertEqual(ns, n)
        
        loop = find_loop(n)        
        print('clear_non_loop')
        print(str(clear_non_loop(field, loop)))

        
    # ··┎┒·
    # ·┎┛┃·
    # S┛·┖┒
    # ┃┎━━┛
    # ┖┛···
    def test_scenario3(self):
        def scenario3(): return  \
'''..F7.
.FJ|.
SJ.L7
|F--J
LJ...'''
        scenario = scenario3()
        field = ParseField(scenario)
        print(str(field))
        


    def test_step2_1(self):
        def gen_scenario(): return \
'''
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
'''.strip()

        def gen_scen2(): return \
'''
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
'''.strip()

        for scenario in [ gen_scenario(), gen_scen2() ]:
            field = ParseField(scenario)
            print(str(field))
            n11 = field.get(1,1)
            n00 = field.get(0,0)
            n01 = field.get(0,1)
            n10 = field.get(1,0)
            
        
            n = field.get_start_pos()
            self.assertEqual(n11, n)

            loop = find_loop(n)
            
            move00 = n00.connect_one()
            self.assertEqual(0, len(move00))
            
            move11 = n11.connect_one()
            self.assertTrue(contains(move11, field.get(1, 2)))
            self.assertTrue(contains(move11, field.get(2, 1)))
            n40 = field.get(4, 0)
            n04 = field.get(0, 4)
            n44 = field.get(4, 4)
            self.assertTrue(field.path_between(n00, n40))
            self.assertTrue(field.path_between(n00, n04))

            # print('mark_outside')        
            # outside = mark_outside(field, loop)
            # print(str(outside))
        

if __name__ == '__main__':
    unittest.main()
    
