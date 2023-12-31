from mapping import Mapping
import unittest


class Tests(unittest.TestCase):

    def test_mappings(self):
        m = Mapping()
        m.add_mapping(50, 98, 2)
        
        self.assertEqual(97, m.lookup_src(97))
        self.assertEqual(50, m.lookup_src(98))
        self.assertEqual(51, m.lookup_src(99))
        self.assertEqual(100, m.lookup_src(100))


        self.assertEqual(49, m.lookup_dst(49))
        self.assertEqual(98, m.lookup_dst(50))
        self.assertEqual(99, m.lookup_dst(51))
        self.assertEqual(52, m.lookup_dst(52))
        

if __name__ == '__main__':
    unittest.main()
    
