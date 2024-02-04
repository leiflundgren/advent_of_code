import unittest
import desert

unittest.TestLoader.sortTestMethodsUsing = None

def parse_scenario():
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


    
class Tests(unittest.TestCase):
    def test_basics(self):
        scenario = parse_scenario()
        self.assertEqual('RL', scenario.directions)
        self.assertEqual(7, len(scenario.nodes))


if __name__ == '__main__':
    unittest.main()
    
