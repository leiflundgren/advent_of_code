
from enum import Enum
from typing import Self

class Card:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return self.name

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

card_dict = dict(map(lambda c: (c.name, c), card_types))

def parse_cards(str_cards:str) -> list[Card] :
    return list(map(lambda chr: card_dict[chr], str_cards))
        

class HandType:
    def __init__(self, name:str, value:int):
        self.name = name
        self.value = value
    def __str__(self) -> str:
        return self.name
 
ht_highcard = HandType('HighCard', 1)
ht_pair = HandType('Pair', 2)
ht_twopair = HandType('TwoPair', 3)
ht_threekind = HandType('ThreeOfKind', 4)
ht_house = HandType('FullHouse', 5)
ht_fourkind = HandType('FourOfKind', 6)
ht_fivekind = HandType('FiveOfKind', 7)    
    

hand_types = [
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
        

    def identify_my_hand(self) -> HandType:
        return Hand.identify_hand(self.cards)

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

    
    @staticmethod
    def identify_hand(cards : list[Card]) -> HandType:
        counted_cards : list[(int, Card)] = Hand.count_types(cards)
        if counted_cards[0][0] == 5:
            return ht_fivekind
        elif counted_cards[0][0] == 4:
            return ht_fourkind
        elif counted_cards[0][0] == 3 and counted_cards[1][0] == 2:
            return ht_house
        elif counted_cards[0][0] == 2:
            return ht_twopair if counted_cards[1][0] == 2 else ht_pair
        elif counted_cards[0][0] == 1:
            return ht_highcard
        raise ValueError('Got a hand which is nothing')
    

    def second_comp_greater_than(x : list[Card], y : list[Card]) -> bool:
        for i in range(len(x)):
            xi = x[i]
            yi = y[i]
            if xi != yi:
                return xi > yi
        return False

def parse_hand(str:str) -> Hand:
    space = str.index(' ')
    cards = parse_cards(str[:space])
    bid = int(str[space+1:])
    return Hand(cards, bid)



