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

    # def test_dot2(self):
    #     raise
    #     expected_results = [True, False, False, True, True, True]
    #     self.general(expected_results, prog.is_safe_if_remove_one)
        
    #     actual0 = prog.is_safe([1,3,2,4,5])
    #     actual1 = prog.is_safe_if_remove_one([1,3,2,4,5])
    #     actual2 = prog.is_safe([1,2,4,5])
    #     actual3 = prog.is_safe([1,3,4,5])
    #     self.assertEqual(False, actual0)
    #     self.assertEqual(True, actual1)
    #     self.assertEqual(True, actual2)
    #     self.assertEqual(True, actual3)

   

if __name__ == '__main__':
    unittest.main()
    
