from typing import List
import unittest
from directions import Direction
from map import Map, Node, Point
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
    def test_tools(self):
        n0 = Node(Point(1,1))

        self.assertEqual(1, n0.pos.x)
        self.assertEqual(1, n0.pos.y)
        self.assertEqual(Point(1,1), n0.pos)


        m = Map.create(10, 10)

        n = m.get(Point(1,1))
        
        path = n.path(Direction.E, 0)
        self.assertEqual(1, len(path))
        self.assertEqual(Point(1,1), path[0].pos)

        path = n.path(Direction.E, 3)
        self.assertEqual(4, len(path))
        self.assertEqual(Point(1,1), path[0].pos)
        self.assertEqual(Point(4,1), path[-1].pos)
   

if __name__ == '__main__':
    unittest.main()
    
