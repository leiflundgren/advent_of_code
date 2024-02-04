import unittest
import card

unittest.TestLoader.sortTestMethodsUsing = None

def create_hands():
    return list(map(
        lambda s: card.parse_hand(s), [
            '32T3K 765',
            'T55J5 684',
            'KK677 28',
            'KTJJT 220',
            'QQQJA 483'
        ]))


    
class Tests(unittest.TestCase):
    def test_basics(self):
        hands = create_hands()
        self.assertEqual(765, hands[0].bid)
        self.assertEqual('3', hands[0].cards[0].name)
        self.assertEqual(card.ht_pair, hands[0].hand_type)

        self.assertEqual(684, hands[1].bid)
        self.assertEqual('T', hands[1].cards[0].name)        
        self.assertEqual(card.ht_threekind, hands[1].hand_type)

        self.assertEqual(28, hands[2].bid)
        self.assertEqual('K', hands[2].cards[0].name)        
        self.assertEqual(card.ht_twopair, hands[2].hand_type)
    
        self.assertEqual(220, hands[3].bid)
        self.assertEqual('K', hands[3].cards[0].name)        
        self.assertEqual(card.ht_twopair, hands[3].hand_type)

        self.assertEqual(483, hands[4].bid)
        self.assertEqual('Q', hands[4].cards[0].name)        
        self.assertEqual(card.ht_threekind, hands[4].hand_type)

        sorted_hands = card.sort_hands(hands)
        print("Sorted:")
        for hand in sorted_hands:
            print(hand)

        print()
        print("Ranked:")
        card.rank_hands(hands)
        for hand in hands:
            winning = hand.rank * hand.bid
            print(f'{hand} win:{winning}')
                       
        winnings = card.sum_winnings(hands)
        self.assertEqual(6440, winnings)

if __name__ == '__main__':
    unittest.main()
    
