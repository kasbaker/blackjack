from random import randint


class Card(object):
    def __init__(self, name: str = "", points: int = 0):
        """Initializes an object representing a card.
        Args:
            name (str): Name of the card
            points (tuple): point values of card, usually (x, x) or could be (1,11) for Aces
        """
        self.name = name
        self.points = points

    def __str__(self):
        """String representation of the card's name and point value"""
        return f"{self.name}"   # : {str(self.points)} points"


class Ace(Card):
    def __init__(self, name: str = "", points: int = 11, alt_points: int = 1):
        """Special instance of a card, with an alternate point value"""
        super().__init__(name=name, points=points)
        self.alt_points = alt_points

    def __str__(self):
        """String representation of an Ace"""
        return f"{self.name}"   # : {str(self.points)} points or {str(self.alt_points)} point"


class Hand(object):
    def __init__(self, cards: list = None, scores: set = None):
        """Initializes an hand for a player
        Args:
            scores (int): point value of the hand
            cards (set): set of cards in the hand
        """
        if cards is None:
            self.cards = list()
            self.scores = [0]
        else:
            self.cards = cards
            self.scores = scores

    def check_bust(self):
        """
        Checks to see if player's hand busts or not, scores should be an empty list if all scores are greater than 21
        :return (bool): True if players hand is a 'bust', False if hand is not a bust
        """
        return self.scores == []

    def __iadd__(self, card: Card):
        """
        Adds two cards together and returns a Hand
        :param card: another card or set of cards to add to this card
        :return: this hand with the new card added to it
        """
        # adds the new card to the hand
        self.cards.append(card)
        # loops through possible point values of the cards in the hand
        for element in enumerate(self.scores):
            # adds the new card's value to each element of this hand's list of values
            self.scores[element[0]] = element[1] + card.points
            # checks if the card is an ace (value == 11)
            if card.points == 11:
                # appends the list with a new possible value of +1 for the ace
                self.scores = self.scores + [element[1] + 1]
        # sort the cards, weed out duplicate values and scores over 21
        self.scores = [score for score in set(self.scores) if score <= 21]
        self.scores.sort(reverse=True)
        return self

    def __str__(self):
        card_names = str()
        for card in self.cards:
            card_names += "\n    " + str(card.name)
        return f"{card_names}"


class Player(object):
    def __init__(self, name: str = "", hand: Hand = None):
        """Initializes a player for the game
        Args:
            name (str): the player's name
            hand (object): the player's hand
        """
        self.name = name
        if hand is None:
            self.hand = Hand()
        else:
            self.hand = hand

        self.choose = True

    def stand(self):
        """Has the player skip their turn instead of accepting another card."""
        print(f"\n{self.name} stands!")
        self.choose = False
        pass

    def hit(self, card: Card):
        """Has the player accept another card
        :arg card: card object dealt by the deck
        """
        print(f"\n{self.name} hits!")
        self. hand += card

    def split(self):
        ...

    def display_hand(self):
        """Displays the players hand"""
        print(f"\n{self.name}'s Hand: {str(self.hand)}")

    def discard_hand(self):
        """Discards the players current hand"""
        self.hand = Hand()

    def __str__(self):
        """"Returns: a string representation of the players name and hand"""
        return f"\nPlayer name: {self.name}"


class Dealer(Player):
    def __init__(self, name: str = "Dealer"):
        """Initializes an automated dealer for blackjack.
        Args:
            name (str): the name of the dealer, which defaults to 'Dealer'"""
        super().__init__(name=name)
        self.hidden_card = ""

    def choose_hit(self):
        """Chooses whether the dealer should hit or not. Dealer will hit on soft 17 and stand on 17 or higher.
        :return (bool) False
        """
        if len(self.hand.scores) > 1 and max(self.hand.scores) == 17:
            #  hit on a 'soft 17'
            return True
        elif max(self.hand.scores) < 17:
            # hit if score is less than 17
            return True
        else:
            # don't hit
            return False

    def hide_card(self):
        """Hides one of the dealer's cards from the user"""
        self.hidden_card = self.hand.cards[0].name
        self.hand.cards[0].name = "**** Hidden Card ****"

    def reveal_card(self):
        self.hand.cards[0].name = self.hidden_card
        """Reveals the dealer's hidden card to the user"""


class User(Player):
    def __init__(self, name: str = "User", money: int = 500):
        """Initializes a player that can be controlled by the user.
        Args:
            name (str): name of the user, defaults ot 'User'
            money (int): number of chips the user has
        """
        super().__init__(name=name)
        self.money = money

    def bet(self, amount: int = 2):
        """Places a bet
        Args:
            amount (int): minimum amount to bet
        """
        if self.money >= amount:
            self.money -= amount
            print(f"{self.name} bets ${amount}")
            return Chip(owner=self, value=amount)
        else:
            print("Not enough money!")
            return None

    def double_down(self):
        ...

    def surrender(self):
        ...

    def insurance(self):
        ...

    def __str__(self):
        """"Returns: a string representation of the players name and hand"""
        return f"\nPlayer name: {self.name}\n    Money: ${self.money}"


