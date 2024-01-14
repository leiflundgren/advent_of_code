
from json import load
from typing import Self


class Race:
    def __init__(self, racetime, dist):
        self.racetime = racetime
        self.mindist = dist
        
    def calc_dist(self, loadtime: int) -> int:
        assert(self.racetime >= loadtime)
        run_time = self.racetime - loadtime
        speed = loadtime * 1
        return run_time * speed

    

class Races:
    def __init__(self):
        self.races = []
        
    def add_race(self, r : Race) -> Self:
        self.races.append(r)
        return self

