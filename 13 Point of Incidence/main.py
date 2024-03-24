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

    sum = 0
    
    for (n, pattern) in zip(tools.natural_numbers(), split_list_on_empty_line(input_str)):
        m = Matrix(pattern)
        print(f'{n}\n{m}')
        sum = sum + m.sum_lines()

    print(sum)    ## 29130

if __name__ == '__main__':
    main()