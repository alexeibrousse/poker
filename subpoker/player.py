class Player:
    def __init__(self, name: str, chips: int):
        self.name = name
        self.chips = chips
        self._hand = [] # For internal use
        self.folded = False
        self.all_in = False
        self.bet = 0

        self.actions = ["check", "fold", "call", "raise", "all_in"]

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
    
    
    def has_folded(self):
        if self.folded:
            return f"{self.name} has folded."
        return f"{self.name} is still in the game."
    
    def fold(self):
        self.folded = True
        self._hand = []

    def check(self, current_bet: int):
        return True

    def bet_chips(self, amount: int):
        self.chips -= amount
        self.bet += amount

    def raise_bet(self, amount: int):
        self.chips -= amount
        self.bet += amount
        if self.chips == 0:
            self.all_in = True
    
    def go_all_in(self):
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
    
    def add_chips(self, amount: int):
        self.chips += amount

    def perform_action(self, action: str, current_bet: int = 0, amount: int = 0) -> int:
        if action not in self.actions:
            raise ValueError(f"Invalid action: {action}")
        
        if action == "check":
            if self.bet != current_bet:
                raise ValueError("Cannot check when bet is not equal to current bet.")
            return 0
        
        elif action == "fold":
            if self.bet == current_bet:
                raise ValueError("Cannot fold when bet is equal to current bet.")
            self.fold()
            return 0
        
        elif action == "call":
            to_call = current_bet - self.bet
            if to_call < 0:
                raise ValueError("Current bet is less than player's bet.")
            self.bet_chips(to_call)
            return to_call
        
        elif action == "raise":
            raise_amount = amount - self.bet
            if raise_amount <= 0:
                raise ValueError("Raise amount must be greater than the current bet.")
            self.raise_bet(raise_amount)
            return raise_amount
        
        elif action == "all_in":
            to_all = self.chips
            self.go_all_in()
            return to_all
