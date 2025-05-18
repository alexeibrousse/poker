from .card import Card
import random

class Deck:
    def __init__(self):
        self.cards = []
        for suit in Card.suits:
            for rank in Card.ranks:
                self.cards.append(Card(rank, suit))
    
    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self): # allows for "for card in deck"
        return iter(self.cards)
    

    def __getitem__(self,position: int) -> Card:
        return self.cards[position]
    
    def __str__(self) -> str:
        return f"({self.cards})"   

    def __repr__(self) -> str:
        return f"Deck with {len(self.cards)} cards: ({self.cards})"

    def shuffle(self) -> "Deck": 
        random.shuffle(self.cards)
        return self
    
    def sort(self) -> "Deck":
        self.cards.sort()
        return self

    def reset(self) -> "Deck":
        self.cards = []
        for suit in Card.suits:
            for rank in Card.ranks:
                self.cards.append(Card(rank, suit))
        return self

    def deal(self, num: int) -> list[Card]:
        if num > len(self.cards):
            raise ValueError("Not enough cards in the deck")
        dealt_cards = self.cards[:num]
        self.cards = self.cards[num:]
        return dealt_cards
    
    def add(self, cards: Card | list[Card]) -> None:
        if isinstance(cards, list):
            self.cards.extend(cards)
        else:
            self.cards.append(cards)
    
    def __contains__(self, card: Card) -> bool:
        return card in self.cards
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Deck):
            return False
        return sorted(self.cards) == sorted(other.cards)

    def remove(self, cards) -> None:
        for card in cards:
            if card in self.cards:
                self.cards.remove(card)

    