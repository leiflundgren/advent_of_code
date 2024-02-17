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
        
        all_derivates = prog.create_derivates(sc1)
        self.assertEqual(3, len(all_derivates))
        
        p1 = prog.Predictor(scenario1())
        self.assertEqual(18, p1.next_el)
        self.assertEqual(-3, p1.prev_el)

        p2 = prog.Predictor(scenario2())
        self.assertEqual(28, p2.next_el)
        self.assertEqual(0, p2.prev_el)

        p3 = prog.Predictor(scenario3())
        self.assertEqual(68, p3.next_el)
        self.assertEqual(5, p3.prev_el)
        
        self.assertEqual(114, p1.next_el+p2.next_el+p3.next_el)
        self.assertEqual(2, p1.prev_el+p2.prev_el+p3.prev_el)

if __name__ == '__main__':
    unittest.main()
    
