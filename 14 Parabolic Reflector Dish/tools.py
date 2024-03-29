from abc import abstractmethod
from collections import UserList
from typing import Iterable, Iterator, Self, TypeVar, Sequence, overload, Generic
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
        
    def __hash__(self) -> int:
        h = 0
        for x in self:
            h = 31*h + (0 if h is None else h.hash() )
        return h
    
    def is_empty(self) -> bool:
        return 0 == len(self)
    def not_empty(self) -> bool:
        return not self.is_empty()
    
    def __iter__(self):
        def generator(ls : list[T]):
            for i in range(len(ls)):
                yield ls[i]
            return
        return generator(self)


    def __getitem__(self, a1, a2=None, a3=None, is_slice:bool=False) -> T:
        start: int
        stop: int
        step: int

        if isinstance(a1, slice):
            # (start, stop, step) = a1.indices(len(self))
            # return self.__getitem__(start, stop, step)
            return self.__getitem__(a1.start, a1.stop, a1.step, True)
        elif isinstance(a1, int):
            start = a1
            stop = a2
            step = a3
            
            
            if self.is_reversed:
                start = ListIter.complement_index(start)
                stop = ListIter.complement_index(stop)
                step = None if step is None else -step
            
            if not is_slice: # single
                l = len(self)
#                if start > 0 and l == 1:
                if start >= l:
                    raise StopIteration
                else:
                    return self.inner[start]

            if start == stop:
                return ListIter([])        
            else:
                return ListIter(self.inner[start:stop:step])
        
        elif isinstance(int, tuple):
            raise NotImplementedError('Tuple as index')
        else:
            raise TypeError('Invalid argument type: {}'.format(type(a1)))

    def __setitem__(self, idx: int, t:T) -> None:
        if self.is_reversed:
            idx = ListIter.complement_index(idx)
        self.inner[idx] = t

    def front(self) -> T:
        return self[0]

    @staticmethod
    def complement_index(idx:int) -> int:
        return None if idx is None else (-1 * idx -1)

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
    
    def get_inner(self) -> list[T]:
        if self.is_reversed:
            return self.inner[self.end-1:self.begin-1:-1]
        else:
            return self.inner


def infinite_iterator(base_src):
    while True:
        for x in base_src:
            yield x

def natural_numbers(start = 0):
    i = start
    while True:
        i = i+1
        yield i
            

def hashOfList(ls : Iterable[T]) -> int:
    h = 0
    for x in ls:
        h = 31*h + hash(x)
    return h

def get_inner_list(ls : Iterable[T]) -> list[T] : 
    if isinstance(ls, list): 
        return ls
    else:
        return get_inner_list(ls.get_inner())
    

def equals_string(x:str, y:str) -> bool:
    return x == y

class AllowSomeDifferenceEquals:
    def __init__(self, allowed_wrongs : int):
        self.allowed_wrongs =allowed_wrongs 
        
    def equals_strings(self, x:str, y:str) -> bool:
        if x==y: return True
        if len(x)!=len(y): return False
        for (cx, cy) in zip(x, y):
            if cx != cy:
                if self.allowed_wrongs > 0:
                    self.allowed_wrongs = self.allowed_wrongs-1
                else:
                    return False
        return True
    

def split_list_on_empty_line(lines:list[str]) -> list[list[str]]:
    res = []
    tmp = []
    for line in lines:
        if len(line) == 0 and len(tmp) > 0:
            res.append(tmp)
            tmp = []
        else:
            tmp.append(line)

    if len(tmp) > 0:
        res.append(tmp)
        tmp = []

    return res


def first(it : Iterator[T], default:T, cond) -> T:
    for x in it:
        if cond(x):
            return x
    return default