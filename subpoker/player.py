class Player:
    def __init__(self, name: str, chips: int):
        self.name = name
        self.chips = chips
        self._hand = [] # For internal use
        self.folded = False
        self.all_in = False
        self.bet = 0

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, cards: list):
        if not isinstance(cards, list) or len(cards) != 2:
            raise ValueError("A poker hand must have exactly 2 cards.")
        self._hand = cards
    
    def __str__(self):
        return f"{self.name} ({self.chips} chips)"
    
    def __repr__(self):
        return f"Player({self.name}, {self.chips})"
    
    def fold(self):
        self.folded = True
        self._hand = []
    
    def has_folded(self):
        if self.folded:
            return f"{self.name} has folded."
        return f"{self.name} is still in the game."
    
    def check(self, current_bet: int):
        if self.bet < current_bet:
            raise ValueError(f"{self.name} cannot check — must call or fold.")
        return True

    def call(self, amount: int):
        if amount > self.chips:
            raise ValueError(f"{self.name} does not have enough chips to call {amount}.")
        self.chips -= amount
        self.bet += amount
        if self.chips == 0:
            self.all_in = True

    def raise_bet(self, amount: int):
        if amount > self.chips:
            raise ValueError(f"{self.name} does not have enough chips to call {amount}.")
        self.chips -= amount
        self.bet += amount
        if self.chips == 0:
            self.all_in = True
    
    def all_in(self):
        self.all_in = True
        self.bet += self.chips
        self.chips = 0
    
    def win_pot(self, amount: int):
        self.chips += amount
        self.bet = 0
        self.all_in = False
    
    def reset(self):
        self.folded = False
        self.all_in = False
        self.bet = 0
        self._hand = []