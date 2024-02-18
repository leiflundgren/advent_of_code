import os
import prog
from pathlib import Path
import time


t0 = time.perf_counter()

input = os.path.join(os.path.dirname(__file__), 'input.txt')
scenario = Path(input).read_text()


field = prog.ParseField(scenario)
print(str(field))
 
t1 = time.perf_counter()

start_pos = field.get_start_pos()
loop = prog.find_loop(start_pos)
dist = len(loop)/2

t2 = time.perf_counter()
print(f'10.1  start:{start_pos} dist:{dist}  dt1:{t1-t0}  dt2:{(t2-t1)}') # 1743490457
