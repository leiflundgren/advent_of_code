import unittest
from prog import Field, parse_pipe
from prog import ParseField

unittest.TestLoader.sortTestMethodsUsing = None


def scenario1(): return \
'''.....
.F-7.
.|.|.
.L-J.
.....'''

def scenario2(): return [1, 3, 6, 10, 15, 21]
def scenario3(): return [10, 13, 16, 21, 30, 45]


    
class Tests(unittest.TestCase):
    def test_basics(self):
        pass

    def test_scenario1(self):
        scenario = scenario1()
        field = ParseField(scenario)
        print(str(field))
        self.assertEqual(5, len(field.field))
        self.assertEqual(parse_pipe('7'), field.get(3, 1).value)

if __name__ == '__main__':
    unittest.main()
    
