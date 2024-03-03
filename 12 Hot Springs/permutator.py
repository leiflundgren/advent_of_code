from typing import Dict
from prog import Springs


# if arrangement take X and fields is X+1
# returns number possible arrangements, 0 if not calculated
def permut_one_free(springs:Springs) -> int:
    if springs.sum_arrangement() + 1 == springs.sum_springs():
        return 2
    return 0

class Permutor:
    def __init__(self, springs:Springs):
        self.springs = springs
        self.cache : Dict[Springs, int] = {}


    def calc