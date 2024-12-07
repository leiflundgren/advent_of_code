from itertools import count
import math
import tools
import os
import desert
from desert import Node
from desert import Scenario
from pathlib import Path
import time


t0 = time.perf_counter()

input = os.path.join(os.path.dirname(__file__), 'input.txt')
lines = Path(input).read_text().splitlines()

sc = desert.parse_scenario(iter(lines))

t1 = time.perf_counter()

lengths = sc.find_loops(True)
t2 = time.perf_counter()
print(f'length:{lengths}  dt:{t2-t1}  ')

lcm_sys = math.lcm(*lengths)
print(f'lcm_sys:{lcm_sys}  dt:{t2-t1}  ')

t3 = time.perf_counter()


lcm = tools.lcm_list(lengths)

t4 = time.perf_counter()

print(f'lcm:{lcm}  dt:{t4-t3}  ')

# steps = sc.find_loop_length()
# #print(f'lcm: {tools.lcm_list(steps)}')
    

# def format_nodes(nodes : list[Node]) -> list[str]:
#     def format_node(n : Node) -> str:
#         name = n.name
#         return 'Z' if name[-1] == 'Z' else '-'
#     return list(map(format_node, nodes))


# routes = list(map(lambda n: [n], format_nodes(sc.start_pos)))
# pos = sc.start_pos
# r2 = list(map(lambda n: [f'- {n.name}'], sc.start_pos))
# for d in sc.directions:
#     nextpos = sc.move(pos, d)
#     formated = format_nodes(nextpos)
    
#     for r, f in zip(routes, formated):
#         r.append(f)
#     for r, n in zip(r2, nextpos):
#         r.append(f'{d} {n.name}')
#     pos = nextpos

# len = len(routes[0])
# print('\n')
# print('     ' + ''.join(map(lambda i:' ' if i%100!=0 else str((i//100)),  range(len))))
# print('     ' + ''.join(map(lambda i:' ' if i%10!=0 else str((i//10)),  range(len))))
# print('     ' + ''.join(map(lambda i:str(i%10),  range(len))))
# # for i in range(len(routes)):
# #     c = ' ' if i%10!=0 else str((i%10))
# #     print(c, end='')
# # for i in range(len(routes)):
# #     c = ' ' if i%10!=0 else str((i//10))
# #     print(str(i%10), end='')
# # print('     ', end='')
# for r, sp in zip(routes, sc.start_pos):
#     print(sp.name + ': ' + ''.join(r))


bp = 17



