from re import X
from directions import Direction
import tools
from enum import Enum
from typing import Iterable, Iterator, List, Self, Sequence, Tuple


class Order(object):
    def __init__(self, first, second) -> None:
        self.first = first
        self.second = second
        self.pair = (first, second)

class PrintJob(object):
    def __init__(self, pages : List[int]) -> None:
        self.pages = pages


    def adheres_to(self, order : Order) -> bool:
        idx1 = self.pages.index(order.first)
        if idx1 < 0:
           return True
        idx2 = self.pages.index(order.second)
        return idx2 < 0 or idx2 > idx1
       




def parse(txtmap: str) -> Tuple[List[Order], List[PrintJob]]:
    lines = txtmap.strip('\r\n').splitlines()
    
    # First parses orders
    # 96|15
    orders = []
    while lines:
        l = lines.pop(0)
        if len(l) == 0:
            break

        pipe = l.index('|')
        orders.append(Order(int(l[:pipe]), int(l[pipe+1:])))

    # The parse print-jobs
    # 74,64,82,87,27
    printjobs = []
    while lines:
        l = lines.pop(0)
        printjobs.append(PrintJob([int(x) for x in l.split(',') ]))

    return (orders, printjobs)


