
from typing import Iterator, Sequence


class BasicIterator(Iterator[T]):
    def __init__(ls:Sequence[T])