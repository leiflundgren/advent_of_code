    
from abc import abstractmethod
from collections.abc import Iterator, Sequence
from email.policy import strict
from operator import xor
from typing import Self, TypeVar, overload, Generic

T = TypeVar('T')

class ListOnList(Sequence[T]):
    def __init__(self, inner : list = [], begin :int = 0, end:int = -1, is_reversed : bool = False):
        self.inner = inner
        self.begin = begin
        self.end = end if end >= 0 else len(inner)
        self.is_reversed = is_reversed
        
    def __str__(self) -> str:
        return str(self.inner[self.begin:self.end])

    def __repr__(self) -> str:
        return f'ListOnList: {self} {"reversed" if self.is_reversed else ""}'

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
    
    @overload
    def __getitem__(self, idx: int) -> T:
        ...
    @overload
    def __getitem__(self, index: slice) -> Sequence[T]:
        ...
        
    def __getitem__(self, a1, a2=None, a3=None) -> T:
        start: int
        stop: int
        step: int

        if isinstance(a1, slice):
            return self.__getitem__slice(a1)
        elif isinstance(a1, int):
            return self.__getitem__int(a1)
        elif isinstance(int, tuple):
            raise NotImplementedError('Tuple as index')
        else:
            raise TypeError('Invalid argument type: {}'.format(type(a1)))


    def __getitem__int(self, idx: int) -> T:
        if idx >= len(self):
            raise IndexError
        else:
            return self.get_index(idx)

    def get_index(self, idx:int) -> T:
         return self.inner[self.true_index(idx)]

    def __getitem__slice(self, index: slice) -> Sequence[T]:
        (start, stop, step) = index.indices(len(self))
        if not (step == 1 or step == -1):
            raise ValueError(f'step must be on of None, 1, -1. Got {step}')
        
        if start >= len(self):
            raise StopIteration
        else:
            start = self.true_index(start)
            stop = self.true_index(stop)
            is_reversed = xor(bool(step == -1), bool(self.is_reversed))
            return ListOnList(self.inner, start, stop, is_reversed)


    def __setitem__(self, idx: int, t:T) -> None:
        raise RuntimeError('ListOnList is const')

    def copy(self, start=None, stop=None):
        if self.is_reversed: raise NotImplemented("cannot copy a reverted list yet")
        return ListOnList(self.inner[start:stop])

    def __reversed__(self) -> Sequence[T]:
        return ListOnList(self.inner, self.start, self.stop, not self.is_reversed)

    def __iter__(self):
        def generator(ls : list[T], start:int, stop:int, is_reversed:bool):
            step = -1 if is_reversed else 1
            for i in range(start, stop, step):
                yield ls[i]
            return
        return generator(self.inner, self.begin, self.end, self.is_reversed)

    @staticmethod
    def complement_index(idx:int) -> int:
        return -1 * idx -1
    def true_index(self, idx:int) -> int:
        if self.is_reversed:
            idx = ListOnList.complement_index(idx)
        return self.begin + idx



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

    def slice_front(self):
        if len(self) <= 1:
            return ListOnList()
        else:
            return ListOnList(self.get_inner(), 1+self.begin)

    def remove(self, x) -> None:
        idx = self.index(x)
        if idx >= 0:
            self.pop(idx)

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

    # def index(self, t:T) -> int:
    #     for i in range(len(self)):
    #         if self[i] == t:
    #             return i
    #     return -1

    def get_reversed(self) -> Self:
        l =  len(self.inner)
        return ListOnList(self.inner, l - self.begin, l - self.end, not self.is_reversed)

    def sub(self, begin:int, end:int = None) -> Sequence[T]:
        return self[begin:end]
        # end = end if end >= 0 else len(self)-1 + end
        # return ListOnList(self.begin+begin, self.end-end)
    
    def get_inner(self) -> list[T]:
        if self.is_reversed:
            return self.inner[self.end-1:self.begin-1:-1]
        else:
            return self.inner

def infinite_iterator(base_src):
    while True:
        for x in base_src:
            yield x
            