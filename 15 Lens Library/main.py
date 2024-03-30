import os
from pathlib import Path
import time
from prog import Matrix
import tools
from directions import Direction

# entry point
def main():

    input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = Path(input_txt).read_text()

    m = Matrix("m", input_str)
    # print(f'calc {m.name} dir=N\n{m}\n')
        
    tilted = Matrix.tilt(m, Direction.N, True)
    tilted.name = 'tilted'
    print(f'tilt {tilted.name} dir={tilted.dir}\n{tilted}')
    
    force_1 = Matrix.calc_force(tilted, Direction.N)
    force_2 = Matrix.spin_many_times_force_north(m, 1000000000, False)

        
    print(f'force_1:{force_1}  force_2:{force_2} ')  
    
    # after 141 spin cycles (cycle detected, at 107 len=34)
    # force_2:90551 after 160 spin cycles (cnt=126, diff=34)
    # force_1:110677  force_2:90551

if __name__ == '__main__':
    main()