import datetime
from importlib.metadata import files
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

    #for f in [ 'input2.txt', 'input.txt' ]:
    for f in [ 'input.txt' ]:
        file_path = os.path.join(os.path.dirname(__file__), f)
        input_str = Path(file_path).read_text()

        t0 = time.perf_counter()
      
        m = prog.FileSystem.parse(input_str, False)

        print('Beginning input\n' + prog.FileSystem.disk_to_str(m.disk[:100], True))

        m.compact_disk()
        sum_1 = m.calc_checksum()

        dt1 = time.perf_counter() - t0
        print(f'sum1:{sum_1}')  
        print(f'dt1:{dt1}') 
        print('Compact disk \n' + prog.FileSystem.disk_to_str(m.disk[:100], True))



        m = prog.FileSystem.parse(input_str, True)

        print('Beginning input\n' + prog.FileSystem.block_to_str(m.blocks[:100], True))

        t1 = time.perf_counter()
        m.compact_blocks()
        sum_2 = m.calc_checksum()

        dt1 = time.perf_counter() - t0
        print(f'sum1:{sum_1}')  
        print(f'dt1:{dt1}') 

        dt2 = time.perf_counter() - t1
        print('Compact disk \n' + prog.FileSystem.block_to_str(m.blocks[:100], True))

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