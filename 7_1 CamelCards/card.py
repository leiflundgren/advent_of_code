
from enum import Enum
from typing import Self

class Card:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
card_types = [
    Card('A', 14),
    Card('K', 13),
    Card('Q', 12),
    Card('J', 11),
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

class HandType:
    def __init__(self, name, value):
        self.name = name
        self.value = value

        
    def count_types(self, card: list[Card]) -> list[(int, Card)] :
        dic = {}
        for c in card:
            dic[c] = 1 if not dic.has_key(c) else 1 + dic[c]
        ls = []
        for c in dic:
            ls.append((dic[c], c))
            
        return list(sorted(ls, key=lambda tup: tup[0]))

 
ht_highcard = HandType('HighCard', 1),
ht_pair = HandType('Pair', 2),
ht_twopair = HandType('TwoPair', 3),
ht_threekind = HandType('ThreeOfKind', 4),
ht_house = HandType('FullHouse', 5),
ht_fourkind = HandType('FourOfKind', 6),
ht_fivekind = HandType('FiveOfKind', 7),    
    

hand_types = [
    ht_highcard,
    ht_pair,
    ht_twopair,
    ht_threekind,
    ht_house,
    ht_fourkind,
    ht_fivekind,       
]

class Cards:
    def __init__(self):
        pass        

    @staticmethod
    def sort(cards : list[Card]) -> list[Card]:
        return list(sorted(cards, key=lambda c: c.value))
    
    @staticmethod
    def identity_hand_type(counted_cards : list(int, Card)) -> HandType:
        if counted_cards[0][0] == 5:
            return ht_fivekind
        elif counted_cards[0][0] == 4:
            return ht_fourkind
        elif counted_cards[0][0] == 3 and counted_cards[1][0] == 2:
            return ht_house
        elif counted_cards[0][0] == 2:
            return ht_pair
        elif counted_cards[0][0] == 1:
            return ht_highcard
        raise ValueError('Got a hand which is nothing')
    

    s
