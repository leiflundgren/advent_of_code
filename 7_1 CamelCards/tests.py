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
        hand_type = hands[0].identity_my_hand()
        self.assertEqual(card.ht_pair, hand_type)

    


 
if __name__ == '__main__':
    unittest.main()
    
