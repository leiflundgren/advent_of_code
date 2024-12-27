import os
from pathlib import Path
import time
import prog
from text_map import TextMap
import tools

PATTERN = "XMAS"
LEN = len(PATTERN)


# entry point
def main():

    input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = Path(input_txt).read_text()

    t0 = time.perf_counter()

    map = prog.parse_map(input_str)
    sum_1 = prog.count_all_matches_map(PATTERN, map)
    
    t1 = time.perf_counter()

    tm = TextMap.parse_text(input_str)
    sum_2 = len(prog.find_all_x_mas(tm))

    t2 = time.perf_counter()

    print(f'sum1:{sum_1}  sum2:{sum_2}')    ## sum1:242  sum2:311
    print(f'dt1:{t1-t0}  dt2:{(t2-t1)}') # 20513

if __name__ == '__main__':
    main()