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
        print("TEST 1\r\n=================")
        hands = create_hands()
        self.assertEqual(765, hands[0].bid)
        self.assertEqual('3', hands[0].cards[0].name)
        self.assertEqual(card.ht_pair, hands[0].hand_type)

        self.assertEqual(684, hands[1].bid)
        self.assertEqual('T', hands[1].cards[0].name)        
        self.assertEqual(card.ht_fourkind, hands[1].hand_type)

        self.assertEqual(28, hands[2].bid)
        self.assertEqual('K', hands[2].cards[0].name)        
        self.assertEqual(card.ht_twopair, hands[2].hand_type)
    
        self.assertEqual(220, hands[3].bid)
        self.assertEqual('K', hands[3].cards[0].name)        
        self.assertEqual(card.ht_fourkind, hands[3].hand_type)

        self.assertEqual(483, hands[4].bid)
        self.assertEqual('Q', hands[4].cards[0].name)        
        self.assertEqual(card.ht_fourkind, hands[4].hand_type)

        sorted_hands = card.sort_hands(hands)
        print("Sorted:")
        card.rank_hands(hands)
        for hand in sorted_hands:
            print(hand)

        print()
        print("Ranked:")
        for hand in hands:
            winning = hand.rank * hand.bid
            print(f'{hand} win:{winning}')
                       
    def test_currated(self):
        print("TEST 2\r\n=================")
        hands = list(map(
            lambda s: card.parse_hand(s), [
                '2345A 1',
                'Q2KJJ 13',
                'Q2Q2Q 19',
                'T3T3J 17',
                'T3Q33 11',
                '2345J 3',
                'J345A 2',
                '32T3K 5',
                'T55J5 29',
                'KK677 7',
                'KTJJT 34',
                'QQQJA 31',
                'JJJJJ 37',
                'JAAAA 43',
                'AAAAJ 59',
                'AAAAA 61',
                '2AAAA 23',
                '2JJJJ 53',
                'JJJJ2 41'
            ]))
        
        expected_order = list(map(
            lambda s: card.parse_hand(s), [
                '2345A 1',
                'J345A 2',
                '2345J 3',
                '32T3K 5',
                'KK677 7',
                'T3Q33 11',
                'Q2KJJ 13',
                'T3T3J 17',
                'Q2Q2Q 19',
                '2AAAA 23',
                'T55J5 29',
                'QQQJA 31',
                'KTJJT 34',
                'JJJJJ 37',
                'JJJJ2 41',
                'JAAAA 43',
                '2JJJJ 53',
                'AAAAJ 59',
                'AAAAA 61'
            ]))
        
        for (i, h) in zip(range(1, 1+len(expected_order)), expected_order):
            h.rank = i
        sorted_hands = card.sort_hands(hands)
        print("Sorted:")
        card.rank_hands(hands)
        for hand in sorted_hands:
            winning = hand.rank * hand.bid
            print(f'{hand} win:{winning}')

        print("========\r\nExpected:")
        for hand in expected_order:
            winning = hand.rank * hand.bid
            print(f'{hand} win:{winning}')
        b = expected_order[0] == sorted_hands[0]
        self.assertEqual(expected_order[0], sorted_hands[0])
        self.assertListEqual(expected_order, sorted_hands)

        winnings = card.sum_winnings(hands)
        self.assertEqual(6839, winnings)

if __name__ == '__main__':
    unittest.main()
    
