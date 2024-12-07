
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

    # def interval_half_best_loadtime(self) -> int:
    #     low = 0        
    #     high = self.racetime
        
    #     low_dist = self.calc_dist(low)
    #     hi_dist = self.calc_dist(high)

    #     last = -1
    #     while True:
    #         half = (high+low)//2
    #         if last == half:
    #             break
    #         half_dist = self.calc_dist(half)            

    #         last = half
    #         if low_dist > half_dist:
    #             high = half
    #             hi_dist = half_dist
    #         else:
    #             low = half
    #             low_dist = half_dist
            
    #     if last == hi_dist:
    #         return last
    #     elif self.calc_dist(last) < self.calc_dist(last+1):
    #         return last+1
    #     else:
    #         return last
        

    def find_loadtimes_better_than(self, limit_dist: int) -> list[int] :
        #def natural_numbers():
        #    yield from enumerate(iter(int,1, 1))
        def natural_numbers():
            i = 0
            while True:
                i = i+1
                yield i


        best = self.racetime // 2
        dist = self.calc_dist(best)
        if dist <= limit_dist:
            return []
        res = [best]

        for i in natural_numbers():
            dist = self.calc_dist(best-i)
            if dist > limit_dist:
                res.append(best-i)
            else:
                break
        for i in natural_numbers():
            dist = self.calc_dist(best+i)
            if dist > limit_dist:
                res.append(best+i)
            else:
                break
        res.sort()
        return res               
    

class Races:
    def __init__(self):
        self.races = []
        
    def add_race(self, r : Race) -> Self:
        self.races.append(r)
        return self

