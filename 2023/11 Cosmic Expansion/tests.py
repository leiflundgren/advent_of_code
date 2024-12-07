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
    (Springs('???.### 1,1,3'), 1),
    (Springs('.??..??...?##. 1,1,3'), 4),
    (Springs('?#?#?#?#?#?#?#? 1,3,1,6'), 1),
    (Springs('????.#...#... 4,1,1'), 1),
    (Springs('????.######..#####. 1,6,5'), 4),
    (Springs('?###???????? 3,2,1'), 10),
]

def scenario2(): return [1, 3, 6, 10, 15, 21]
def scenario3(): return [10, 13, 16, 21, 30, 45]


    
class Tests(unittest.TestCase):
    def test_scenario1(self):
        (scen, solution) = scenario1()
        
        self.assertEqual([3,2,1], scen.arrangement)
        self.assertEqual([('?', 1), ('#', 3), ('?', 8)], scen.springs)


    def test_scenario2(self):
        scenarios = scenario2()
        for (n, springs) in zip(range(len(scenarios)), scenarios):
            print(f'Reduce scen {n}')
            springs.reduce()

if __name__ == '__main__':
    unittest.main()
    
