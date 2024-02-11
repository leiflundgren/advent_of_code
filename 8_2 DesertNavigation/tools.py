
import math
import itertools

def infinite_iterator(base_src):
    while True:
        for x in base_src:
            yield x
            
def natural_numbers(start:int = 1):
    return itertools.count(start)


def lcm_list(numbers:list[int]) -> int:
    def gcd(n, m):
        if m == 0:
            return n
        return gcd(m, n % m)

    lcm = 1
    for i in numbers:
        lcm = lcm * i // gcd(lcm, i)
    return lcm
    