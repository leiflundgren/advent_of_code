
from enum import Enum
from os import name
import stat
from typing import Iterator, Self

import functools
from weakref import ReferenceType

import collections

class Card:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'Card {self.name}'

    def __hash__(self) -> int:
        return self.value    
    def __eq__(self, __value: object) -> bool:
        return self.value == __value.value
    def __cmp__(self, other: object) -> int:
        return self.value - other.value
        
    
card_types = [
    Card('A', 14),
    Card('K', 13),
    Card('Q', 12),
    Card('J', 0),
    Card('T', 10),
    Card('9', 8),
    Card('8', 7),
    Card('7', 6),
    Card('6', 5),
    Card('5', 4),
    Card('4', 3),
    Card('3', 2),
    Card('2', 1),
]

card_dict = dict(map(lambda c: (c.name, c), card_types))

def parse_cards(str_cards:str) -> list[Card] :
    return list(map(lambda chr: card_dict[chr], str_cards))
        

class HandType:
    def __init__(self, name:str, value:int):
        self.name = name
        self.value = value
        self.with_joker : Self = None
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.name
    
ht_nothing = HandType('Nothing-only jokers', 0)
ht_highcard = HandType('HighCard', 1)
ht_pair = HandType('Pair', 2)
ht_twopair = HandType('TwoPair', 3)
ht_threekind = HandType('ThreeOfKind', 4)
ht_house = HandType('FullHouse', 5)
ht_fourkind = HandType('FourOfKind', 6)
ht_fivekind = HandType('FiveOfKind', 7)    
    
ht_nothing.with_joker = ht_highcard
ht_highcard.with_joker = ht_pair
ht_pair.with_joker = ht_threekind
ht_twopair.with_joker = ht_house
ht_threekind.with_joker = ht_fourkind
ht_house.with_joker = ht_fourkind
ht_fourkind.with_joker = ht_fivekind    

hand_types = [
    ht_nothing,
    ht_highcard,
    ht_pair,
    ht_twopair,
    ht_threekind,
    ht_house,
    ht_fourkind,
    ht_fivekind,       
]

class Hand:
    def __init__(self, cards : list[Card], bid : int):
        self.cards = cards
        self.bid = bid
        self.hand_type = Hand.use_jokers(self.cards, Hand.identify_hand(self.cards))
        self.rank = -1
        self.card_string = ''.join(map(lambda c:str(c), cards))

    def __str__(self):
        return f'rank:{self.rank} {self.card_string} {self.hand_type.name}'

    def __repr__(self) -> str:
        return f'Hand {str(self)}'
    
    def __eq__(self, __value: object) -> bool:
        # https://docs.python.org/3.5/library/collections.html#collections.Counter
        return collections.Counter(self.cards) == collections.Counter(__value.cards) 
    
    @staticmethod
    def sort(cards : list[Card]) -> list[Card]:
        return list(sorted(cards, key=lambda c: c.value))

    @staticmethod
    def count_types(cards : list[Card]) -> list[(int, Card)] :
        dic = {}
        for c in cards:
            v = dic.get(c, 0)
            dic[c] = 1 + v
        ls = []
        for c in dic:
            ls.append((dic[c], c))
            
        return list(sorted(ls, key=lambda tup: -1 * tup[0]))

    
    # updated to ignore jokers
    @staticmethod
    def identify_hand(cards : list[Card]) -> HandType:
        counted_cards : list[(int, Card)] = Hand.count_types(cards)
        for i in range(len(counted_cards)):            
            if counted_cards[i][1].name == 'J':
                pass
            elif counted_cards[i][0] == 5:
                return ht_fivekind
            elif counted_cards[i][0] == 4:
                return ht_fourkind
            elif counted_cards[i][0] == 3:
               return ht_house if len(counted_cards) > i+1 and counted_cards[i+1][0] == 2 else ht_threekind
            elif counted_cards[i][0] == 2:
                return ht_twopair if len(counted_cards) > i+1 and counted_cards[i+1][0] == 2 else ht_pair
            elif counted_cards[i][0] == 1:
                return ht_highcard
            else:
                ValueError('Got a hand which is nothing')
        # if here, 5 J
        if counted_cards[0][0] == 5 and counted_cards[0][1].name == 'J':
            return ht_fivekind
        else:
            ValueError('Got a hand which is nothing')
            
    
    @staticmethod
    def second_comp_greater_than(x : list[Card], y : list[Card]) -> bool:
        for (xi, yi) in zip(x, y):
            if xi != yi:
                return xi > yi
        return False
    
    # given start hand-type, apply jokers
    @staticmethod
    def use_jokers(cards:list[Card], ht:HandType) -> HandType:
        jokers = [c for c in cards if c.name == 'J']
        for j in jokers:
            if ht == ht_fivekind:
                break
            ht = ht.with_joker
        return ht
            
    
def sort_hands_cmp(x : Hand, y:Hand) -> int:

    xv = x.hand_type.value 
    yv = y.hand_type.value
    if xv != yv:
        return xv - yv
    for (xc, yc) in zip(x.cards, y.cards):
        if xc.value != yc.value:
            return xc.value - yc.value
    return 0

def sort_hands(hands : list[Hand]) -> list[Hand] :
    return sorted(hands, key=functools.cmp_to_key(sort_hands_cmp))

def rank_hands(hands : list[Card]):
    sorted_hands = sort_hands(hands)
    for (hand, rank) in zip(sorted_hands, range(1, 1+len(sorted_hands))):
        hand.rank = rank

def sum_winnings(hands : list[Hand]) -> int:
    rank_hands(hands)
    sum = 0
    for hand in hands:
        sum += hand.rank * hand.bid
    return sum
        
def parse_hand(str:str) -> Hand:
    space = str.index(' ')
    cards = parse_cards(str[:space])
    bid = int(str[space+1:])
    return Hand(cards, bid)



