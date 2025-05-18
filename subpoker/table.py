from .deck import Deck

class Table():
    def __init__(self, players: list):
        self.players = players
        self.deck = Deck().shuffle()
        self.board = []
        self.pots = []  # List of dicts: {"amount": int, "players": set}
    
    def reset(self) -> None:
        self.deck.reset().shuffle()
        self.board = []
        self.pots = []
        for player in self.players:
            player.reset()
        
    def remove_busted_players(self):
        busted = [player for player in self.players if player.chips == 0]
        for player in busted:
            print(f"{player.name} is out of chips and has been eliminated.")
        self.players = [player for player in self.players if player.chips > 0]

    def deal_private(self) -> None:
        for player in self.players:
            player.hand = self.deck.deal(2)

    def deal_board(self, num:int) -> list:
        self.deck.deal(1) # Burn card
        self.board.extend(self.deck.deal(num))
        return self.board

    def add_to_pot(self, amount: int, eligible_players=None)  -> int:
        if eligible_players is None: 
            eligible_players = set(self.players)
        
        if self.pots and self.pots[-1]["players"] == eligible_players:
            self.pots[-1]["amount"] += amount
        else:
            self.pots.append({"amount": amount, "players": eligible_players.copy()})
        return self.total_pot()

    def create_side_pot(self, amount: int, eligible_players: list) -> None:
        self.pots.append({"amount": amount, "players": set(eligible_players)})

    def total_pot(self) -> int:
        return sum(pot["amount"] for pot in self.pots)
    

    def __str__(self) -> str:
        pots_info = " | ".join(f"Pot: {pot['amount']} ({len(pot['players'])} eligible)" for pot in self.pots)
        return f"Table with {len(self.players)} players. | {pots_info} | Board: {self.board}"
    
    def show_board(self) -> str:
        if not self.board:
            return f"Board is empty. Total Pot: {self.total_pot()}"
        
        cards = " ".join(str(card) for card in self.board)
        return f"Board: {cards} | Total Pot: {self.total_pot()}"


    
