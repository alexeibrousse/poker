from .card import Card
import random

class Deck:
    def __init__(self):
        self.cards = []
        for suit in Card.suits:
            for rank in Card.ranks:
                self.cards.append(Card(rank, suit))
    
    def __len__(self):
        return len(self.cards)
    
    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self,position: int):
        return self.cards[position]
    
    def __str__(self):
        return f"({self.cards})"
    
    def __repr__(self):
        return f"Deck with {len(self.cards)} cards: ({self.cards})"

    def shuffle(self): 
        random.shuffle(self.cards)
        return self
    
    def sort(self):
        self.cards.sort()
        return self

    def reset(self):
        self.cards = []
        for suit in Card.suits:
            for rank in Card.ranks:
                self.cards.append(Card(rank, suit))
        return self

    def deal(self, num: int):
        if num > len(self.cards):
            raise ValueError("Not enough cards in the deck")
        dealt_cards = self.cards[:num]
        self.cards = self.cards[num:]
        return dealt_cards
    
    def add(self, cards: Card | list[Card]):
        if isinstance(cards, list):
            self.cards.extend(cards)
        else:
            self.cards.append(cards)
    
    def __contains__(self, card: Card):
        return card in self.cards
    
    def __eq__(self, other):
        if not isinstance(other, Deck):
            return False
        return sorted(self.cards) == sorted(other.cards)

    def remove(self, cards):
        for card in cards:
            if card in self.cards:
                self.cards.remove(card)

    