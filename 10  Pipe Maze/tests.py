import unittest
from prog import Field, find_loop, parse_pipe
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
        self.assertEqual(5, len(field.field))
        self.assertEqual(parse_pipe('7'), field.get(3, 1).value)
        n11 = field.get(1,1)
        self.assertTrue(n11.can_move_E())
        self.assertFalse(n11.can_move_W())
        self.assertFalse(n11.can_move_N())
        self.assertTrue(n11.can_move_S())
        
        self.assertEqual(25, len(field.all_nodes()))
        
        n = field.get_start_pos()
        self.assertEqual(None, n)
        
        loop = find_loop(n11)
        self.assertEqual(8, len(loop))
        self.assertEqual(n11, loop[0])
        self.assertEqual(field.get(3,3), loop[4])
        self.assertEqual(4, len(loop)/2)

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
        
if __name__ == '__main__':
    unittest.main()
    
