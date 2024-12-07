import os
from pathlib import Path
import time
from prog import Matrix
import tools


# entry point
def main():

    input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = list(Path(input_txt).read_text().splitlines())

    sum_1 = 0; sum_2 = 0
    
    for (n, pattern) in zip(tools.natural_numbers(), tools.split_list_on_empty_line(input_str)):
        if n == 30:
            bp =17
        m = Matrix(f'file-{n}', pattern)
        s1 = m.sum_lines(0)
        s2 = m.sum_lines(1)
        sum_1 += s1
        sum_2 += s2

             
        rows = m.find_mirrors(1)
        columns = m.rotate().find_mirrors(1)


        print(f'{m.name}  dot1:{s1}  dot2:{s2}')
        if len(rows) + len(columns) != 1:
            print(f'Found rows {rows} cols{columns}')
        print(f'\norg\n{m}\nrotat\n{m.rotate()}\n')
        
        bp = 18

    print(f'sum1:{sum_1}  sum2:{sum_2}')    ## sum1:19608  sum2:26180

if __name__ == '__main__':
    main()