from importlib.metadata import files
from pickle import OBJ
from directions import Direction
from point import Point, Vector
import tools
from enum import Enum
from typing import Any, Dict, Iterable, Iterator, List, Self, Sequence, Set, Tuple

class FileBlock(object):
    def __init__(self, id:int, size:int): 
        self.id : int = id
        self.size : int = size

    def is_empty(self) -> bool:
        return self.id < 0

    def __str__(self) -> str:
        return f'b{self.id} s={self.size}'

    def __repr__(self) -> str:
        return str(self)

class FileSystem(object):
    EMPTY = '.'

    
    def __init__(self, disk : List[int], blocks : List[FileBlock]):

        if not disk is None and not blocks is None:
            raise ValueError(f'Filesystem should be file-block or posision base. Not both')

        self.disk : List[int] = disk
        self.blocks : List[FileBlock] = blocks
        self.bigger_than_9 = False
        for x in self.disk if self.disk is not None else self.blocks:
            if FileSystem.id_of(x) > 9:
                bigger_than_9 = True
                break

    def __repr__(self) -> str:
        if self.disk is not None:
            return self.disk_str()
        else:
            return self.block_str()

    def id_of(x : Any) -> int:
            if isinstance(x , int):
                return x
            elif isinstance(x, FileBlock):
                return x.id
            else:
                raise ValueError(f'Only int and FileBlock allowed, got {x}')

    def __str__(self) -> str:
        return self.__repr__()

    def disk_to_str(disk : List[int], big_number:bool) -> str:
        def format(x) -> str:
            id = FileSystem.id_of(x)
            if id < 0: return FileSystem.EMPTY
            elif not big_number: return str(id)
            else: return f'({id}) '

        return ''.join(map(format, disk))
    def disk_str(self):
        return FileSystem.disk_to_str(self.disk, self.bigger_than_9)

    def block_to_str(blocks : List[FileBlock], big_number:bool) -> str:
        def format(x) -> str:
            id = FileSystem.id_of(x)
            if id < 0: return FileSystem.EMPTY
            elif not big_number: return str(id)
            else: return f'({id}) '

        return ''.join(map(lambda b : format(b.id)*b.size, blocks))


    def block_str(self):
        return FileSystem.block_to_str(self.blocks, self.bigger_than_9)

    def compact_disk(self) -> None:
        def find_last_used():
            for i in range(len(self.disk)-1, -1, -1):
                if self.disk[i] >= 0:
                    yield i
        first_free_it = tools.index_of(-1, self.disk)
        last_used_it = find_last_used()
        
        while True:
            first_empty = next(first_free_it, -1)
            if first_empty < 0:
                return # compact

            last_data = next(last_used_it, -1)
            if last_data < 0:
                return # no data, nothing to compact
            if last_data < first_empty:
                return # is compacted

            v = self.disk[last_data]
            self.disk[first_empty] = v
            self.disk[last_data] = -1

    def compact_blocks(self) -> None:
        def find_all_free() -> Iterator[int]:
            for (b, i) in zip(self.blocks, tools.natural_numbers()):
                if b.is_empty():
                    yield i
        def find_last_used(last:int):
            for i in range(last-1, -1, -1):
                if not self.blocks[i].is_empty():
                    return i
            return -1


        
        last_data = find_last_used(len(self.blocks))

        while True:
            if last_data < 0:
                return # no data, nothing to compact
            v = self.blocks[last_data]

            for idx in find_all_free():
                freeb = self.blocks[idx]
                if idx > last_data:
                    # cannot move last
                    break
                if freeb.size >= v.size:
                    self.blocks[idx] = v
                    self.blocks[last_data] = FileBlock(-1, v.size)
                    freeb.size -= v.size
                    if freeb.size > 0:
                        self.blocks.insert(idx+1, freeb)
                    break

            last_data = find_last_used(last_data)


    def calc_checksum(self) -> int:
        chk = 0
        n = 0
        if self.disk is not None:
            for (sid, n) in zip(self.disk, tools.natural_numbers()):
                if sid >= 0:
                    c = (sid * n)
                    chk += c                
        else:
            for b in self.blocks:
                    for _ in range(b.size):
                        if b.id >= 0:
                            c = (b.id * n)
                            chk += c                        
                        n += 1
        return chk

    @staticmethod
    def parse(line, parse_blocks : bool) -> Self:
        id = 0

        disk : List[int] = [] if not parse_blocks else None
        block : List[FileBlock] = [] if parse_blocks else None

        inside_file = True
        for ns in line:
            size = int(ns)
            if inside_file:
                pattern = id
                id += 1
            else:
                pattern = -1
            inside_file = not inside_file

            if parse_blocks:
                block.append(FileBlock(pattern, size))
            else:
                for _ in range(size):
                     disk.append(pattern)
            
        return FileSystem(disk, block)