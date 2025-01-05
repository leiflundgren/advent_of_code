import datetime
import os
from pathlib import Path
import time
from typing import Set
from map import Point
import prog
from text_map import TextMap
import tools

def prRed(skk): print("\033[91m {}\033[00m" .format(skk), end='')
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk), end='')
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk), end='')
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk), end='')
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk), end='')
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk), end='')
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk), end='')
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk), end='')


# entry point
def main():

    sum_1 = sum_2 = 0

    input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = Path(input_txt).read_text()

    t0 = time.perf_counter()

    m = TextMap.parse_text(input_str)

    path = prog.Path(m)

    for start in path.find_start_pos():
        paths = path.walk_path(start)

        endp : Set[Point] = set()
        for p in paths:
            endp.add(p[-1])

        score = len(endp)
        rating = len(paths)
            
        print(f'start:{start} score: {score} rating:{rating}')
        # for p in paths:
        #     print(Path.to_string_map(m, p))
            
        sum_1 += score
        sum_2 += rating
    

    dt1 = time.perf_counter() - t0
    print(f'sum1:{sum_1}')  
    print(f'dt1:{dt1}') 

    t1 = time.perf_counter()

    dt2 = time.perf_counter() - t1

    print(f'sum1:{sum_1}  sum2:{sum_2}')    ## sum1:242  sum2:311
    print(f'dt1:{dt1}  dt2:{(dt2)}') # 20513

if __name__ == '__main__':
    main()