import os
import prog
from pathlib import Path
import time
import fields


t0 = time.perf_counter()

input = os.path.join(os.path.dirname(__file__), 'input.txt')
scenario = Path(input).read_text()


field = fields.ParseField(scenario)
print(str(field))
 
t1 = time.perf_counter()

start_pos = field.get_start_pos()
loop = prog.find_loop(start_pos)
dist = len(loop)/2


t2 = time.perf_counter()
print(f'10.1  start:{start_pos} dist:{dist}  dt1:{t1-t0}  dt2:{(t2-t1)}') # 6890

field = prog.clear_non_loop(field, loop)
print('loop cleared:')
print(field)

scaled = prog.tranform_up3(field)
scaled_start = scaled.get_start_pos()


# edge = prog.find_edge_nodes(scaled, 0)

print(f'edges checked  bounds: {scaled.get_bounds()}')
print(str(scaled))


f2 = prog.mark_outside_inside(scaled)
print(f'bounds: {f2.get_bounds()}')
print(str(f2))
            
rescaled = prog.tranform_down3(f2)
print(f'rescaled  bounds: {rescaled.get_bounds()}')
print(str(rescaled))
            
inside = prog.count_inside(rescaled)
print(f'Inside count is: {inside}')
