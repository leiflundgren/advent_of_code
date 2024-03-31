from codecs import charmap_build
from ftplib import error_reply
import os
from pathlib import Path
import time
from prog import Matrix
import prog
import tools
from directions import Direction

# entry point
def main():

    input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = Path(input_txt).read_text()
                     
    input_str = input_str.replace('/', Direction.char_forward_angle)
    input_str = input_str.replace('\\', Direction.char_back_angle)
    input_str = input_str.replace('|', Direction.char_vertial)
    input_str = input_str.replace('-', Direction.char_horizontal)
        
    input_ls = input_str.splitlines()

    m = Matrix("big", input_ls)
    # print(f'calc {m.name} dir=N\n{m}\n')
        
    t0 = time.perf_counter() 
    path = m.trace_path((1,1), Direction.E)
    t1 = time.perf_counter() 

    m.color_mark( Matrix.path_to_points(path), prog.color_Red)
    print(f"\npath calc in {t1-t0}")
    print(m.as_color_text())
        
    uniq = Matrix.path_to_points(path)

    max_en = 0
    edges = []    
    for i in range(1, 1+m.get_width()):
        edges.append(((1, i), Direction.S))
        edges.append(((m.get_height(), i), Direction.N))
    for i in range(1, 1+m.get_height()):
        edges.append(((1, i), Direction.E))
        edges.append(((m.get_width(), i), Direction.W))

    for (pos, dir) in edges:
        t0 = time.perf_counter() 
        path = Matrix.path_to_points(m.trace_path(pos, dir))
        t1 = time.perf_counter() 
        energized = len(path)
        if energized > max_en:
            m.color_mark(m.get_points(), prog.color_Yellow)
            m.color_mark(path, prog.color_Red)
            
            print(f'Better part starting at {pos} {dir} gives {energized} J (old {max_en}) took {t1-t0}')
            print(m.as_color_text())
            
            max_en = energized
                
    print(f'enegized-1:{len(uniq)}  force_2:{max_en} ')  # 6740  NA
    

if __name__ == '__main__':
    main()