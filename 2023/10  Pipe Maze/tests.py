from operator import contains
import unittest
import prog 

import directions
import fields
import nodes
import pipes

from directions import Direction
from fields import Field
from nodes import  Node
from pipes import  Pipe

unittest.TestLoader.sortTestMethodsUsing = None

N=directions.N
NE=directions.NE
E=directions.E
SE=directions.SE
S=directions.S
SW=directions.SW
W=directions.W
NW=directions.NW


def gen_scenario(): return ('scen1', \
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
'''.strip())

def gen_scen2(): return ('scen2', \
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
'''.strip())

def gen_scen3(): return ('scen3', \
'''
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
'''.strip())


    
class Tests(unittest.TestCase):
    def test_basics(self):
        self.assertEqual(E, E.rotate(90).rotate(90).rotate(90).rotate(90).dir)

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
        field = fields.ParseField(scenario)
        print()
        print(str(field))
        self.assertEqual(pipes.parse_pipe('7'), field.get(3, 1).value)
        n11 = field.get(1,1)
        self.assertIsNotNone(n11.connect(E))
        self.assertIsNone(n11.connect(W))
        self.assertIsNone(n11.connect(N))
        self.assertIsNotNone(n11.connect(S))
        
        self.assertEqual(25, len(field.all_nodes_unsorted()))
        
        n = field.get_start_pos()
        self.assertEqual(None, n)
                
        loop = prog.find_loop(n11)
        self.assertEqual(8, len(loop))
        self.assertEqual(n11, loop[0])
        self.assertEqual(field.get(3,3), loop[4])
        self.assertEqual(4, len(loop)/2)

        ((min_x, min_y), (max_x,max_y)) = field.get_bounds()

        edge = prog.find_edge_nodes(field)
        self.assertEqual(16, len(edge))
        self.assertTrue(contains(edge, field.get(min_x, min_y)))
        self.assertTrue(contains(edge, field.get(min_x, max_y)))
        self.assertTrue(contains(edge, field.get(max_x, min_y)))
        self.assertTrue(contains(edge, field.get(max_x, max_y)))
        
        between1 = field.nodes_between(field.get(1,1), field.get(1,4))
        self.assertEqual(2, len(between1))
        
        self.assertEqual(pipes.PIPE_VERTICAL, pipes.from_directions([N, S]))
        self.assertEqual(pipes.PIPE_BEND_N_E, pipes.from_directions([N, E]))


    def test_scale_basics(self):
        field = fields.ParseField(gen_scen2()[1])
        
        print('Test scale:')
        print(field)

        up = prog.tranform_up3(field)
        print(up)


        back = prog.tranform_down3(up)
        print(back)


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
        field = fields.ParseField(scenario)
        print(str(field))
        n = field.get_start_pos()
        ns = field.get(1,1)
        self.assertEqual(ns, n)
        
        loop = prog.find_loop(n)        
        print('clear_non_loop')
        print(str(prog.clear_non_loop(field, loop)))

        
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
        field = fields.ParseField(scenario)
        print(str(field))
        




    def test_print_loops(self):
        nscen = 0
        for (name, scenario) in [ gen_scen3(), gen_scen2(), gen_scenario() ]:
            ++nscen
            field = fields.ParseField(scenario)
            print()
            print()
            print(f'{name}  bounds:{field.get_bounds()}')
            print(str(field))
            n11 = field.get(1,1)
            n00 = field.get(0,0)
            n01 = field.get(0,1)
            n10 = field.get(1,0)
            
        
            n = field.get_start_pos()
            #self.assertEqual(n11, n)

            loop = prog.find_loop(n)
            
            f2 = prog.clear_non_loop(field, loop)
            
            print()
            print()
            print(f'{name}  bounds: {f2.get_bounds()}')
            print(str(field))


        nscen = 0
        
    def test_detaiils_scen_1_2(self):

        for (name, scenario) in [ gen_scen2(), gen_scenario() ]:

            field = fields.ParseField(scenario)
            print()
            print()
            print(f'{name}  bounds:{field.get_bounds()}')
            print(str(field))
            n11 = field.get(1,1)
            n00 = field.get(0,0)
            n01 = field.get(0,1)
            n10 = field.get(1,0)

            move00 = n00.connect_one()
            self.assertEqual(0, len(move00))
            
            move11 = n11.connect_one()
            self.assertTrue(contains(move11, field.get(1, 2)))
            self.assertTrue(contains(move11, field.get(2, 1)))
            n40 = field.get(4, 0)
            n04 = field.get(0, 4)
            n44 = field.get(4, 4)
        #    self.assertTrue(field.path_between(n00, n40))
        #    self.assertTrue(field.path_between(n00, n04))
            
            n27 = field.get(2, 7)
            n25 = field.get(2, 5)
            n34 = field.get(3, 4)
            n43 = field.get(4, 3)
            n44 = field.get(4, 4)
            n45 = field.get(4, 5)
            n46 = field.get(4, 6)
            n47 = field.get(4, 7)
            n48 = field.get(4, 8)

            self.assertIsNone(n34.sneak(S, E))
            self.assertIsNone(n34.sneak(W, E))


            # if field.get(5, 6).value == PIPE_VERTICAL:
            #     self.assertEqual(n47, n48.sneak(N))
            #     self.assertEqual(n46, n47.sneak(N))
            #     self.assertEqual(n45, n46.sneak(N))
            #     self.assertEqual(None, n45.sneak(N))
            #     self.assertEqual(None, n44.sneak(N))
            #     self.assertEqual(None, n45.sneak(W))

            # self.assertTrue(field.canSneak(n48, n44))

            #self.assertIsNone(n27.sneak(N))
            #self.assertIsNone(n25.sneak(S))
            
            

            loop = prog.find_loop(field.get_start_pos())
            
            scaled = prog.tranform_up3(field)
            scaled_start = scaled.get_start_pos()
            self.assertIsNotNone(scaled_start)
            scaled_loop = prog.find_loop(scaled_start) 
            
            self.assertEqual(3*len(loop), len(scaled_loop))


            # edge = prog.find_edge_nodes(scaled, 0)

            print(f'{name} edges checked  bounds: {scaled.get_bounds()}')
            print(str(scaled))


            f2 = prog.mark_outside_inside(scaled, scaled_loop)
            print(f'{name}  bounds: {f2.get_bounds()}')
            print(str(f2))
            
            rescaled = prog.tranform_down3(f2)
            print(f'{name}-rescaled  bounds: {rescaled.get_bounds()}')
            print(str(rescaled))
            
            inside = prog.count_inside(rescaled)
            print(f'Inside count is: {inside}')

            # print('mark_outside_inside')        
            # outside = mark_outside_inside(field, loop)
            # print(str(outside))
        
    def test_mark_outside_inside_3(self):
        for (name, scenario) in [ gen_scen3() ]:


            field = fields.ParseField(scenario)
            print()
            print()
            print(f'{name}  bounds: {field.get_bounds()}')
            print(str(field))
            n11 = field.get(1,1)
            n00 = field.get(0,0)
            n01 = field.get(0,1)
            n10 = field.get(1,0)

         
            n40 = field.get(4, 0)
            n04 = field.get(0, 4)
            n44 = field.get(4, 4)
        #    self.assertTrue(field.path_between(n00, n40))
        #    self.assertTrue(field.path_between(n00, n04))
            
            n27 = field.get(2, 7)
            n25 = field.get(2, 5)
            n34 = field.get(3, 4)
            n43 = field.get(4, 3)
            n44 = field.get(4, 4)
            n45 = field.get(4, 5)
            n46 = field.get(4, 6)
            n47 = field.get(4, 7)
            n48 = field.get(4, 8)

                      
            loop = prog.find_loop(field.get_start_pos())
            f2 = prog.mark_outside_inside(field, loop)
            nodes = f2.all_nodes_sorted()
            print(f'{name}  bounds: {f2.get_bounds()}')
            print(str(f2))

            # print('mark_outside_inside')        
            # outside = mark_outside_inside(field, loop)
            # print(str(outside))
            
if __name__ == '__main__':
    unittest.main()
    
