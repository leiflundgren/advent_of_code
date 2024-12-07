
from pathlib import Path
import os.path

source_path = Path(__file__).resolve()
source_dir = source_path.parent


sum = 0

def eval_digit(c):
    match c:
        case '0': return 0
        case '1': return 1
        case '2': return 2
        case '3': return 3 
        case '4': return 4
        case '5': return 5
        case '6': return 6
        case '7': return 7
        case '8': return 8
        case '9': return 9
        case _: return None

def first_digit(s):
    for c in s:
        d = eval_digit(c)
        if d is None: continue
        return d


def last_digit(s): return first_digit(reversed(s))

with open( os.path.join(source_dir, "input.txt"), "r") as file:
    for line in file.readlines():
        d1 = first_digit(line)
        d2 = last_digit(line)
        val = d1*10 + d2
        
        sum = sum + val
        
print(sum) ## 54601
