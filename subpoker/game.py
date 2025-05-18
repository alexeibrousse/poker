from .table import Table
from .player import Player
from typing import Optional
from .hand_evaluator import evaluate_hand, get_hand_rank_string


class Game:
    def __init__(self, players: list, small_blind: int):
        if len(players) < 2:
            raise ValueError("At least 2 players are needed to start a game.")
        for i,player in enumerate(players):
            player.id = i
        self.players = players
        self.table = Table(players)
        self.small_blind = small_blind
        self.big_blind = 2 * small_blind
        self.dealer_position = -1
        self.round = 0
        self.state = "preflop"
        self.game_over = False


    def get_active_nonfolded_players(self):
        return [p for p in self.players if p.is_active and not p.folded]


    def rotate_blinds(self) -> None:
        self.dealer_position = (self.dealer_position + 1) % len(self.players)

        sb_index = (self.dealer_position + 1) % len(self.players)
        bb_index = (self.dealer_position + 2) % len(self.players)

        self.current_sb = self.players[sb_index]
        self.current_bb = self.players[bb_index]

        if self.current_sb.chips < self.small_blind:
            print(f"{self.current_sb.name} posts small blind and is all-in for {self.current_sb.chips} chips!")
            amount = self.current_sb.chips
            self.current_sb.go_all_in()
        else:
            print(f"{self.current_sb.name} posts small blind of {self.small_blind} chips.")
            amount = self.small_blind
            self.current_sb.bet_chips(amount)
        eligible_players = set(self.get_active_nonfolded_players())  # Eligible players for pot
        self.table.add_to_pot(amount, eligible_players=eligible_players)

        if self.current_bb.chips < self.big_blind:
            print(f"{self.current_bb.name} posts big blind and is all-in for {self.current_bb.chips} chips!")
            amount = self.current_bb.chips
            self.current_bb.go_all_in()
        else:
            print(f"{self.current_bb.name} posts big blind of {self.big_blind} chips.")
            amount = self.big_blind
            self.current_bb.bet_chips(amount)
        eligible_players = set(self.get_active_nonfolded_players())  # Eligible players for pot
        self.table.add_to_pot(amount, eligible_players=eligible_players)

        self.current_bet = max(self.current_sb.bet, self.current_bb.bet) # in case bb is all-in

    
    def reset(self) -> None:
        self.table.reset()
        self.current_bet = 0
        self.round += 1
        self.state = "preflop"

    def show_state(self) -> None:
        for player in self.players:
            if player is self.current_sb:
                print(f"{player.name}'s hand: {player.hand} | is small blind")
            elif player is self.current_bb:
                print(f"{player.name}'s hand: {player.hand} | is big blind")
            else:
                print(f"{player.name}'s hand: {player.hand}") 
    
    def show_full_state(self) -> None:
        print(f"Current round: {self.round} | Dealer is {self.players[self.dealer_position].name}")
        print(f"Board: {self.table.board} | State: {self.state}")
        print(f"Pot: {self.table.total_pot()} | Current Bet: {self.current_bet}")
        for player in self.players:
            if player is self.current_sb:
                print(f"{player.name}'s hand: {player.hand} | is small blind")
            elif player is self.current_bb:
                print(f"{player.name}'s hand: {player.hand} | is big blind")
            else:
                print(f"{player.name}'s hand: {player.hand}") 
        print(f"Active players: {[player.name for player in self.players if player.is_active]}")
        print(f"Deck left: {len(self.table.deck)} cards")


    def start_round(self) -> None:
        self.reset()
        self.rotate_blinds()
        self.table.deal_private()

    def deal_flop(self) -> None:
        self.state = "flop"
        self.table.deal_board(3)

    def deal_turn(self) -> None:
        self.state = "turn"
        self.table.deal_board(1)

    def deal_river(self) -> None:
        self.state = "river"
        self.table.deal_board(1)
    
    def only_one_player_left(self) -> bool:
        return len([p for p in self.players if p.is_active and not p.folded]) == 1


    def award_last_player(self) -> None:
        remaining_player = next(p for p in self.players if p.is_active and not p.folded)
        total_pot = self.table.total_pot()
        remaining_player.chips += total_pot
        print(f"{remaining_player.name} wins the pot of {total_pot} chips as the last player standing.")
        self.table.pots = []

    def betting_order(self):
        if len(self.players) == 2: # When only 2 players are left, the order is fixed
            if self.state == "preflop":
                return [self.current_sb, self.current_bb]
            return [self.current_bb, self.current_sb]
        else:
            if self.state == "preflop": # Order is different to rest of round
                first = (self.players.index(self.current_bb) + 1) % len(self.players)
            else:
                first = (self.dealer_position + 1) % len(self.players)
            return [self.players[(first + i) % len(self.players)] for i in range(len(self.players))]
    
    def valid_actions(self, player, to_call: int)-> list:
        if not player.is_active:
            return []

        actions = ["fold"]

        if player.chips == 0: # player should already be all-in
            return actions

        if to_call == 0:
            actions.append("check")
            if player.chips > 0:
                actions.extend(["raise", "all-in"])
        elif to_call > 0:
            if player.chips > to_call:
                actions.append("call")
                actions.extend(["raise", "all-in"])
            elif player.chips == to_call:
                actions.append("call")
            elif player.chips < to_call:
                actions.append("all-in")

        return list(dict.fromkeys(actions)) # no repetitions
    
    def process_action(self, player, action: str, to_call: int = 0, raise_to: Optional[int] = None) -> bool:
        """
        Processes a player's action during betting.

        Raises:
            ValueError: If the action is invalid or cannot be processed.
        """
        if action == "fold":
            player.fold()
            print(f"{player.name} has folded.")
            return True

        elif action == "check":
            print(f"{player.name} checks.")
            return True

        elif action == "call":
            player.bet_chips(to_call)
            eligible_players = set(self.get_active_nonfolded_players())  # Eligible players for pot
            self.table.add_to_pot(to_call, eligible_players=eligible_players)
            return True

        elif action == "raise":
            if raise_to is None or raise_to <= player.bet or raise_to - player.bet <= to_call:
                raise ValueError("Invalid raise amount.")
            raise_amount = raise_to - player.bet
            if raise_amount > player.chips:
                raise ValueError("Not enough chips to raise.")
            player.bet_chips(raise_amount)
            self.current_bet = raise_to
            eligible_players = set(self.get_active_nonfolded_players())  # Eligible players for pot
            self.table.add_to_pot(raise_amount, eligible_players=eligible_players)
            print(f"{player.name} raises to {raise_to}.")
            return True

        elif action == "all-in":
            all_in_amount = player.chips
            player.go_all_in()
            eligible_players = set(self.get_active_nonfolded_players())  # Eligible players for pot
            self.table.add_to_pot(all_in_amount, eligible_players=eligible_players)
            if all_in_amount + player.bet > self.current_bet:
                self.current_bet = all_in_amount + player.bet
                print(f"{player.name} goes all-in for {all_in_amount} and sets new bet of {self.current_bet}.")
            else:
                print(f"{player.name} goes all-in for {all_in_amount}.")
            return True

        else:
            raise ValueError("Unknown action.")

    
    def betting_round(self) -> None:
        players_in_hand = [p for p in self.players if not p.folded and p.is_active]
        if len(players_in_hand) <= 1:
            print("Not enough players to continue betting.")
            return

        action_order = self.betting_order()
        action_order = [player for player in action_order if player.is_active and not player.folded]

        last_raiser = None
        index = 0
        num_players = len(action_order)

        while True:
            if len([p for p in self.players if p.is_active and not p.folded]) <= 1:
                break

            player = action_order[index % num_players]

            if player.folded or player.all_in or not player.is_active:
                index += 1
                continue

            to_call = self.current_bet - player.bet
            valid_actions = self.valid_actions(player, to_call)

            valid_action_chosen = False
            while not valid_action_chosen:
                action = input(f"\n{player.name}'s turn. Chips: {player.chips}, To call: {to_call}\nValid actions: {', '.join(valid_actions)}\nChoose action: ").strip().lower()
                if action not in valid_actions:
                    print("Invalid action, try again.")
                    continue

                raise_to = None
                if action == "raise":
                    while True:
                        try:
                            raise_to_input = input("Enter total bet amount: ").strip()
                            raise_to = int(raise_to_input)
                        except ValueError:
                            print("Invalid amount. Please enter a valid integer.")
                            continue

                        if raise_to <= player.bet or raise_to - player.bet <= to_call:
                            print("Raise amount too low.")
                            continue

                        if raise_to - player.bet > player.chips:
                            print("Not enough chips to raise that amount.")
                            continue

                        break

                try:
                    if self.process_action(player, action, to_call, raise_to):
                        valid_action_chosen = True
                    else:
                        print("Action failed validation, please try again.")
                except ValueError as err:
                    print(err)
                    # retry input

                if valid_action_chosen:
                    if action == "raise" or (action == "all-in" and player.bet > self.current_bet):
                        last_raiser = player
                        index = (action_order.index(player) + 1) % num_players
                        continue  # Restart loop with updated index

            index += 1


            if last_raiser is None:
                if index >= num_players:
                    break
            else:
                if index % num_players == action_order.index(last_raiser):
                    break


    def showdown(self):
        board = self.table.board
        pots = self.table.pots  # List of dicts with 'amount' and 'players' keys

        hand_strengths = {}
        for player in self.players:
            if not player.folded:
                hand_strengths[player] = evaluate_hand(player.hand, board)

        winnings = {p: 0 for p in self.players}

        for pot in pots:
            # Filter eligible players for this pot
            eligible_players = [p for p in pot['players'] if not p.folded]
            if not eligible_players:
                print("A pot has no eligible players.")
                continue

            best_score = min(hand_strengths[p] for p in eligible_players)
            winners = [p for p in eligible_players if hand_strengths[p] == best_score]

            split_amount = pot['amount'] // len(winners)
            remainder = pot['amount'] % len(winners)

            for winner in winners:
                winnings[winner] += split_amount

            if remainder > 0:
                winnings[winners[0]] += remainder # convention

        for player, amount in winnings.items():
            if amount > 0:
                player.chips += amount
                print(f"{player.name} wins {amount} chips.")

        self.table.pots = []


    

    def handle_early_hand_end(self) -> bool:
        if self.only_one_player_left():
            self.award_last_player()
            self.game_over = True
            return True
        return False



    def play_hand(self) -> None:
        self.start_round()
        stages = [
            ("preflop", self.betting_round),
            ("flop", self.deal_flop),
            ("flop_bet", self.betting_round),
            ("turn", self.deal_turn),
            ("turn_bet", self.betting_round),
            ("river", self.deal_river),
            ("river_bet", self.betting_round),
        ]

        for state, action in stages:
            self.state = state
            action()
            if self.handle_early_hand_end():
                return

        self.showdown()

        self.players = [p for p in self.players if p.chips > 0]
        if len(self.players) == 1:
            print(f"{self.players[0].name} wins the game!")
            self.game_over = True

    def run_game(self):
        while not self.game_over:
            self.play_hand()
            if self.game_over:
                print("Game over!")
                winner = self.players[0] if self.players else None
                if winner:
                    print(f"{winner.name} is the champion!")
                break

            while True:
                cont = input("Play next hand? (y/n): ").strip().lower()
                if cont == 'n':
                    print("Game stopped by user.")
                    break
                elif cont != 'y':
                    print("Invalid input. Please enter 'y' or 'n'.")
                    continue
            break