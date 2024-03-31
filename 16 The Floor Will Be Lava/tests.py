import unittest
import prog
import tools
from hashmap import HashMap
from prog import Matrix
from directions import Direction
import color_print

small_input = '''
.|...╲....
|.⎯.╲.....
.....|⎯...
........|.
..........
.........╲
....╱.╲╲..
.⎯.⎯╱..|..
.|....⎯|.╲
..╱╱.|....
'''.strip().splitlines()




class Tests(unittest.TestCase):
    
    def test_color(self):
        color_print.prRed('is this red?')

    def test_trace_path(self):
        m = Matrix('small', small_input)
        
        print("plain")
        print(m.as_plain_text())
        print("\ncolor")
        print(m.as_color_text())

        path = m.trace_path((1,1), Direction.E)

        m.color_mark( map(lambda x_y_dir: x_y_dir[0], path), prog.color_Red)
        print("\npathh")
        print(m.as_color_text())
        
        uniq = Matrix.path_to_points(path)
                
        self.assertEqual(46, len(uniq))
        

if __name__ == '__main__':

    unittest.main()
    
