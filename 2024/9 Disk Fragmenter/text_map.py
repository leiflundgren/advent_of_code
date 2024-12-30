from typing import Iterator, List, Self, Tuple

from point import Point


class TextMap(object):
    def __init__(self, text : List[str]):
        self.text = [list(line) for line in text]

    @staticmethod
    def parse_text(text : str) -> Self:
        if not isinstance(text, str): raise TypeError('arg to TextMap should be string, got ' + str(type(text)))
        return TextMap(text.strip('\r\n').splitlines())

    def at(self, p:Point) -> str:
        if 0 <= p.y and p.y < self.height() and 0 <= p.x and p.x < self.width():
            return self.text[p.y][p.x]
        else:
            return '.'

    def set(self, p:Point, s:str) -> None:
        if 0 <= p.y and p.y < self.height() and 0 <= p.x and p.x < self.width():
            self.text[p.y][p.x] = s


    def nodes(self) -> Iterator[Tuple[Point, str]]:
        for x in range(self.width()):
            for y in range(self.height()):
                p = Point(x, y)
                yield (p, self.at(p))

    def height(self) -> int:
        return len(self.text)
    def width(self) -> int:
        return len(self.text[0])

    def contains(self, p:Point) -> bool:
        return 0 <= p.x and p.x < self.width() and 0 <= p.y and p.y < self.height()

    # \return all points contined in the map
    def containing(self, it : Iterator[Point]) -> Iterator[Point]:
        for p in it:
            if self.contains(p):
                yield p


