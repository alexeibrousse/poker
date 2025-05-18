from treys import Evaluator, Card


evaluator = Evaluator()

def card_to_treys_str(card):
    rank_map = {
        14: 'A', 13: 'K', 12: 'Q', 11: 'J',
        10: 'T', 9: '9', 8: '8', 7: '7', 6: '6',
        5: '5', 4: '4', 3: '3', 2: '2',
        'A': 'A', 'K': 'K', 'Q': 'Q', 'J': 'J', 'T': 'T',
        '9': '9', '8': '8', '7': '7', '6': '6',
        '5': '5', '4': '4', '3': '3', '2': '2'
    }
    suit_map = {
        '♥': 'h',
        '♦': 'd',
        '♣': 'c',
        '♠': 's'
    }

    rank = rank_map[card.rank]
    suit = suit_map[card.suit]
    return rank + suit


def evaluate_hand(player_hand, board):
    
    treys_hand = [Card.new(card_to_treys_str(card)) for card in player_hand]
    treys_board = [Card.new(card_to_treys_str(card)) for card in board]
    return evaluator.evaluate(treys_board, treys_hand)


def get_hand_rank_string(score):
    
    rank_class = evaluator.get_rank_class(score)
    return evaluator.class_to_string(rank_class)
