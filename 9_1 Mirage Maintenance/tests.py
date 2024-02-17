import unittest
import prog

unittest.TestLoader.sortTestMethodsUsing = None


def scenario1(): return [0, 3, 6, 9, 12, 15]
def scenario2(): return [1, 3, 6, 10, 15, 21]
def scenario3(): return [10, 13, 16, 21, 30, 45]


    
class Tests(unittest.TestCase):
    def test_basics1(self):
        sc1 = scenario1()

        d1 = prog.int_derivate(sc1)
        self.assertEqual([3,3,3,3,3], d1)

        d2 = prog.int_derivate(d1)
        self.assertEqual([0,0,0,0], d2)

        self.assertTrue(prog.all_zero(d2))

if __name__ == '__main__':
    unittest.main()
    
