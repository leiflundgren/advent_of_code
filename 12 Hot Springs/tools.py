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
    
    def __getitem__(self, index: int) -> T:
        if index < len(self):
            return self.inner[index]
        else:
            raise StopIteration

    def front(self) -> T:
        return self.inner[-1 if self.is_reversed else 0]

    def pop(self) -> T:
        idx = -1 if self.is_reversed else 0
        inner = self.inner
        t = inner[idx]
        inner.pop(idx)
        return t

    def get_reversed(self) -> Self:
        return ListIter(self.inner, not self.is_reversed)

    def remove(self, x):
        self.inner.remove(x)


def infinite_iterator(base_src):
    while True:
        for x in base_src:
            yield x
            