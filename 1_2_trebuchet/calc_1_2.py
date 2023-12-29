
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

def find_1st_digit(s : string):
    
    while len(s) > 0:
        for key in digits_dict:
            l = len(key)
            if s.startswith(key):
                return digits_dict[key]

        s = s[1:]
        
    return None

def find_last_digit(s : string):
    
    while len(s) > 0:
        for key in digits_dict:
            l = len(key)
            if s.endswith(key):
                return digits_dict[key]

        s = s[0:-1]
        
    return None




sum = 0
with open( os.path.join(source_dir, "input.txt"), "r") as file:
    for line in file.readlines():
        line = line.rstrip('\n\r')

        if line == "4b":
            bp = 17

        d1 = find_1st_digit(line)
        d2 = find_last_digit(line)
        val = d1*10 + d2
        
        sum = sum + val
        
print(sum) ## 54093  new 54078
