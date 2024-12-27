import datetime
import os
from pathlib import Path
import time
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

    input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = Path(input_txt).read_text()

    t0 = time.perf_counter()

    m = TextMap.parse_text(input_str)   
    v = prog.Guard.find_guard_pos(m)

    g = prog.Guard(v, m)
    g.walk_path()

    # def color_select(x: int, y:int, d:Direction) -> str:
    #     return prRed if Point(x,y) in g.history else prBlack

    #m.print(color_select)

    sum_1 = g.count_unique_positions()

    dt1 = time.perf_counter() - t0
    print(f'sum1:{sum_1}')  
    print(f'dt1:{dt1}') 

    # g.print_path(prBlack, prRed)
    path1 = g.history

    t1 = time.perf_counter()

    mods = []
    path_len = len(set([v.pos for v in g.history]))
    for ((attempt, p), n) in zip(g.modify_path_to_create_loops_yield(), tools.natural_numbers()):
        mods.append(p)
        print(f'{n} obst={p} attempt={attempt} mods={len(mods)} ')
        dt = time.perf_counter() - t1
        t_per_attempt = dt / attempt
        est_total_time = t_per_attempt * path_len
        est_time_left = (int)(t_per_attempt * (path_len-attempt))


# get '14:39:57':
# est_done.strftime('%H:%M:%S')
        
        print(f'time/attempt={t_per_attempt:.4f} est_total={est_total_time:.2f} est_time_left={est_time_left}')


    sum_2 = len(mods)

    dt2 = time.perf_counter() - t1

    print(f'sum1:{sum_1}  sum2:{sum_2}')    ## sum1:242  sum2:311
    print(f'dt1:{dt1}  dt2:{(dt2)}') # 20513

if __name__ == '__main__':
    main()