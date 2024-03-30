import unittest
import prog
import tools
from hashmap import HashMap

small_input = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

class Tests(unittest.TestCase):
    
    def test__simple_hash(self):
        tests = [
('rn=1', 30),
('cm-', 253),
('qp=3', 97),
('cm=2', 47),
('qp-', 14),
('pc=4', 180),
('ot=9', 9),
('ab=5', 197),
('pc-', 48),
('pc=6', 214),
('ot=7', 231),
        ]

        for (input, expected) in tests:
            h = prog.calc_hash(input)    
            self.assertEqual(expected, h)

    def test_parsing_dot1(self):
        h = prog.sum_hash_line(small_input)
        self.assertEqual(1320, h)
        
    def test_hashmap(self):
        operations = prog.split_input(small_input)
        hmap = HashMap()
        for op in operations:
            hmap.perform_operation(op)
            
        self.assertEqual([('rn', 1), ('cm', 2)], hmap.data[0])
        self.assertEqual([('ot', 7), ('ab', 5), ('pc', 6)], hmap.data[3])

        self.assertEqual(5, hmap.calc_focal_length_box(hmap.data[0]))
        self.assertEqual(28+40+72, 4*hmap.calc_focal_length_box(hmap.data[3]))
        self.assertEqual(145, hmap.calc_focal_length_total())

if __name__ == '__main__':

    unittest.main()
    
