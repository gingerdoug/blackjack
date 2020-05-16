# IMPORT STATEMENTS AND VARIABLE DECLARATIONS:

# from IPython.display import clear_output -- only works in jupyter
import random
import itertools

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

#CLASS DEFINITIONS:

class Card:
    
    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit
        
    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

        ''' alternatively can use
        for t in list(itertools.product(suits,ranks)):
            self.deck.append(Card(t[0], t[1]))
        '''
        
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += "\n " + card.__str__()
        return "the deck has: " + deck_comp
        
    def shuffle(self): 
        random.shuffle(self.deck)
    
    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:
    
    def __init__(self):
        self.cards = []  
        self.value = 0
        self.aces = 0
        
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
                self.aces += 1
        
    def adjust_for_aces(self):
        while self.value >21 and self.aces >0:
            self.value -= 10
            self.aces -= 1
            
class Chips:
    
    def __init__(self, total = 100):
        self.total = total
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
        
        
    def lose_bet(self):
        self.total -= self.bet
    # add something here to tell the player when they've lost everything and give option to buy back in...

#FUNCTION DEFINITIONS:

def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input("Enter bet amount: "))
        except ValueError: 
            print("please enter a number")
        else:
            if chips.bet > chips.total:
                print(f"Sorry, your bet can't exceed {chips.total}")
            else:
                break

def twist(deck, hand):
    
    #create and add card to hand
    hand.add_card(deck.deal())
    hand.adjust_for_aces()
        

def stick_or_twist(deck, hand):
    
    global playing
    
    while True:
       
        x = input("Stick or twist? s/t ")
    
        if x[0].lower() == "t":
                twist(deck, hand)
                
        elif x[0].lower() == "s":
                print("player is sticking. Dealer to play")
                playing = False
               
        else:
            print("please enter a valid response")
            continue
        break
        
def show_some(player, dealer):

    #player and dealer will both be objects of class Hand. hand.cards is a list with 2 items to begin with
    print("\nDealer's cards: ")
    print("\n<card hidden>")
    print(dealer.cards[1])
    
    print("\nPlayer's cards: \n")
    for card in player.cards:
        print(card)   
    #print('\033[1m',"\nHand value = ", player.value, '\033[0m') -- if want the hand value in bold 

def show_all(player, dealer):
    
    print("\nDealer's cards: ")
    for card in dealer.cards:
        print(card)
    print(dealer.value)
    
    print("\nPlayer's cards: \n")
    for card in player.cards:
        print(card)
    print(player.value)    

def player_busts(player, dealer, chips):
    #if player.value exceeds 21, then they're bust
    print("\nPlayer is bust, bet lost")
    chips.lose_bet()
        
def player_wins(player, dealer, chips):
    #if player.value > dealer.value and <21 then player wins
    print("\nPlayer wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    #if dealer.value exceeds 21, they're bust
    print("\nDealer busts")
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    #if dealer.value > player.value and is <21
    print("\nDealer wins")
    chips.lose_bet()
    
def tie(player, dealer):
    #if dealer.value == player.value, it's a tie and player get's their bet back
    print("\nit's a tie")



#GAMEPLAY:

# Print an opening statement
print("\nWelcome to Blackjack, enjoy responsibly")

while True:

    try: 
        chip_total_input = int(input("Please specify your starting chip stack as a numeric value: "))
    except: 
        print("please enter a number")
    else: 
        if chip_total_input <= 0:
            print("\nYou can't play without money in this casino buddy\n ")
            continue
        break

player_chips = Chips(chip_total_input)
print(f"Your starting chip stack is {player_chips.total} ")

while True:
    

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    
    player = Hand()
    dealer = Hand()
    player.add_card(deck.deal())
    dealer.add_card(deck.deal()) 
    player.add_card(deck.deal())
    dealer.add_card(deck.deal()) 
    

    # Prompt the Player for their bet
    print(f"\nYou have {player_chips.total} chips\n")
    take_bet(player_chips)
    
    #clear_output() -- only works in jupyter
    
    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)
    
    
    while playing:  # recall this variable from our hit_or_stand function
        
        
        # Prompt for Player to Hit or Stand. If they choose to stick then playing = False so while-loop breaks
        stick_or_twist(deck, player)
        #clear_output() -- only works in jupyter
        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            player_busts(player, dealer, player_chips)
            break
        
            
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 
    if player.value <= 21:
        
        #clear_output() -- only works in jupyter
        
        while dealer.value < 17:
            twist(deck, dealer)
             
                
        show_all(player,dealer)
            
        if dealer.value > 21:
            dealer_busts(dealer, player, player_chips)
            
        elif player.value > dealer.value:
            player_wins(player, dealer, player_chips)
            
        elif player.value < dealer.value:
            dealer_wins(player, dealer, player_chips)
            
        else:
            tie(player, dealer)
    
    print(f"chip balance is now {player_chips.total}")
        
    replay = input("Would you like to play again? y/n ")
        
    if replay[0].lower() == "y":
        if player_chips.total == 0:

            while True:

                buy_in = input("You've run out of chips, want to buy back in? y/n ")

                if buy_in[0].lower() == "y":
                    while True:

                        try: 
                            buy_back_input = int(input("how many chips do you want to buy: "))
                        except: 
                            print("please enter a number")
                        else: 
                            if buy_back_input <= 0:
                                print("\nYou can't play without money in this casino buddy\n ")
                                continue
                            else:
                                player_chips.total = buy_back_input
                                break
                    break
                elif buy_in[0].lower() == "n":
                    playing = False
                    break
                else:
                    print("please enter a valid response")
                    continue  
            
      
    elif replay[0].lower() == "y" and player_chips.total > 0 :
            playing = True
            #clear_output() -- only works in jupyter
            continue 
    else:
        print("thanks for playing!")
        break
        
