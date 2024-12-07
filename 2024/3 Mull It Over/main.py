import os
from pathlib import Path
import time
import prog
import tools


# entry point
def main():

    input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = ''.join(list(Path(input_txt).read_text().splitlines()))
    input = prog.parse_muls_pairs(input_str)
    sum_1 = 0
    sum_2 = 0
    
    # Part 1
    for (n, (x, y)) in zip(tools.natural_numbers(), input):
        sum_1 += x*y

    print(f'sum1:{sum_1}  sum2:{sum_2}')    ## sum1:191183308  sum2:311

if __name__ == '__main__':
    main()