from typing import List
import unittest
import prog
import tools

import prog 

pattern1 = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'


    
class Tests(unittest.TestCase):
       
    def test_dot1(self):
        expected_results = ['mul(2,4)','mul(5,5)', 'mul(11,8)', 'mul(8,5)']
        expected_results = [(2,4),(5,5),(11,8), (8,5)]
        actual = prog.parse_muls_pairs(pattern1)
        self.assertEqual(expected_results, actual, 'Test 3.1')

    def test_dot2(self):
        pattern1 = '''xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))'''
        # xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))

        expected_results = ['mul(2,4)','don\'t()', 'mul(5,5)', 'mul(11,8)', 'do()', 'mul(8,5)']
        actual = prog.parse_inputs(pattern1)
        print(actual)
        self.assertEqual(expected_results, actual, 'Test 3.2a')

        expected_results = ['mul(2,4)', 'mul(8,5)']
        actual = prog.filter_inputs(actual)
        print(actual)

        self.assertEqual(expected_results, actual, 'Test 3.2b')

        inputs = [ prog.parse_muls_pairs(inp)[0] for inp in actual ]
        print(inputs)

        actual_sum = prog.multiply_inputs(inputs)
        self.assertEqual(48, actual_sum)



   

if __name__ == '__main__':
    unittest.main()
    
