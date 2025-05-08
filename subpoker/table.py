from .deck import Deck
from .player import Player

class Table():
    def __init__(self, players: list):
        self.players = players
        self.deck = Deck().shuffle()
        self.board = []
        self.pot = 0
    
    def reset(self):
        self.deck.reset().shuffle()
        self.board = []
        self.board = []
        self.pot = 0
        for player in self.players:
            player.reset()
    
    def deal_private(self):
        for player in self.players:
            player.hand = self.deck.deal(2)

    def deal_board(self, num:int):
        self.board.extend(self.deck.deal(num))
        return self.board

    def add_to_pot(self, amount: int):
        for player in self.players:
            if player.bet > 0:
                self.pot += player.bet
                player.bet = 0
        return self.pot
    
