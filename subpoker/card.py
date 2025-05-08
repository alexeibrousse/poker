class Card:
    suits = ['♠', '♥', '♦', '♣']    
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self,rank: str,suit: str):
        self.rank=rank
        self.suit=suit

    def __str__(self):
       return f"{self.rank}{self.suit}"
    
    def __repr__(self):
        return f"{self.rank}{self.suit}"
    
    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit
    
    def __hash__(self):
        return hash((self.rank, self.suit))