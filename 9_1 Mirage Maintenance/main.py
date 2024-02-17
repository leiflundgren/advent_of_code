import os
import desert
from pathlib import Path
import time


t0 = time.perf_counter()

input = os.path.join(os.path.dirname(__file__), 'input.txt')
lines = Path(input).read_text().splitlines()

sc = desert.parse_scenario(iter(lines))

t1 = time.perf_counter()

steps = sc.walk_to_end()

t2 = time.perf_counter()
print(f'steps:{steps}  dt1:{t1-t0}  dt2:{(t2-t1)}') # 20513


