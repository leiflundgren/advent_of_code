from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import wait
import multiprocessing
import os
from threading import Thread
import prog
from pathlib import Path
import time
from SimplerPermut import Perm2


input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
input_str = list(Path(input_txt).read_text().splitlines())

def run_one(input_str:str, use_cache:bool, five_fold:bool) -> int:
    springs = prog.parse_springs(input)

    perm = Perm2(False, False)
    c = perm.calc_permutations(springs)
    return c

def run_12_1_nocache():
    t0 = time.perf_counter()
    sum1 = 0
    
    for input in input_str:
        springs = prog.parse_springs(input)

        perm = Perm2(False, False)
        c = perm.calc_permutations(springs)
        sum1 = sum1 + c
    
    t1 = time.perf_counter()
    print(f'12.1 no cache sum_1:{sum1} dt1:{t1-t0}  ') # 7633
    
def run_12_1_cache():
    t0 = time.perf_counter()
    sum2 = 0
    for input in input_str:
        springs = prog.parse_springs(input)

        perm = Perm2(True, False)
        c = perm.calc_permutations(springs)
        sum2 = sum2 + c

    t1 = time.perf_counter()
    print(f'12.1 cache sum_2:{sum2}  dt1:{t1-t0}') # 7633

def run_12_2_nocache():
    t0 = time.perf_counter()
    sum1 = 0
    for input in input_str:
        springs = prog.parse_springs(input).five_fold()

        perm = Perm2(False, False)
        c = perm.calc_permutations(springs)
        sum1 = sum1 + c
    
    t1 = time.perf_counter()
    print(f'12.2 no cache sum_1:{sum1} dt1:{t1-t0}  ') # 7633
    

def run_12_2_cache():
    t0 = time.perf_counter()
    sum2 = 0
    for input in input_str:
        springs = prog.parse_springs(input).five_fold()

        perm = Perm2(True, False)
        c = perm.calc_permutations(springs)
        sum2 = sum2 + c

    t1 = time.perf_counter()
    print(f'12.2 cache sum_2:{sum2}  dt1:{t1-t0}') # 7633




    ############
    
# entry point
def main():
    # create the pool of workers
    with ProcessPoolExecutor(13) as executor:

        t_12_1_nocache = executor.submit(run_12_1_nocache)
        t_12_1_cache = executor.submit(run_12_1_cache)
        t_12_2_nocache = executor.submit(run_12_2_nocache)
        t_12_2_cache = executor.submit(run_12_2_cache)


        wait([t_12_1_nocache, t_12_1_cache, t_12_2_nocache, t_12_2_cache])


    print('All tasks are done!')
 
if __name__ == '__main__':
    main()