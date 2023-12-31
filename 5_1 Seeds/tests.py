from mapping import Mapping
import unittest


class Tests(unittest.TestCase):

    def test_mappings(self):
        m = Mapping()
        m.add_mapping(50, 98, 2)
        
        self.assertEqual(49, m.lookup(49))
        self.assertEqual(98, m.lookup(50))
        self.assertEqual(99, m.lookup(51))
        self.assertEqual(52, m.lookup(52))
        

if __name__ == '__main__':
    unittest.main()
    
