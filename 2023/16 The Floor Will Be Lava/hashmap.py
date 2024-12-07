import prog
import tools

class HashMap():
    def __init__(self):
        self.data = [None]*256
        for i in range(256):
            self.data[i] = []
        pass
    
    def hashcode(self, s:str) -> int:
        return prog.calc_hash(s)

    def add(self, lbl:str, focallen: int) -> tuple[str,int]:
        h = self.hashcode(lbl)
        ls = self.data[h]
        for i in range(len(ls)):
            (lbl2, focallen2) = ls[i]
            if lbl == lbl2:
                ls[i] = (lbl, focallen)
                return (lbl2, focallen2)
        ls.append((lbl, focallen))
        return (lbl, focallen)

    def remove(self, s:str) -> tuple[str,int]:
        h = self.hashcode(s)
        ls = self.data[h]
        for i in range(len(ls)):
            (lbl, focallen) = ls[i]
            if s == lbl:
                ls.pop(i)
                return (lbl, focallen)
            
        return None
            
    def perform_operation(self, str:str) -> tuple[str,int]:
        if str[-1] == '-':
            return self.remove(str[:-1])
        elif str[-2] == '=':
            return self.add(str[:-2], int(str[-1]))
        else:
            raise ValueError(f'Invalid input str "{str}"')
        

    def calc_focal_length_box(self, box : list[tuple[str, int]]) -> int:
        return sum([ i*foclen for (i, (label, foclen)) in zip(range(1, 1+len(box)), box) ])
    
    def calc_focal_length_total(self):
        return sum([ i * self.calc_focal_length_box(box) for (i, box) in zip(range(1, 1+len(self.data)), self.data)])
    
            