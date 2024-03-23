import unittest
import prog
import tools
from prog import Springs
from list_on_list import ListOnList
from permutator import Permutor
from SimplerPermut import Perm2

unittest.TestLoader.sortTestMethodsUsing = None

def scenario1(): return \
('?###???????? 3,2,1', 
[
'.###.##.#...',
'.###.##..#..',
'.###.##...#.',
'.###.##....#',
'.###..##.#..',
'.###..##..#.',
'.###..##...#',
'.###...##.#.',
'.###...##..#',
'.###....##.#'])

def scenario2(): return [
#    ('???.### 1,1,3', 1),
#    ('.??..??...?##. 1,1,3', 4),
    ('?#?#?#?#?#?#?#? 1,3,1,6', 1),
    ('????.#...#... 4,1,1', 1),
    ('????.######..#####. 1,6,5', 4),
    ('?###???????? 3,2,1', 10),
]


    
class Tests(unittest.TestCase):
    def test_basics(self):
        self.assertEqual(-1, tools.ListIter.complement_index(0))
        self.assertEqual(0, tools.ListIter.complement_index(-1))
        self.assertEqual(-6, tools.ListIter.complement_index(5))
        self.assertEqual(5, tools.ListIter.complement_index(-6))

        ls = tools.ListIter([0,1,2,3,4,5])
        
        self.assertEqual(0, ls[0])
        self.assertEqual(5, ls[5])

        self.assertEqual(5, ls[-1])
        self.assertEqual(0, ls[-6])
        

    def test_list_on_list(self):
        ls5 = [0,1,2,3,4]
        lol5 = ListOnList(ls5)
        it1 = iter(ls5)
        it2 = iter(lol5)
        

        # zero = lol5[0]
        # four = lol5[4]

        # for i in ls5:
        #     pass
        for i in lol5:
            j = i

        self.assertEqual(0, next(it1))
        self.assertEqual(0, next(it2))
        self.assertEqual(1, next(it1))
        self.assertEqual(1, next(it2))
        self.assertEqual(2, next(it1))
        self.assertEqual(2, next(it2))
        self.assertEqual(3, next(it1))
        self.assertEqual(3, next(it2))
        self.assertEqual(4, next(it1))
        self.assertEqual(4, next(it2))
        

        # exceptions stops the debugger...

        # try:
        #     fem = lol5[5]
        # except IndexError:
        #     pass
        
        # with self.assertRaises(IndexError) as x:
        #     lol5[5]
        # self.assertRaises(StopIteration, lambda: next(it2))
        # self.assertRaises(StopIteration, lambda: next(it1))


        self.assertEqual([0,1,2,3,4], lol5)
        for i in range(5):
            self.assertEqual(i, lol5[i])
        self.assertEqual([1,2,3,4], lol5[1:])
        self.assertEqual([1,2,3,4], lol5[1:5])
        self.assertEqual([1,2,3,4], lol5[1:5:None])
        self.assertEqual([1,2,3,4], lol5[1:5:1])

        self.assertEqual([0,1,2,3], lol5[:-1])
        self.assertEqual([1,2], lol5[1:3])


    def test_ListIter(self):
        ls = tools.ListIter([0, 1,2,3,4])
        
        ls[1]
        ls_1 = ls[1:]
        

        self.assertEqual(0, ls[0])
        self.assertEqual(1, ls[1])
        self.assertEqual(1, ls[1:][0])



    # #def test_change_before_after_to(self):
    # #    unknowns = Springs([(Springs.UNKNOWN, 3)])


    def test_trivial_permutators(self):
        def gen(scen:str) -> Springs:
            return prog.parse_springs(scen)
        
        self.assertEqual(1, Perm2(False).calc_permutations(gen("## 2")))
        self.assertEqual(1, Perm2(False).calc_permutations(gen("?? 2")))
        self.assertEqual(2, Perm2(False).calc_permutations(gen("?? 1")))
        self.assertEqual(1, Perm2(False).calc_permutations(gen("?# 1")))
        self.assertEqual(1, Perm2(False).calc_permutations(gen("?#??# 3,1")))

    def test_scenario1(self):
        (scen, solution) = scenario1()
        
        springs = prog.parse_springs(scen)
        self.assertEqual([3,2,1], springs.arrangment)
        self.assertEqual([('?', 1), ('#', 3), ('?', 8)], springs.springs)

    # def test_scenario2(self):
    #     scenarios = scenario2()
    #     for (n, (str_springs, combinations)) in zip(range(len(scenarios)), scenarios):
    #         print(f'\nReduce scen {n}: {str_springs}  arr:{combinations}')
    #         springs = prog.parse_springs(str_springs)
    #         springs.reduce(n)

    #         # if  len(springs.springs) == 0 or len(springs.arrangment) == 0:
    #         #     self.assertEqual(1, combinations)

    #         perm = Permutor()
    #         c = perm.calc_permutations(springs)
            
    #         self.assertEqual(combinations, c)


    def test_scenario2_perm2(self):
        scenarios = scenario2()
        for (n, (str_springs, combinations)) in zip(range(len(scenarios)), scenarios):
            print(f'\Permutate scen {n}: {str_springs}  arr:{combinations}')
            springs = prog.parse_springs(str_springs)

            perm = Perm2(False)
            c = perm.calc_permutations(springs)
            
            self.assertEqual(combinations, c)

if __name__ == '__main__':
    unittest.main()
    
