from importlib.metadata import files
from typing import List
import unittest
from directions import Direction
from map import Map, Node, Point
import prog
from text_map import TextMap
import tools


#from colorama import Fore, Back, Style
#from termcolor import colored, cprint

import prog 

pattern1 = \
'2333133121414131402'


class Tests(unittest.TestCase):


    def test1(self):
        m = prog.FileSystem.parse('12345', False)
        mstr = m.disk_str()
        self.assertEqual('0..111....22222', mstr)
        m.compact_disk()
        mstr = m.disk_str()
        self.assertEqual('022111222......', mstr)


        
        m = prog.FileSystem.parse('2333133121414131402', False)
        mstr = m.disk_str()
        self.assertEqual('00...111...2...333.44.5555.6666.777.888899', mstr)

        m.compact_disk()

        self.assertEqual('0099811188827773336446555566..............', m.disk_str())

        self.assertEqual(1928, m.calc_checksum())

    def test2(self):

        m = prog.FileSystem.parse('2333133121414131402', True)
        self.assertEqual('00...111...2...333.44.5555.6666.777.888899', m.block_str())

        m.compact_blocks()

        self.assertEqual('00992111777.44.333....5555.6666.....8888..', m.block_str())

        block_check = m.calc_checksum()
        # disk_check = prog.FileSystem.parse(m.block_str(), False).calc_checksum()
        self.assertEqual(2858, block_check)


if __name__ == '__main__':
    unittest.main()
    
