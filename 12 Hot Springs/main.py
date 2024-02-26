import os
import prog
from pathlib import Path
import time



input = os.path.join(os.path.dirname(__file__), 'input.txt')
input_str = Path(input).read_text()


t0 = time.perf_counter()

m = prog.Map(input_str)
sum_1 = m.sum_dist_pairs()

t1 = time.perf_counter()

m = prog.Map(input_str, 1000000)
sum_2 = m.sum_dist_pairs()

t2 = time.perf_counter()
print(f'11.1  sum:{sum_1} 11.2 sum:{sum_2}  dt1:{t1-t0}  dt2:{(t2-t1)}') # 9648398

