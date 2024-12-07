from typing import List
import unittest
import prog
import tools

import prog 

pattern1 = \
'''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9'''.splitlines()


    
class Tests(unittest.TestCase):
    def general(self, max_faults : int, expected_results : List[bool]):

        levels_list = list(map(prog.parse_line, pattern1))

        for n, levels, expected in zip(tools.natural_numbers(), levels_list, expected_results):
            actual = prog.is_safe(levels, max_faults)
            errmsg = f'test {n},{max_faults}'
            self.assertEqual(expected, actual, errmsg)

        pass
       
    def test_dot1(self):
        expected_results = [True, False, False, False, False, True]
        self.general(0, expected_results)

    def test_dot2(self):
        expected_results = [True, False, False, True, True, True]
        self.general(1, expected_results)

   

if __name__ == '__main__':
    unittest.main()
    
