import datetime
import os
from pathlib import Path
import time
import prog
from text_map import TextMap
import tools


# entry point
def main():

    file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = Path(file_path).read_text()

    t0 = time.perf_counter()
      
    measures = prog.parse(input_str)

    w = prog.Worker()
    sum_1 = w.sum_result_of_matching(measures)

    dt1 = time.perf_counter() - t0
    print(f'sum1:{sum_1}')  
    print(f'dt1:{dt1}') 

    t1 = time.perf_counter()

    
    sum_2 = 0

    dt2 = time.perf_counter() - t1

    print(f'sum1:{sum_1}  sum2:{sum_2}')    ## sum1:242  sum2:311
    print(f'dt1:{dt1}  dt2:{(dt2)}') # 20513

if __name__ == '__main__':
    main()