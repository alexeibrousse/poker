from .table import Table
from .player import Player

class Game:
    def __init__(self, players: list, small_blind: int):
        if len(players) < 2:
            raise ValueError("At least two players are required to start a game.")
        for i,player in enumerate(players):
            player.id = i
        self.players = players
        self.table = Table(players)
        self.sb = small_blind
        self.bb = 2*small_blind
        self.current_bet = 0
        self.round = 0
        self.dealer_position = -1

    def rotate_blinds(self):
        self.dealer_position = (self.dealer_position + 1) % len(self.players)

        sb_index = (self.dealer_position + 1) % len(self.players)
        bb_index = (self.dealer_position + 2) % len(self.players)
        self.current_dealer = self.players[self.dealer_position]
        self.current_sb = self.players[sb_index]
        self.current_bb = self.players[bb_index]

        self.current_sb.bet_chips(self.sb)
        self.current_bb.bet_chips(self.bb)

        self.table.pot = self.sb + self.bb
        self.current_bet = self.bb
        self.round += 1

    def reset(self):
        self.table.reset()
        self.current_bet = 0

    def show_state(self):
        for player in self.players:
            print(f"{player.name}'s hand: {player.hand}")
        print(f"Board: {self.table.board}")
        print(f"Pot: {self.table.pot}")

    def start_round(self):
        self.reset()
        self.rotate_blinds()
        self.table.deal_private()

    def deal_flop(self):
        self.table.deal_board(3)

    def deal_turn(self):
        self.table.deal_board(1)

    def deal_river(self):
        self.table.deal_board(1)
    
    def betting_round(self):
        for player in self.players:
            if player.folded or player.all_in:
                continue

            while True:
                action = input(f"{player.name}, Choose an action from {player.actions}: ").strip().lower()

                if action not in player.actions:
                    print("Not a valid option. Try again.")
                    continue

                amount = 0
                if action == "raise":
                    try:
                        amount = int(input("Enter raise amount: ").strip())
                    except ValueError:
                        print("Invalid number. Try again.")
                        continue

                try:
                    moved = player.perform_action(action, current_bet=self.current_bet, amount=amount)
                except ValueError as err:
                    print(err)
                    continue

                self.table.pot += moved
                if action in ("raise", "all_in"):
                    self.current_bet = player.bet

                break
        