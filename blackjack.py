from random import randint 
from itertools import  product

class Deck():
    
    def __init__(self,index_list =None):
        self.index_list = []
  
    def draw_card(self):
        ranks_values = [('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), 
                    ('8', 8), ('9', 9), ('T', 10),
                     ('J', 10), ('Q', 10), ('K', 10), ('A', 11)]
        suits = 'CDHS'
        ranks = '23456789TJQKA'
        deck_of_cards = [''.join(card) for card in product(ranks, suits)]
        
        while True:
            index = randint(0,51)
            if index not in self.index_list:
                self.index_list.append(index)
                current_drawn_card = deck_of_cards[index]
                current_card_rank = (deck_of_cards[index])[0]
                for i in ranks_values:
                    if current_card_rank == i[0]:
                        current_card_value = i[1]
                break
        return (current_drawn_card, current_card_value)
        

            
    
class Hand():
    def __init__(self):
        self.cards = []
        self.values = []
        self.valid_moves = []
                
    def add_card(self, card_value):
        self.cards.append(card_value[0])
        self.values.append(card_value[1])
        self._valid_moves()
                
    def _valid_moves(self):
        moves = ['stay']
        
        if len(self.cards) <= 2:
            if sum(self.values)<=11:
                moves.append('double')

        if len(self.cards) == 2:
            if sum(self.values) == 21:
                self.valid_moves = 'Blackjack'
                return
                
        if sum(self.values) > 21:
            for i in range(len(self.values)):           
                if self.values[i]==11:
                    self.values[i] = 1
                    if sum(self.values) > 21:
                        self.valid_moves = 'Bust'
                        return
                    moves.append('hit')
                    self.valid_moves = moves
                    return
            self.valid_moves = 'Bust'
            return
            
        moves.append('hit')
        self.valid_moves = moves
        
    
class Player():
    def __init__(self, chips=1000):
        self.chips = chips
        
    def place_bet(self):
        print ('Chips: ', (self.chips))
        bet = input("Place your bet. It must be an interger. ('q' to quit): ")
        if bet == 'q':
            return bet

        while True:
            try:
                bet = int(bet)
                if bet < 1:
                    bet = int(input('Bet must be at least 1. Try again: '))
                elif self.chips - bet < 0:
                    bet = int(input('Not enough chips. Try again: '))
                else:
                    break
            except:
                bet = input('Not a valid bet. Try again: ')
        self.chips -= bet
        return bet
  

class Game():
       
    def __init__(self):
        self.player = Player()
                       
    def play(self):
        print("WELCOME TO BLACKJACK")
        while True:
            if (self.player.chips<=0):
                print("You don't have any more chips to play")
                break
            print("\n*****Starting a new game*****")
            print("Ranks = 23456789TJQKA | Suits = 'CDHS'")
            self.dealer_cards = Hand()
            self.player_cards = Hand()
            self.deck = Deck()
            bet = self.player.place_bet()
            if bet == 'q':
                print ('Thanks for playing')
                break
            for _ in range(2):
                self.dealer_cards.add_card(self.deck.draw_card())
                self.player_cards.add_card(self.deck.draw_card())
            print('Player Cards: ', self.player_cards.cards)
            print('Dealer Cards: ', self.dealer_cards.cards[0])
                        
            while True:
                if (self.player_cards.valid_moves == 'Blackjack'):
                    self.player.chips += 2*bet
                    print(self.player.chips)
                    print('Yay Blackjack')
                    user_input = 'BlackJack'
                    break
                if(self.player_cards.valid_moves == 'Bust'):
                    print('You got Busted')
                    break
                while True:
                    if(sum(self.player_cards.values) == 21):
                        user_input = 'stay'
                        break
                    else:
                        print('\nValid Moves: ', self.player_cards.valid_moves, end = '')
                        user_input =input('Please enter one of the above displayed\nValid Moves without quotes(eg. stay): ').lower()
                        if user_input in  self.player_cards.valid_moves:
                            break
                
                if user_input == 'stay':
                    break
                if user_input == 'hit':
                    self.player_cards.add_card(self.deck.draw_card())
                    print('Player Cards: ', self.player_cards.cards)
                    
                if user_input == 'double':
                    self.player.chips-=bet
                    bet = 2*bet
                    self.player_cards.add_card(self.deck.draw_card())
                    print('Player Cards: ', self.player_cards.cards)
                    
            if user_input == 'stay':
                while True:
                    if self.dealer_cards.valid_moves == "Bust":
                        print("\nDealer got Busted")
                        self.player.chips += 2*bet
                        break
                    elif sum(self.dealer_cards.values)>=17:
                        if sum(self.dealer_cards.values) < sum(self.player_cards.values):
                            print("\nYou won")
                            self.player.chips += 2*bet
                            break
                        elif sum(self.dealer_cards.values) > sum(self.player_cards.values):
                            print("\nYou lost")
                            break
                        else:
                            print("\nIt is a draw")
                            self.player.chips += bet
                            break
                    else:
                        self.dealer_cards.add_card(self.deck.draw_card())
                print('Dealer Cards: ', self.dealer_cards.cards)
                
    
if __name__ == '__main__':
    x = Game()
    x.play()   
