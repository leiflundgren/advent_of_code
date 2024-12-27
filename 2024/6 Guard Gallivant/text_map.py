from typing import List, Self


class TextMap(object):
    def __init__(self, text : List[str]):
        self.text = text

    @staticmethod
    def parse_text(text : str) -> Self:
        if not isinstance(text, str): raise TypeError('arg to TextMap should be string, got ' + str(type(text)))
        return TextMap(text.strip('\r\n').splitlines())

    def at(self, x:int, y:int) -> str:
        if 0 <= y and y < len(self.text):
            if 0 <= x and x <= len(self.text[y]):
                return self.text[y][x]
        return '.'

    def height(self) -> int:
        return len(self.text)
    def width(self) -> int:
        return len(self.text[0])

    def is_inside(self, x:int, y:int) -> bool:
        return 0 <= x and x < self.width() and 0 <= y and y < self.height()

  


