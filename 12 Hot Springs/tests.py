from math import comb
import unittest
import prog
import tools
from prog import Springs

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
    ('???.### 1,1,3', 1),
    ('.??..??...?##. 1,1,3', 4),
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


    def test_scenario1(self):
        (scen, solution) = scenario1()
        
        springs = prog.parse_springs(scen)
        self.assertEqual([3,2,1], springs.arrangment)
        self.assertEqual([('?', 1), ('#', 3), ('?', 8)], springs.springs)


    def test_scenario2(self):
        scenarios = scenario2()
        for (n, (str_springs, combinations)) in zip(range(len(scenarios)), scenarios):
            print(f'\nReduce scen {n}: {str_springs}  arr:{combinations}')
            springs = prog.parse_springs(str_springs)
            springs.reduce()

            if  len(springs.springs) == 0 or len(springs.arrangment) == 0:
                self.assertEqual(1, combinations)

if __name__ == '__main__':
    unittest.main()
    
