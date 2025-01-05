from typing import List, Self


class TextMap(object):
    def __init__(self, text : List[str]):
        self.text = [list(line) for line in text]

    @staticmethod
    def parse_text(text : str) -> Self:
        if not isinstance(text, str): raise TypeError('arg to TextMap should be string, got ' + str(type(text)))
        return TextMap(text.strip('\r\n').splitlines())

    def at(self, x:int, y:int) -> str:
        if 0 <= y and y < self.height() and 0 <= x and x < self.width():
            return self.text[y][x]
        else:
            return '.'

    def set(self, x:int, y:int, s:str) -> None:
        if 0 <= y and y < self.height() and 0 <= x and x < self.width():
            self.text[y][x] = s



    def height(self) -> int:
        return len(self.text)
    def width(self) -> int:
        return len(self.text[0])

    def is_inside(self, x:int, y:int) -> bool:
        return 0 <= x and x < self.width() and 0 <= y and y < self.height()

  


