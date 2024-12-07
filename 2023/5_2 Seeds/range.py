
class Range:
    def __init__(self, num, len):
        self.num = num
        self.len = len

    def __str__(self) -> str:
        return f'Range({self.num}, {self.len})'

    def range(self):
        return range(self.num, self.num+self.len)
        
def parse_seeds_from_list(nums: list[int]) -> list[Range]:
    res = []
    for i in range(0, len(nums), 2):
        start = nums[i+0]
        length = nums[i+1]
        res.append(Range(start, length))
    return res

def parse_seeds_from_str(line:str) -> list[Range]:
    return parse_seeds_from_list(list(map(int, line.strip().split(' '))))

