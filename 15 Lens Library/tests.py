import unittest
import prog
import tools

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

if __name__ == '__main__':
    unittest.main()
    
