import unittest
import prog
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
    (prog.parse_springs('???.### 1,1,3'), 1),
    (prog.parse_springs('.??..??...?##. 1,1,3'), 4),
    (prog.parse_springs('?#?#?#?#?#?#?#? 1,3,1,6'), 1),
    (prog.parse_springs('????.#...#... 4,1,1'), 1),
    (prog.parse_springs('????.######..#####. 1,6,5'), 4),
    (prog.parse_springs('?###???????? 3,2,1'), 10),
]


    
class Tests(unittest.TestCase):
    def test_scenario1(self):
        (scen, solution) = scenario1()
        
        springs = prog.parse_springs(scen)
        self.assertEqual([3,2,1], springs.arrangement)
        self.assertEqual([('?', 1), ('#', 3), ('?', 8)], springs.springs)


    def test_scenario2(self):
        scenarios = scenario2()
        for (n, (springs, combinations)) in zip(range(len(scenarios)), scenarios):
            print(f'Reduce scen {n}')
            springs.reduce()

if __name__ == '__main__':
    unittest.main()
    
