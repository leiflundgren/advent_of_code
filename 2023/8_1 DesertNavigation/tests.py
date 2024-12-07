import unittest
import desert

unittest.TestLoader.sortTestMethodsUsing = None

def parse_scenario1():
    return desert.parse_scenario(iter(
"""RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""".splitlines()))        


def parse_scenario2():
    return desert.parse_scenario(iter(
"""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".splitlines()))        


    
class Tests(unittest.TestCase):
    def test_basics1(self):
        sc = parse_scenario1()
        self.assertEqual('RL', sc.directions)
        self.assertEqual(7, len(sc.nodes))
        self.assertEqual('AAA', sc.pos.name)
        self.assertEqual('AAA', sc.start_pos.name)
        self.assertEqual('ZZZ', sc.end_pos.name)
        steps = sc.walk_to_end()
        self.assertEqual(2, steps)

    def test_basics2(self):
        sc = parse_scenario2()
        self.assertEqual('LLR', sc.directions)
        self.assertEqual(3, len(sc.nodes))
        self.assertEqual('AAA', sc.pos.name)
        self.assertEqual('AAA', sc.start_pos.name)
        self.assertEqual('ZZZ', sc.end_pos.name)
        steps = sc.walk_to_end()
        self.assertEqual(6, steps)

if __name__ == '__main__':
    unittest.main()
    
