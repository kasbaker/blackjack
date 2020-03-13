"""A Blackjack game with an automated dealer"""
from lib import blackjack_lib as bj


def main():
    """Main program"""
    # initializing deck and dealer
    deck = bj.Deck()
    dealer = bj.Dealer()

    game_over = False

    print("\nWelcome to Blackjack!")

    # Prompt for user to input their name and initialize user
    user = bj.User(name=input("\nPlease enter your name: "))
    user_chip = None

    play = True
    while play:

        if game_over:
            # Showing game results
            print("\nGame over! Here's what the dealer had:")
            dealer.reveal_card()
            dealer.display_hand()
            user.display_hand()
            input("\n....Press Enter to start a new game....\n")
            print("\n"*100)

            # Resetting things
            deck.shuffle()
            print("----------New Game----------")
            user.discard_hand()
            dealer.discard_hand()
            user_chip = None
            user.choose = True
            dealer.choose = True
            game_over = False
        else:
            pass

        print(user)

        while user_chip is None:
            try:
                amount = int(input("\nPlease input the amount you would like to bet: "))
                user_chip = user.bet(amount=amount)
            except ValueError:
                print("Error - please enter an integer")
                continue
        input("\n....Press Enter to continue....\n")

        deck.deal_hands(dealer=dealer, user=user)

        while not game_over:
            print("\n"*100)
            # displaying hands
            dealer.display_hand()
            user.display_hand()

            # ask the user what to do if they haven't already chose to stand
            if user.choose:
                while True:
                    response = input("\nWhat would you like to do? You can type 'hit' or 'stand' ").lower()
                    if response == 'hit':
                        user.hit(deck.deal())
                        print(f"{str(user.name)} receives: {str(user.hand.cards[-1])}")
                        break
                    elif response == 'stand':
                        user.stand()
                        break
                    else:
                        print(f"I'm sorry {user.name}, you can't do that.\n")
                        dealer.display_hand()
                        user.display_hand()
                        continue
            else:
                pass

            # ask the dealer what to do if they haven't already chose to stand
            if dealer.choose:
                if dealer.choose_hit():
                    dealer.hit(deck.deal())
                    print(f"{str(dealer.name)} receives: {str(dealer.hand.cards[-1])}")
                else:
                    dealer.stand()

            input("\n....Press Enter to continue....\n")

            if user.hand.check_bust() and dealer.hand.check_bust():
                print(f"{user.name} BUST! {dealer.name} BUST!")
                user_chip.settle_bets('lose')
                game_over = True
            elif user.hand.check_bust():
                print(f"{user.name} BUST!")
                user_chip.settle_bets('lose')
                game_over = True
            elif dealer.hand.check_bust():
                print(f"{dealer.name} BUST!")
                user_chip.settle_bets('win')
                game_over = True
            else:
                pass

            if not user.choose and not dealer.choose:
                user_score = max(user.hand.scores)
                dealer_score = max(dealer.hand.scores)
                if user_score > dealer_score:
                    print(f"{user.name} wins with {user_score}")
                    user_chip.settle_bets('win')
                elif user_score < dealer_score:
                    print(f"{dealer.name} wins with {dealer_score}")
                    user_chip.settle_bets('lose')
                else:
                    print(f"{user.name} ties with {user_score}")
                    user_chip.settle_bets('push')
                game_over = True
            else:
                continue


if __name__ == "__main__":
    main()
