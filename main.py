from subpoker.card import Card
from subpoker.deck import Deck
from subpoker.player import Player

Decks = Deck()
Decks.shuffle()

Mark = Player("Mark", 1000)

print(Decks.deal(5))    
