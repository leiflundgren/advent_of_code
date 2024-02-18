import os
import prog
from pathlib import Path
import time


t0 = time.perf_counter()

input = os.path.join(os.path.dirname(__file__), 'input.txt')
scenario = Path(input).read_text()


field = prog.ParseField(scenario)
print(str(field))
 
start_pos = next(filter(lambda n: n.value field.all_nodes()
                        get_start_pos
t1 = time.perf_counter()

self.assertEqual(5, len(field.field))
self.assertEqual(parse_pipe('7'), field.get(3, 1).value)
n11 = field.get(1,1)
self.assertTrue(n11.can_move_E())
self.assertFalse(n11.can_move_W())
self.assertFalse(n11.can_move_N())
self.assertTrue(n11.can_move_S())
        
loop = find_loop(n11)
self.assertEqual(8, len(loop))
self.assertEqual(n11, loop[0])
self.assertEqual(field.get(3,3), loop[4])
self.assertEqual(4, len(loop))

t2 = time.perf_counter()
print(f'9.1  sum:{sum_next} 9.2 sum:{sum_prev}  dt1:{t1-t0}  dt2:{(t2-t1)}') # 1743490457

