from abc import abstractmethod
from collections import UserList
from typing import Self, TypeVar, Sequence, overload, Generic
T = TypeVar('T')

class ListIter(Generic[T]):
    def __init__(self, inner : list = [], is_reversed : bool = False):
        self.inner = inner
        self.is_reversed = is_reversed
        
    def __str__(self) -> str:
        return str(self.inner)

    def __repr__(self) -> str:
        return f'ListIter: {self.inner} {"reversed" if self.is_reversed else ""}'

    def __len__(self) -> int:
        return len(self.inner)
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, ListIter):
            return self.is_reversed == other.is_reversed and self.inner == other.inner
        else:
            return self.inner == other
        
    
    def is_empty(self) -> bool:
        return 0 == len(self)
    def not_empty(self) -> bool:
        return not self.is_empty()
    
    def __getitem__(self, idx: int) -> T:
        if self.is_reversed:
            idx = ListIter.complement_index(idx)
        
        if idx < len(self):
            return self.inner[idx]
        else:
            raise StopIteration

    def __setitem__(self, idx: int, t:T) -> None:
        if self.is_reversed:
            idx = ListIter.complement_index(idx)
        self.inner[idx] = t

    def front(self) -> T:
        return self[0]

    @staticmethod
    def complement_index(idx:int) -> int:
        return -1 * idx -1

    def pop(self, idx:int = 0) -> T:
        if self.is_reversed:
            idx = ListIter.complement_index(idx)
        inner = self.inner
        t = inner[idx]
        inner.pop(idx)
        return t

    def get_reversed(self) -> Self:
        return ListIter(self.inner, not self.is_reversed)

    def remove(self, x) -> None:
        self.inner.remove(x)

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
       if self.is_reversed:
            idx = ListIter.complement_index(idx)
       self.inner.insert(idx, t)

    def index(self, t:T) -> int:
        for i in range(len(self)):
            if self[i] == t:
                return i
        return -1

def infinite_iterator(base_src):
    while True:
        for x in base_src:
            yield x
            