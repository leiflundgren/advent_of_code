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
        try:
            idx1 = self.pages.index(order.first)
        except ValueError:
           return True
        try:
            idx2 = self.pages.index(order.second)
            return idx2 > idx1
        except ValueError:
           return True
       
    def in_correct_order(self, orders : List[Order]) -> bool:
        return all( self.adheres_to(o) for o in orders)

    def middle_page(self) -> int:
        return self.pages[len(self.pages)//2]

class Scenario(object):
    def __init__(self, orders : List[Order], printjobs : List[PrintJob]) -> None:
        self.orders = orders
        self.printjobs = printjobs

    def jobs_in_correct_order(self) -> List[PrintJob]:
        return list(filter( lambda j: j.in_correct_order(self.orders), self.printjobs))

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


