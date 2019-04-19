# Card class used when creating the deck


class Card:
    RANKS = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}
    SUITS = {'C', 'D', 'H', 'S'}
    # dictionary to hold rank:value pairs
    VALUES = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10,
              11: 10, 12: 10, 13: 10, 14: 11}

    def __init__(self, rank, suit):
        """
        Each card has a rank, suit, and value
        """
        if rank in Card.RANKS:
            self.rank = rank
            self.value = Card.VALUES[rank]
        else:
            raise ValueError(f"'rank' must be in {Card.RANKS}")
        if suit in Card.SUITS:
            self.suit = suit
        else:
            raise ValueError(f"'suit' must be in {Card.SUITS}")

    def __str__(self):
        """
        Print J, Q, K, and A instead of 11, 12, 13, 14
        And print the card symbols instead of letters
        """
        suit_symobols = {
            "C": "\u2663",
            "D": "\u2666",
            "H": "\u2665",
            "S": "\u2660"
        }
        if self.rank == 14:
            rank = 'A'
        elif self.rank == 13:
            rank = 'K'
        elif self.rank == 12:
            rank = 'Q'
        elif self.rank == 11:
            rank = 'J'
        else:
            rank = self.rank
        return str(rank) + suit_symobols[self.suit]

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __add__(self, other):
        if isinstance(other, Card):
            return self.value + other.value
        elif isinstance(other, int):
            return other + self.value
        else:
            raise TypeError("Other must be of type 'Card' or 'int'")
