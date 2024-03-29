import os
from pathlib import Path
import time
from prog import Matrix
import tools
from directions import Direction

# entry point
def main():

    input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = list(Path(input_txt).read_text().splitlines())

    m = Matrix("m", input_str)
    # print(f'calc {m.name} dir=N\n{m}\n')
        
    tilted = Matrix.tilt(m, Direction.N)
    tilted.name = 'tilted'
    print(f'tilt {tilted.name} dir={tilted.dir}\n{tilted}')
    
    force_1 = Matrix.calc_force(tilted, Direction.N)
    force_2 = 0  
        
    print(f'force_1:{force_1}  force_2:{force_2}')    ## sum1:19608  sum2:26180

if __name__ == '__main__':
    main()