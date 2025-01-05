from typing import List, Self, Tuple


class TextMap(object):
    def __init__(self, data : List[List[int]]):
        self.data = data

    @staticmethod
    def parse_text(data : str) -> Self:
        if not isinstance(data, str): raise TypeError('arg to TextMap should be string, got ' + str(type(data)))

        return TextMap([ [int(c) for c in line ] for line in data.strip('\r\n').splitlines() ])

    @staticmethod
    def create_empty(width: int, height: int, c:int) -> Self:
        return TextMap([ [c] * width for n in range(height) ])


    def at(self, x:int, y:int) -> int:
        if 0 <= y and y < self.height() and 0 <= x and x < self.width():
            return self.data[y][x]
        else:
            return -1

    def set(self, x:int, y:int, s:int) -> None:
        if 0 <= y and y < self.height() and 0 <= x and x < self.width():
            self.data[y][x] = s



    def height(self) -> int:
        return len(self.data)
    def width(self) -> int:
        return len(self.data[0])

    def is_inside(self, x:int, y:int) -> bool:
        return 0 <= x and x < self.width() and 0 <= y and y < self.height()

    def nodes(self) -> List[Tuple[int, int, int]]:
        return [(x, y, self.at(x,y)) for y in range(self.height()) for x in range(self.width())]

    def __str__(self) -> str:
        return '\r\n'.join( (''.join([(str(c) if c >= 0 else ' ') + ' ' for c in line])) for line in self.data)



