from re import X
from directions import Direction
import tools
from enum import Enum
from typing import Dict, Iterable, Iterator, List, Self, Sequence, Tuple
from functools import cmp_to_key

class Order(object):
    def __init__(self, first, second) -> None:
        self.first = first
        self.second = second
        self.pair = (first, second)



class PrintJob(object):
    def __init__(self, pages : List[int]) -> None:
        self.pages = pages

    def __eq__(self, value: object) -> bool:
        return self.pages == value.pages

    def __hash__(self) -> int:
        return hash(frozenset(self.pages))

    def __str__(self) -> str:
        return ','.join([ str(x) for x in self.pages])

    def __repr__(self) -> str:
        return str(self)

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
        self.dict_orders = {}
        self.sorted_jobs = None

        for o in self.orders:
            self.dict_orders.setdefault(o.first, []).append(o.second)
            # self.dict_orders.setdefault(o.second, []).append(o.first)

    def filter_jobs_in_correct_order(self) -> List[PrintJob]:
        if self.sorted_jobs is None:
            self.sort_jobs(self.printjobs)

        self.correct = list(filter( lambda j: j.in_correct_order(self.orders), self.printjobs))
        self.incorrect = list(self.printjobs)
        for j in self.correct:
            self.incorrect.remove(j)
        return self.correct


    def sort_jobs(self, jobs : List[PrintJob]) -> List[PrintJob]:
        def comparer(x, y):
            for (a, b, r) in [(x,y, -1), (y,x, 1)]:
                z : List[int] = self.dict_orders.get(a)
                if z is not None and b in z:
                    return r
            return 0

        sorted_jobs = []
        for job in jobs:
            k = cmp_to_key(comparer)
            s = list(sorted(job.pages, key=k))
            sorted_jobs.append(PrintJob(s))
        return sorted_jobs


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



def sum_middle_page(jobs : List[PrintJob]) -> int:
    return sum( j.middle_page() for j in jobs)
