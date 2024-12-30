import datetime
import os
from pathlib import Path
import time
from point import Point
import prog
from text_map import TextMap
import tools


# entry point
def main():
    sum_1 = sum_2 = -1

    file_path = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = Path(file_path).read_text()

    t0 = time.perf_counter()
      
    m = TextMap.parse_text(input_str)

    w = prog.Worker(m)
    points = list(w.find_interference_point(True))
    sum_1 = len(points)

    dt1 = time.perf_counter() - t0
    print(f'sum1:{sum_1}')  
    print(f'dt1:{dt1}') 

    t1 = time.perf_counter()

    points = list(w.find_interference_point(False))
    setp = set(points)
    if len(points) != len(setp):
        bp = 17
    sum_2 = len(points)

    dt2 = time.perf_counter() - t1

    print(f'sum1:{sum_1}  sum2:{sum_2}')    ## sum1:242  sum2:311
    print(f'dt1:{dt1}  dt2:{(dt2)}') # 20513

    # for y in range(m.height()):
    #     for x in range(m.width()):
    #         p = Point(x, y)
    #         val = m.at(p)
    #         pr = tools.prRed if p in points else tools.prBlack
    #         pr(val + ' ')
    #     print()


if __name__ == '__main__':
    main()