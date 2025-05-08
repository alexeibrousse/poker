from subpoker.card import Card
from subpoker.deck import Deck
from subpoker.player import Player
from subpoker.table import Table
from subpoker.game import Game

p1= Player("Player 1", 1000)
p2= Player("Player 2", 2000)

players = [p1, p2]

game = Game(players, 10)

game.start_round()
game.deal_flop()
game.betting_round()
