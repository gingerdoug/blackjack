import random
import itertools

SUITS = ("Hearts", "Diamonds", "Spades", "Clubs")

VALUES = {
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
    "Six": 6,
    "Seven": 7,
    "Eight": 8,
    "Nine": 9,
    "Ten": 10,
    "Jack": 10,
    "Queen": 10,
    "King": 10,
    "Ace": 11,
}

RANKS = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)


class Game:
    """
    Blackjack game, allowing player to play multiple hands vs. dealer

    Attributes:
        chip_balance (int): chips purchased
        current_bet (int): amount currently wagering
        dealer_stick_threshold (int): dealer card total where they always stick

    Methods:
        take_bet (bet_size): Takes a wager from player, and shuffles and deals deck
        play_hand: Plays out hand, with player & dealer drawing cards and then resolving bet payoffs
    """

    def __init__(self, chip_balance, dealer_stick_threshold=17):
        assert chip_balance > 0
        self.chip_balance = chip_balance
        self.current_bet = 0
        self.dealer_stick_threshold = dealer_stick_threshold

    def take_bet(self, bet_amount):
        """
        Takes wager from player
        decreasing chip balance by bet amount
        & deals and shows cards to player

        Args:
            bet_amount (int): amount to bet 
        """
        self.current_bet = bet_amount
        self.chip_balance -= bet_amount
        self._deal_new_hand()
        self._show_cards()

    def play_hand(self):
        """
        Plays out hand:
            - prompting player to make choices (stick/twist)
            - finding dealer choices (stick/twist)
            - finding hand outcome (dealer/player wins, or tie)
        """
        self._get_player_outcome()
        self._get_dealer_outcome()
        self._find_hand_outcome()
        self._show_cards(dealer_partly_hidden=False)

    def _deal_new_hand(self):
        """
        Deals out hand:
            - shuffling deck
            - giving both players two cards
            - revealing 2 player cards, and one dealer card
        """
        self.deck = list(itertools.product(SUITS, RANKS))
        random.shuffle(self.deck)
        player_hand = []
        dealer_hand = []
        for card in range(2):
            player_hand = self._draw_card(player_hand)
            dealer_hand = self._draw_card(dealer_hand)
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.player_has_stuck = False
        self.player_is_bust = False

    def _show_cards(self, dealer_partly_hidden=True):
        """
        Reveals cards (all of players and some/all of dealer)

        Args:
            dealer_partly_hidden (bool): show one/all of dealers cards
        """
        print("\nDealer's cards: ")
        if dealer_partly_hidden:
            print("\n<card hidden>")
            print(self.dealer_hand[1])
        else:
            for c in self.dealer_hand:
                print(c)
        print("\nPlayer's cards: \n")
        for c in self.player_hand:
            print(c)

    def _get_player_outcome(self):
        """
        Repeatedly ask player to stick/twist, keeping track of hand total, and is-bust
        """
        while self.player_has_stuck == False and self.player_is_bust == False:
            self._stick_or_twist()
            self.player_hand_total = self._get_hand_total(self.player_hand)
            self.player_is_bust = self._get_hand_total(self.player_hand) > 21

    def _get_dealer_outcome(self):
        """
        Repeatedly twisting for dealer until hand_total >= stick_threshold
        """
        self.dealer_hand_total = 0
        if self.player_is_bust == False:
            self.dealer_hand_total = self._get_hand_total(self.dealer_hand)
            dealer_has_stuck = self.dealer_hand_total > min(
                self.dealer_stick_threshold, self.player_hand_total
            )
            while dealer_has_stuck == False:
                self.dealer_hand = self._draw_card(self.dealer_hand)
                dealer_hand_total = self._get_hand_total(self.dealer_hand)
                dealer_has_stuck = dealer_hand_total > min(
                    self.dealer_stick_threshold, self.player_hand_total
                )

    def _draw_card(self, hand):
        """
        Adds top card from 'deck' to hand  

        Args:
            hand (list): hand before drawn

        Returns:
            hand (list): hand after drawn
        """
        hand.append(self.deck.pop())
        return hand

    def _stick_or_twist(self):
        """
        Prompts the player with stick/twist choice

        If chooses stick, switch to dealers' choice, else draw another card and repeat 
        """
        twist_choice = get_yes_no_input("Would you like to twist y/n? \n")
        if twist_choice:
            self.player_hand = self._draw_card(self.player_hand)
            self._show_cards()
            return self.player_hand
        else:
            print("player is sticking. Dealer to play")
            self.player_has_stuck = True
            return self.player_hand

    def _find_hand_outcome(self):
        """
        Checks if player/dealer has one, updating chip_balance and pringing outcome to player
        """
        print("\n**********************")
        if self.player_is_bust:
            # if player.value > dealer.value and <21 then player wins
            print("Player bust, dealer wins!")
        elif self.dealer_hand_total > 21 or (
            self.dealer_hand_total < self.player_hand_total
        ):
            print("Player wins!")
            self.chip_balance += self.current_bet * 2
        elif self.dealer_hand_total > self.player_hand_total:
            # if dealer.value exceeds 21, they're bust
            print("Dealer wins")
        elif self.dealer_hand_total == self.player_hand_total:
            print("Tie")
            self.chip_balance += self.current_bet * 2
        print("**********************")

    def _get_hand_total(self, hand):
        """
        Finds total of hand (sum of card values, less 10 if hand contains ace & total > 21)

        Args:
            hand (list): hand of cards (list of tuples)

        Returns:
            total (int): hand total
        """
        card_ranks = [card[1] for card in hand]
        hand_total = sum(VALUES[rank] for rank in card_ranks)
        for c in card_ranks:
            if c == "Ace" and hand_total > 21:
                hand_total -= 10
        return hand_total


def get_numeric_input(message, min=0, max=0):
    """
    Prompts with 'message' and returns numeric input provided
    Retries if invalid input

    Args:
        message (string): prompt message
        min (numeric): minimum valid input
        max (numeric): maximum valid input

    Returns:
        numeric_input (int): number provided
    """
    while True:
        try:
            numeric_input = int(input(message))
            assert numeric_input > min and numeric_input < max
            return numeric_input
        except:
            print(f"please enter a number, between {min}-{max}")


def get_yes_no_input(message):
    """
    Prompts with 'message' and returns boolean of y/n response
    Retries if invalid input

    Args:
        message (string): prompt message

    Returns:
        response (boolean): was response 'y'?
    """
    while True:
        try:
            response = input(message)
            assert len(response) > 0 and response[0].lower() in ["y", "n"]
            return response[0].lower() == "y"
        except:
            print("please enter valid input y/n")


def main():
    """
    Game loop

    (1) gets input on starting stack and initialises new blackjack game
    (2) takes multiple betting rounds, prompting if player wishes to continue, and propting for redeposit if balance 0 
    """
    print("\nWelcome to Blackjack, enjoy responsibly")
    starting_stack = get_numeric_input("Please enter your starting stack \n", min=1)
    game = Game(chip_balance=starting_stack)
    while True:
        bet = get_numeric_input(
            "Please place your bet \n", min=1, max=game.chip_balance
        )
        game.take_bet(bet)
        game.play_hand()
        print(f"Chip balance {game.chip_balance}")
        if game.chip_balance == 0:
            if get_yes_no_input("Would you like to deposit more? \n"):
                game.chip_balance += get_numeric_input(
                    "How much would you like to deposit? \n"
                )
        play_again = get_yes_no_input("Would you like to play again? \n")
        if not play_again:
            break


if __name__ == "__main__":
    main()
