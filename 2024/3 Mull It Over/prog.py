import re
import tools
from enum import Enum
from typing import Iterable, Iterator, List, Self, Sequence, Tuple

def parse_muls(s: str) -> List[str]:
    # mul(1,999)
    # xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

    

    hits = re.findall('(mul\(\d{1,3},\d{1,3}\))', s)
    return hits
