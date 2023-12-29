
import math
from pathlib import Path
import os.path
import string

source_path = Path(__file__).resolve()
source_dir = source_path.parent



digits_dict = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3 ,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    # '0': 0,
    'one': 1,
    'two': 2,
    'three': 3 ,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

def find_digits(s : string):
    res = []
    
    if s == "4b\n":
        bp=17

    while len(s) > 0:
        match = None
        for key in digits_dict:
            l = len(key)
            if s.startswith(key):
                match = key
                break
            
        if not match is None:
            res.append(digits_dict[match])
            s = s[len(match):]
        else:
            s = s[1:]
        
    return res



sum = 0
with open( os.path.join(source_dir, "input.txt"), "r") as file:
    for line in file.readlines():
        digits = find_digits(line)
        if len(digits) == 0:
            print("Bad line " + line)
        elif len(digits) == 1:
            val = digits[0]
        else:
            d1 = digits[0]
            d2 = digits[-1]
            val = d1*10 + d2
        
        sum = sum + val
        
print(sum) ## 54093