class Chip(object):
    def __init__(self, owner: User, value: int = 0):
        """Initializes a chip to bet with."""
        self.value = value
        self.owner = owner
        # self.dealer = dealer

    # an attempt to clean up some code in main program
    # def detect_bust(self):
    #     """Checks to see if someone busts
    #     :return (bool): True if """
    #     if self.owner.hand.check_bust() and self.dealer.hand.check_bust():
    #         print(f"{self.owner.name} BUST! {self.dealer.name} BUST!")
    #         self.settle_bets('lose')
    #         return True
    #     elif self.owner.hand.check_bust():
    #         print(f"{self.owner.name} BUST!")
    #         self.settle_bets('lose')
    #         return True
    #     elif self.dealer.hand.check_bust():
    #         print(f"{self.dealer.name} BUST!")
    #         self.settle_bets('win')
    #         return True
    #     else:
    #         return False
    #
    # def decide_winner(self, dealer: Dealer, user: User):
    #     user_score = max(user.hand.scores)
    #     dealer_score = max(dealer.hand.scores)
    #     if user_score > dealer_score:
    #         print(f"{user.name} wins with {user_score}")
    #         self.settle_bets('win')
    #     elif user_score < dealer_score:
    #         print(f"{dealer.name} wins with {dealer_score}")
    #         self.settle_bets('lose')
    #     else:
    #         print(f"{user.name} ties with {user_score}")
    #         self.settle_bets('push')

    def settle_bets(self, status: str = 'push'):
        """
        Gives or takes chips from players depending on game results.
        """
        if status == 'win':
            print(f"{self.owner.name} wins ${self.value}!")
            self.owner.money += 2*self.value
        elif status == 'lose':
            print(f"{self.owner.name} loses ${self.value}!")
            pass
        else:
            print(f"{self.owner.name} pushes. Money is returned!")
            self.owner.money += self.value
        self.value = 0

    def __str__(self):
        """String representation of chip's value and owner"""
        return f"{self.owner.name}'s bet: ${str(self.value)}"


class Deck(object):
    """A standard deck of 52 playing cards, joker removed"""
    standard_deck = [Ace("Ace of Spades", 11, 1),
                     Card("Two of Spades", 2), Card("Three of Spades", 3), Card("Four of Spades", 4),
                     Card("Five of Spades", 5), Card("Six of Spades", 6), Card("Seven of Spades", 7),
                     Card("Eight of Spades", 8), Card("Nine of Spades", 9), Card("Ten of Spades", 10),
                     Card("Jack of Spades", 10), Card("Queen of Spades", 10), Card("King of Spades", 10),
                     Ace("Ace of Hearts", 11, 1),
                     Card("Two of Hearts", 2), Card("Three of Hearts", 3), Card("Four of Hearts", 4),
                     Card("Five of Hearts", 5), Card("Six of Hearts", 6), Card("Seven of Hearts", 7),
                     Card("Eight of Hearts", 8), Card("Nine of Hearts", 9), Card("Ten of Hearts", 10),
                     Card("Jack of Hearts", 10), Card("Queen of Hearts", 10), Card("King of Hearts", 10),
                     Ace("Ace of Clubs", 11, 1),
                     Card("Two of Clubs", 2), Card("Three of Clubs", 3), Card("Four of Clubs", 4),
                     Card("Five of Clubs", 5), Card("Six of Clubs", 6), Card("Seven of Clubs", 7),
                     Card("Eight of Clubs", 8), Card("Nine of Clubs", 9), Card("Ten of Clubs", 10),
                     Card("Jack of Clubs", 10), Card("Queen of Clubs", 10), Card("King of Clubs", 10),
                     Ace("Ace of Diamonds", 11, 1),
                     Card("Two of Diamonds", 2), Card("Three of Diamonds", 3), Card("Four of Diamonds", 4),
                     Card("Five of Diamonds", 5), Card("Six of Diamonds", 6), Card("Seven of Diamonds", 7),
                     Card("Eight of Diamonds", 8), Card("Nine of Diamonds", 9), Card("Ten of Diamonds", 10),
                     Card("Jack of Diamonds", 10), Card("Queen of Diamonds", 10), Card("King of Diamonds", 10)]

    def __init__(self, cards: list = None):
        """Initializes a deck of cards to play with
        :param cards: a standard deck of 52 playing cards
        """
        if cards is None:
            self.cards = self.standard_deck.copy()
        else:
            self.cards = cards

    def deal(self):
        """
        Deals a random card to a selected player and removes it from the deck
        :return: a random Card to be added to the player's hand
        """
        if len(self.cards) > 0:
            return self.cards.pop(randint(0, len(self.cards) - 1))
        else:
            print("Out of cards!")
            return None

    def shuffle(self):
        """Restores all the cards to the deck"""
        print("Shuffling the deck!")
        self.cards = self.standard_deck.copy()

    def deal_hands(self, dealer: Dealer, user: User):
        user.hand += self.deal()
        user.hand += self.deal()
        dealer.hand += self.deal()
        dealer.hand += self.deal()
        dealer.hide_card()
