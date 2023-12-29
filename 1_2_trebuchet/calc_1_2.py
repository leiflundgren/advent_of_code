
import math
from pathlib import Path
import os.path
import string

source_path = Path(__file__).resolve()
source_dir = source_path.parent



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
        d1 = find_1st_digit(line)
        d2 = find_last_digit(line)
        val = d1*10 + d2
        
        sum = sum + val
        
print(sum) ## 54093
