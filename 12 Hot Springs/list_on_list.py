    
from abc import abstractmethod
from collections import UserList
from collections.abc import Iterator
from email.policy import strict
from typing import Self, TypeVar, Sequence, overload, Generic
T = TypeVar('T')

class ListOnList(Generic[T]):
    def __init__(self, inner : list = [], begin :int = 0, end:int = -1, is_reversed : bool = False):
        self.inner = inner
        self.begin = begin
        self.end = end if end >= 0 else len(inner)
        self.is_reversed = is_reversed
        
    def __str__(self) -> str:
        return str(self.inner)

    def __repr__(self) -> str:
        return f'ListOnList: {self.inner} {"reversed" if self.is_reversed else ""}'

    def __len__(self) -> int:
        return self.end - self.begin
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, ListOnList):
            if not (self.is_reversed == other.is_reversed and len(self) == len(other)):
                return False
          
        for (s, o) in zip(self, other, strict=True):
            if s != o:
                return False
        
        return True
    
    def __hash__(self) -> int:
        h = 0
        for x in self:
            h = 31*h + (0 if h is None else h.hash() )
        return h
    
    def is_empty(self) -> bool:
        return 0 == len(self)
    def not_empty(self) -> bool:
        return not self.is_empty()
    
    @staticmethod
    def complement_index(idx:int) -> int:
        return -1 * idx -1
    def true_index(self, idx:int) -> int:
        if self.is_reversed:
            idx = ListOnList.complement_index(idx)
        return self.begin + idx


    def __getitem__(self, a1, a2=None, a3=None) -> T:
        start: int
        stop: int
        step: int

        if isinstance(a1, slice):
            (start, stop, step) = int.indices(len(self))
            return self.__getitem__(start, stop, step)
        elif isinstance(a1, int):
            start = a1
            stop = start+1 if a2 is None else a2
            if a3 is None or a3 == 1:
                step = 1
            elif a3 == -1:
                step = -1
            else:
                raise ValueError(f'step must be on of None, 1, -1. Got {a3}')
        
            if start >= len(self):
                raise StopIteration
            elif start + step == stop:
                return self.inner[self.true_index(start)]
            else:
                return ListOnList(self.inner, self.true_index(start), self.true_index(stop), self.is_reversed)
        elif isinstance(int, tuple):
            raise NotImplementedError('Tuple as index')
        else:
            raise TypeError('Invalid argument type: {}'.format(type(a1)))

    def __setitem__(self, idx: int, t:T) -> None:
        raise RuntimeError('ListOnList is const')



    def front(self) -> T:
        return self[0]

    @staticmethod
    def complement_index(idx:int) -> int:
        return -1 * idx -1

    def pop(self, idx:int = 0) -> T:
        if idx == 0:
            self.begin = self.begin+1
            return self.inner[self.begin-1]
        # last
        elif idx == -1 or idx+self.begin == self.end - 1:
            self.end = self.end - 1
            return self.inner[self.end]
        else:
            raise RuntimeError('ListOnList only allow delete from front/back')


    def remove(self, x) -> None:
        self.pop(x)

    # return first index matching condition
    def index_cond(self, cond) -> int:
        for i in range(len(self)):
            if cond(self[i]):
                return i
        return -1
    # return first item matching condition
    def find_cond(self, cond) -> T:
        idx = self.index_cond(cond)
        return self[idx] if idx >= 0 else None
    
    def insert(self, idx:int, t:T) -> None:
        raise RuntimeError('ListOnList is const')

    def index(self, t:T) -> int:
        for i in range(len(self)):
            if self[i] == t:
                return i
        return -1

    def get_reversed(self) -> Self:
        l =  len(self.inner)
        return ListOnList(self.inner, l - self.begin, l - self.end, not self.is_reversed)

    def sublist(self, begin:int, end:int) -> Self[T]:
        end = end if end >= 0 else len(self)-1 + end
        return ListOnList(self.begin+begin, self.end-end)

def infinite_iterator(base_src):
    while True:
        for x in base_src:
            yield x
            