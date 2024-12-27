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
    
    g.print_path(prBlack, prRed)

    t1 = time.perf_counter()

    #tm = TextMap.parse_text(input_str)
    sum_2 = 0 # len(prog.find_all_x_mas(tm))

    t2 = time.perf_counter()

    print(f'sum1:{sum_1}  sum2:{sum_2}')    ## sum1:242  sum2:311
    print(f'dt1:{t1-t0}  dt2:{(t2-t1)}') # 20513

if __name__ == '__main__':
    main()