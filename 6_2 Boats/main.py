

import os

import race

# Time:        35     69     68     87
# Distance:   213   1168   1086   1248

races = race.Races()\
    .add_race(race.Race(35696887, 213116810861248))



best_loadtimes = []
for r in races.races:
    best_loadtimes.append(r.find_loadtimes_better_than(r.mindist))

sum = 1
for best_ls in best_loadtimes:
    sum *= len(best_ls)

print('posibilites:', sum) # 
