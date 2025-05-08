from subpoker.card import Card
from subpoker.deck import Deck
from subpoker.player import Player
from subpoker.table import Table


deck = Deck().shuffle()

p1= Player("Player 1", 1000)
p2= Player("Player 2", 2000)

players = [p1, p2]

for player in players:
    player.hand = deck.deal(2)

board = deck.deal(5)

for player in players:
    print(f"{player.name}'s hand: {player.hand}")
print(f"Board: {board}")
