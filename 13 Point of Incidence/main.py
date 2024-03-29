import os
from pathlib import Path
import time
from prog import Matrix
import tools

def split_list_on_empty_line(lines:list[str]) -> list[list[str]]:
    res = []
    tmp = []
    for line in lines:
        if len(line) == 0 and len(tmp) > 0:
            res.append(tmp)
            tmp = []
        else:
            tmp.append(line)

    if len(tmp) > 0:
        res.append(tmp)
        tmp = []

    return res


# entry point
def main():

    input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = list(Path(input_txt).read_text().splitlines())

    sum_1 = 0; sum_2 = 0
    
    for (n, pattern) in zip(tools.natural_numbers(), split_list_on_empty_line(input_str)):
        m1 = Matrix(pattern, Matrix.lines_exactly_equal)
        print(f'{n}\n{m1}')
        sum_1 = sum_1 + m1.sum_lines()

        m2 = Matrix(pattern, Matrix.lines_1_difference)
        sum_2 = sum_2 + m2.sum_lines()


    print(f'sum1:{sum_1}  sum2:{sum_2}')    ## 29130

if __name__ == '__main__':
    main()