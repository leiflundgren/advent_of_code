import os
from pathlib import Path
import time
import prog
import tools


# entry point
def main():

    input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = list(Path(input_txt).read_text().splitlines())
    input = list(map(prog.parse_line, input_str))
    sum_1 = 0; sum_2 = 0
    
    # Part 1
    for (n, levels) in zip(tools.natural_numbers(), input):
        if prog.is_safe(levels):
            sum_1 += 1

    print(f'sum1:{sum_1}  sum2:{sum_2}')    ## sum1:242  sum2:26180

if __name__ == '__main__':
    main()