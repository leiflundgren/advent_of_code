from typing import Dict, List, Set
import unittest
from directions import Direction
from map import Map, Node, Point
from prog import Path
import prog
from text_map import TextMap
import tools

pattern1 = \
'''
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''.strip()


class Tests(unittest.TestCase):


    def test_1(self):
        pattern0 = '''
0123
1234
8765
9876
'''
        m = TextMap.parse_text(pattern0)
        starts = prog.Path(m).find_start_pos()
        self.assertEqual(1, len(list(starts)))

        m = TextMap.parse_text(pattern1)
        starts = prog.Path(m).find_start_pos()
        self.assertEqual(9, len(list(starts)))

        sum = 0
        trailheads : Dict[Point, List[Point]]= {}
        
        scores = [5, 6, 5, 3, 1, 3, 5, 3, 5]
        path = prog.Path(m)
        for start in path.find_start_pos():
            paths = path.walk_path(start)

            endp : Set[Point] = set()
            for p in paths:
                endp.add(p[-1])

            score = len(endp)
            
            print(f'start:{start} score: {score}')
            # for p in paths:
            #     print(Path.to_string_map(m, p))
            
            sum += score
    
            self.assertIn(score, scores)
            scores.remove(score)

        self.assertEqual(36, sum)



if __name__ == '__main__':
    unittest.main()
    
