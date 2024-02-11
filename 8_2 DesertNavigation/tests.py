import unittest
import desert
import tools

unittest.TestLoader.sortTestMethodsUsing = None

def parse_scenario1():
    return desert.parse_scenario(iter(
"""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".splitlines()))        


# def parse_scenario2():
#     return desert.parse_scenario(iter(
# """LLR

# AAA = (BBB, BBB)
# BBB = (AAA, ZZZ)
# ZZZ = (ZZZ, ZZZ)
# """.splitlines()))        


    
class Tests(unittest.TestCase):
    def test__lcm(self)    :
        self.assertEqual(216, tools.lcm_list([54, 24]))
        self.assertEqual(403326, tools.lcm_list([54, 231, 97 ]))



    def test_basics1(self):
        sc = parse_scenario1()
        sc.print_next = True
        self.assertEqual('LR', sc.directions)
        self.assertEqual(8, len(sc.nodes))
        self.assertEqual( sc.pos,  sc.start_pos)
        self.assertEqual( [ sc.nodes['11A'], sc.nodes['22A'] ], sc.pos)
        
        # lengths = sc.find_loops()
        # print(f'loops: [ {lengths} ]')
        # lcm = tools.lcm_list(lengths)

        lengths = sc.find_loops(True)
        print(f'loops: {lengths}')
        lcm = tools.lcm_list(lengths)
        self.assertEqual(6, lcm)


        # steps = sc.walk_to_end()
        # self.assertEqual(6, steps)

    # def test_basics2(self):
    #     sc = parse_scenario2()
    #     self.assertEqual('LLR', sc.directions)
    #     self.assertEqual(3, len(sc.nodes))
    #     self.assertEqual('AAA', sc.pos.name)
    #     self.assertEqual('AAA', sc.start_pos.name)
    #     self.assertEqual('ZZZ', sc.end_pos.name)
    #     steps = sc.walk_to_end()
    #     self.assertEqual(6, steps)

if __name__ == '__main__':
    unittest.main()
    
