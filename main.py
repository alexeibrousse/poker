from subpoker.card import Card
from subpoker.deck import Deck
from subpoker.player import Player
from subpoker.table import Table
from subpoker.game import Game

p1= Player("Player 1", 1000)
p2= Player("Player 2", 2000)
p3= Player("Player 3", 2000)

game = Game([p1, p2, p3], 10)

game.run_game()
