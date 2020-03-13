import unittest
import blackjack
from lib import blackjack_lib as bj

ace = bj.Ace(name="Ace of Spades")
jack = bj.Card(name="Jack of Diamonds", points=10)
two = bj.Card(name="Two of Clubs", points = 2)


class TestBlackjackLib(unittest.TestCase):
    def test_chip(self):
        chip = bj.Chip(value=250)
        print(chip)

    def test_ace(self):
        # card = bj.Ace(name="Ace of Spades")
        card = ace
        print(card)

    def test_card(self):
        # card = bj.Card(name="Jack of Diamonds", points=10)
        card = jack
        print(card)

    def test_hand(self):
        hand = bj.Hand()
        print(hand.cards)
        print(hand.scores)

    def test_hand(self):
        hand = bj.Hand()
        # hand += jack
        # hand += jack
        # hand += jack
        hand += ace
        hand += ace
        hand += ace
        # hand += jack
        hand += two
        hand += two
        hand += two
        hand += two
        # hand += ace
        # hand += ace
        # self.assertEqual(hand.scores, [10])
        # for card in hand.cards:
        #     print(card)
        print(hand)
        self.assertEqual(hand.check_bust(), False)

    def test_deck(self):
        deck = bj.Deck()
        for num in range(54):
            print(f"\nDeck size before draw: {len(deck.cards)}")
            print(deck.deal())
            print(f"Deck size after draw: {len(deck.cards)}")
        deck.shuffle()
        print(f"Deck size after shuffle: {len(deck.cards)}")
        print(deck.deal())
        print(len(deck.cards))

    def test_user(self):
        user = bj.User(name="Katie")
        user.hand += ace
        user.hand += jack
        user.display_hand()
        print(user)
        user_chip = user.bet(200)
        print(user)

    def test_dealer(self):
        dealer = bj.Dealer()
        print(dealer)
        dealer.hand += ace
        dealer.hand += jack
        dealer.hide_card()
        dealer.display_hand()
        dealer.reveal_card()
        dealer.display_hand()

    def test_bets(self):
        user = bj.User(name="Katie")
        print(user)
        user_chip = user.bet(200)
        print(user)
        user_chip.settle_bets('push')
        print(user)
        user_chip = user.bet(100)
        user_chip.settle_bets('win')
        print(user)
        user_chip = user.bet(300)
        user_chip.settle_bets('lose')
        print(user)

    def test_deal_cards(self):
        deck = bj.Deck()
        user = bj.User(name="Katie")
        dealer = bj.Dealer()
        deck.deal_hands(dealer, user)


if __name__ == "__main__":
    unittest.main()