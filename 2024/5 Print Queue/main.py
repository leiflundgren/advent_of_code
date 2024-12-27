import os
import pathlib 
import time
import prog
import tools

PATTERN = "XMAS"
LEN = len(PATTERN)


# entry point
def main():

    input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = pathlib.Path(input_txt).read_text().strip()

    t0 = time.perf_counter()

    (orders, pjobs) = prog.parse(input_str)
    sc = prog.Scenario(orders, pjobs)
    correct_jobs = sc.filter_jobs_in_correct_order()

    sum_1 = sum( j.middle_page() for j in correct_jobs)
    
    t1 = time.perf_counter()

    sc.filter_jobs_in_correct_order()
    batch2 = sc.sort_jobs(sc.incorrect)
    sum_2 = prog.sum_middle_page(batch2)

    t2 = time.perf_counter()

    print(f'sum1:{sum_1}  sum2:{sum_2}')    ## sum1:4569  sum2:6456
    print(f'dt1:{t1-t0}  dt2:{(t2-t1)}') # 20513

if __name__ == '__main__':
    main()