from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import wait
import multiprocessing
import os
from pickle import UnpicklingError
from threading import Thread
import prog
from pathlib import Path
import time
from SimplerPermut import Perm2
from prog import Springs



def run_one(n:int, scen:Springs, use_cache:bool, five_fold:bool) -> int:
    t0 = time.perf_counter()
   
   
    if isinstance(scen, str):
        # print(f'got scen as string: {scen}'        )
        scen = prog.parse_springs(scen)
        
    assert isinstance(scen, Springs), f'expected scen to be Springs, was {type(scen)}: {scen}'
    
    # print(f'{scen} {use_cache} {five_fold} ')

    perm = Perm2(use_cache, False)
    if five_fold: scen = scen.five_fold()
    c = perm.calc_permutations(scen)

    t1 = time.perf_counter()
    # if five_fold:
    #     print(f'12.2-{n} count:{c} dt1:{t1-t0} {scen} {use_cache}')

    return c

def run_(executor : ProcessPoolExecutor, input_str: list[str], use_cache:bool, five_fold:bool) -> int:
    t0 = time.perf_counter()
    sum1 = 0
    l = len(input_str)
    scens = [prog.parse_springs(i) for i in input_str]
    for scen in scens:
        assert isinstance(scen, Springs), f'expected scen to be Springs, was {type(scen)}: {scen}'
        
    use_ls = [use_cache for i in range(l)]
    five_ls = [five_fold for i in range(l)]
    n_ls = [i for i in range(l)]
    if executor is None:
        futur = list(map(run_one, n_ls, scens, use_ls, five_ls))
    else:
        futur = executor.map(run_one, n_ls, input_str, use_ls, five_ls)
    for result in futur:
        sum1 = sum1 + result
    
    t1 = time.perf_counter()
    print(f'{"sequential" if executor is None else "parallell"}  {"12.2" if five_fold else "12.1"} {"cache" if use_cache else "no cache"}  sum_1:{sum1} dt1:{t1-t0}  ') # 7633
    return sum1
    
# def run_12_1_cache(executor : ProcessPoolExecutor):
#     t0 = time.perf_counter()
#     sum2 = 0
#     for input in input_str:
#         springs = prog.parse_springs(input)

#         perm = Perm2(True, False)
#         c = perm.calc_permutations(springs)
#         sum2 = sum2 + c

#     t1 = time.perf_counter()
#     print(f'12.1 cache sum_2:{sum2}  dt1:{t1-t0}') # 7633

# def run_12_2_nocache(executor : ProcessPoolExecutor):
#     t0 = time.perf_counter()
#     sum1 = 0
#     for input in input_str:
#         springs = prog.parse_springs(input).five_fold()

#         perm = Perm2(False, False)
#         c = perm.calc_permutations(springs)
#         sum1 = sum1 + c
    
#     t1 = time.perf_counter()
#     print(f'12.2 no cache sum_1:{sum1} dt1:{t1-t0}  ') # 7633
    

# def run_12_2_cache(executor : ProcessPoolExecutor):
#     t0 = time.perf_counter()
#     sum2 = 0
#     for input in input_str:
#         springs = prog.parse_springs(input).five_fold()

#         perm = Perm2(True, False)
#         c = perm.calc_permutations(springs)
#         sum2 = sum2 + c

#     t1 = time.perf_counter()
#     print(f'12.2 cache sum_2:{sum2}  dt1:{t1-t0}') # 7633


# custom task that will sleep for a variable amount of time
def task(t, name):
    # sleep for less than a second
    time.sleep(t/3)
    return f'Task: {name} done.'
  
# entry point
def main():
    
    input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = list(Path(input_txt).read_text().splitlines())

    
    # with ProcessPoolExecutor(10) as executor:
    #     # execute tasks concurrently and process results in order
    #     futur = executor.map(task, range(10), [f'name {i}' for i in range(10)])
    #     for result in futur:
    #         # report the result
    #         print(result)
    
    s = prog.parse_springs(input_str[0])
    c = run_one(-1, s, False, False)

    s = prog.parse_springs('???.????...???#?#? 2,4,2,4')
    c = run_one(-2, s, False, False)

    # input_str = input_str[:10]

    _12_1_c = 0
    _12_1_p = 0
    _12_2_c = 0

    #run_(None, input_str, True, False)
    run_(None, input_str, True, True)
    
    # create the pool of workers
    with ProcessPoolExecutor(13) as executor:



        _12_1_c = run_(None, input_str, True, False)
        # _12_1_p = run_(executor, input_str, False, False)
        _12_2_c = run_(None, input_str, True, True)
        _12_2_c_e = run_(executor, input_str, True, True)
        #_12_run_(executor, False, True)
        pass


    print('All tasks are done!')
    print(f'_12_1 count: {_12_1_c}  _12_2_c:{_12_2_c}')
 
if __name__ == '__main__':
    main()