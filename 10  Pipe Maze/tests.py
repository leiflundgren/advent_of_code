import unittest
from prog import Field, parse_pipe
from prog import ParseField

unittest.TestLoader.sortTestMethodsUsing = None

# ·····
# ·┎━┒·
# ·┃·┃·
# ·┖━┛·
# ·····

def scenario1(): return \
'''.....
.F-7.
.|.|.
.L-J.
.....'''

# ━┖┃┎┒
# ┒S━┒┃
# ┖┃┒┃┃
# ━┖━┛┃
# ┖┃━┛┎
def scenario2(): return \
'''-L|F7
7S-7|
L|7||
-L-J|
L|-JF'''

# ··┎┒·
# ·┎┛┃·
# S┛·┖┒
# ┃┎━━┛
# ┖┛···
def scenario3(): return  \
'''..F7.
.FJ|.
SJ.L7
|F--J
LJ...'''


    
class Tests(unittest.TestCase):
    def test_basics(self):
        pass

    def test_scenario1(self):
        scenario = scenario1()
        field = ParseField(scenario)
        print(str(field))
        self.assertEqual(5, len(field.field))
        self.assertEqual(parse_pipe('7'), field.get(3, 1).value)

    def test_scenario2(self):
        scenario = scenario2()
        field = ParseField(scenario)
        print(str(field))
        
    def test_scenario3(self):
        scenario = scenario3()
        field = ParseField(scenario)
        print(str(field))
        
if __name__ == '__main__':
    unittest.main()
    
