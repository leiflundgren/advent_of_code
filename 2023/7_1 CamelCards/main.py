import os
import  card
from pathlib import Path
import time


t0 = time.perf_counter()

input = os.path.join(os.path.dirname(__file__), 'input.txt')
lines = Path(input).read_text().splitlines()

hands = list(map(lambda s: card.parse_hand(s), lines))

t1 = time.perf_counter()

card.rank_hands(hands)
winnings = card.sum_winnings(hands) # 250120186

t2 = time.perf_counter()
print(f'winnings:{winnings}  dt1:{t1-t0}  dt2:{(t2-t1)}')


