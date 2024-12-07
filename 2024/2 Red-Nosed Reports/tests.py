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
    def test_dot1(self):

        expected_results = [True, False, False, False, False, True]

        levels_list = map(prog.parse_line, pattern1)

        for n, levels, expected in zip(tools.natural_numbers(), levels_list, expected_results):
            actual = prog.is_safe(levels)
            self.assertEqual(expected, actual, f'test {n}')

        pass
       
    def test_dot2(self):
        raise unittest.SkipTest()
        diffs = 1
        map1 = Matrix('map1', pattern1, 2)
        map2 = Matrix('map2', pattern2, 2)
        # print("map1 orginal")
        # print(map1)
        
#         diffs1 = map1.count_mirror_faults(3)

#         # map1.set(1,1, '.')
#         # print("map1 changed 1,1 to .")
#         # print(map1)
        
#         # diffs2 = map1.count_mirror_faults(3)

#         # self.assertEqual([3], map1.find_equal_lines())
#         # self.assertEqual([3], map1.find_mirrors(diffs))
        
#         # self.assertEqual(1, diffs1)
#         # self.assertEqual(0, diffs2)

#         # rot = map1.rotate()
#         # print()
#         # print(rot)
        
#         # self.assertEqual([5], rot.find_equal_lines())
#         # self.assertEqual([5], rot.find_mirrors(diffs))

#         sum1 = map1.sum_lines(False)
#         self.assertEqual(300, sum1)
# #        map1.set(1,1, '#')

        
#         print("map2 orginal")
#         print(map2)
#         map2.set(5,2, '#')
#         print("map2 changed 5,2 to #")
#         print(map2)
        
#         self.assertEqual([1, 4], map2.find_equal_lines())
#         self.assertEqual([1], map2.find_mirrors(diffs))
        
#         # rot = map2.rotate()
#         # print()
#         # print(rot)
        
#         # self.assertEqual([3,7], rot.find_equal_lines())
#         # self.assertEqual([], rot.find_mirrors(diffs))

#         sum1 = map2.sum_lines(False)
#         self.assertEqual(100, sum1)
#         map2.set(1,1, '#')




        expected_sum_ls = [300, 100]

        m : Matrix = None

        for (m, expected_sum) in zip([map1, map2], expected_sum_ls):
            print()
            print(m.name)
            print(m)
            print()
            print(m.rotate())
            
            max_sum = m.sum_lines(diffs)
            
            # (changed_x, changed_y) = (-1,-1)
            # all_lines = []

            # old_lines = set(m.find_mirror_lines())
            # print(f'{m.name} original lines {old_lines}')
            # print(m)
            
            # for x in range(1, 1+map1.get_width()):
            #     for y in range(1, 1+map1.get_height()):
                    

            #         v = m.get(x, y)
            #         m.set(x, y, 'X')
                    
            #         strm = str(m)
            #         m.set(x, y, '.' if v == '#' else '#')
                    
            #         found_lines = m.find_mirror_lines()
            #         m.set(x, y, v)
                    
            #         print(f'{m.name} changed {x},{y} from {v} found {found_lines}')
            #         print(strm)
                    
            #         if len(found_lines) == 0: continue

            #         new_lines = [x for x in found_lines if x not in old_lines]
                    
            #         if len(new_lines) == 0: 
            #             continue
            #         if len(new_lines) < len(old_lines):
            #             bp = 17

            #         #sum1 = m.sum_lines(False)
            #         sum1 = 100*sum(new_lines)

            #         if x==5 and y == 2:
            #             bp = 17
            #         if sum1 > 0:
            #             all_lines.append((sum1, x, y))
            #         if max_sum < sum1:
            #             max_sum = sum1
            #             (changed_x,changed_y) = (x,y)
                    

            # print(f'change ({changed_x},{changed_y}) from {m.get(changed_x, changed_y)} gave score {max_sum}')     
        
            self.assertEqual(expected_sum, max_sum)
   

if __name__ == '__main__':
    unittest.main()
    
