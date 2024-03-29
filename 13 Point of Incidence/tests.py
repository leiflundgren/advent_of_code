import unittest
import prog
import tools
from prog import Matrix

pattern1 = \
'''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.'''.splitlines()

pattern2 = \
'''#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''.splitlines()

additional = \
'''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

.#.##.#.#
.##..##..
.#.##.#..
#......##
#......##
.#.##.#..
.##..##.#

#..#....#
###..##..
.##.#####
.##.#####
###..##..
#..#....#
#..##...#

#.##..##.
..#.##.#.
##..#...#
##...#..#
..#.##.#.
..##..##.
#.#.##.#.'''.splitlines()


    
class Tests(unittest.TestCase):
    def test_AllowSomeDifferenceEquals(self):
        eq = tools.AllowSomeDifferenceEquals(1)
        fnc = eq.equals_strings
        self.assertTrue(fnc("abc", "abc"))
        self.assertTrue(fnc("abc", "abd"))
        self.assertFalse(fnc("abc", "abd"))


    def test_dot1(self):
        for diffs in  [ 0, 1 ]:
            map1 = Matrix('map1', pattern1)
            print()
            print(map1)
            if diffs == 0:
                self.assertEqual([3], map1.find_equal_lines())
                self.assertEqual([], map1.find_mirrors(diffs))
        
            rot1 = map1.rotate()
            print()
            print(rot1)
        
            if diffs == 0:
                self.assertEqual([5], rot1.find_equal_lines())
                self.assertEqual([5], rot1.find_mirrors(diffs))

            sum1 = map1.sum_lines(diffs)
            if diffs == 0:
                self.assertEqual(5, sum1)
            else:
                self.assertEqual(300, sum1)


            map2 = Matrix('map2', pattern2)
            print()
            print(map2)
            if diffs == 0:
                self.assertEqual([4], map2.find_equal_lines())
                self.assertEqual([4], map2.find_mirrors(diffs))

            rot2 = map2.rotate()
            print()
            print(rot2)
            if diffs == 0:
                self.assertEqual([3, 7], rot2.find_equal_lines())
                self.assertEqual([], rot2.find_mirrors(diffs))
        
            sum2 = map2.sum_lines(diffs)
            if diffs == 0:
                self.assertEqual(400, sum2)
            else:
                self.assertEqual(100, sum2)
        pass
        
    def test_dot2(self):
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
        
    def test_additional(self):
        input_data = tools.split_list_on_empty_line(additional)
        
        sum_1 = 0; sum_2 = 0


        for (n, pattern) in zip(tools.natural_numbers(), input_data):
            m = Matrix(f'additional-{n}', pattern)
            
            rows = m.find_mirrors(1)
            columns = m.rotate().find_mirrors(1)


            s1 = m.sum_lines(0)
            s2 = m.sum_lines(1)
            print(f'{m.name}  dot1:{s1}  dot2:{s2}')
            if len(rows) + len(columns) != 1:
                print(f'Found rows {rows} cols{columns}')
            print(f'\norg\n{m}\nrotat\n{m.rotate()}\n')
            
            sum_1 += s1
            sum_2 += s2


        print(f'sum1:{sum_1}  sum2:{sum_2}')    ## sum1:19608  sum2:26180
        
        self.assertEqual(709, sum_1)
        self.assertEqual(1400, sum_2)
        

if __name__ == '__main__':
    unittest.main()
    
