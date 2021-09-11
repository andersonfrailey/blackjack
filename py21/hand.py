"""
Hand class definition
"""
from .card import Card
from .player import Player


class Hand:

    def __init__(self, card_one, from_split=False, player=None, **kwargs):
        """
        This class handles all of the logic for individual hads. It is
        initiated by passing in two cards that will are the starting cards,
        and a Player object that is the player who is playing the hand.

        Parameters
        ----------
        card_one: first card in the hand
        from_split: boolean indicator for if the hand was delt after splitting
                    a pair
        player: an instance of a player object that represents which player
                was delt this hand
        **kwargs: arguments that get passed to functions called in the hand
                  class such as the wager function of the player
        """
        if isinstance(card_one, Card):
            self.card_one = card_one
        else:
            raise TypeError("'card_one' must be a Card object.")

        if player:
            if isinstance(player, Player):
                self.player = player
            else:
                raise TypeError("'player' must be a Player object.")
            self.wager = self.player.wager(**kwargs)
        self.cards = [card_one]
        self.split = False
        self.soft = card_one.rank == 14
        self.stand = False
        self.bust = False
        self.blackjack = False
        self.from_split = from_split
        self.insurance = False
        self.total = card_one.value
        self.surrender = False
        self.double_down = False
        # this is used to determine whether to add 11 or 1 when delt an ace
        self.non_ace_total = 0
        self.num_aces = 1 * self.soft
        self.num_hard_aces = self.num_aces

    def add_card_two(self, card):
        """
        Add second card to hand.
        """
        self.add_card(card)
        self._check_blackjack()

    def add_card(self, card):
        """
        Add a new card to the hand
        """
        if not isinstance(card, Card):
            raise TypeError("'card' must be a card object.")
        # append new card to list of cards in the hand
        self.cards.append(card)
        self.total = card + self.total
        # aces require a little more work
        if card.rank == 14:
            self.soft = True
            self.num_aces += 1
            self.num_hard_aces += 1
        # account for soft hands
        if self.total > 21 and self.soft:
            self.total -= 10
            self.num_hard_aces -= 1
            self.soft = False
            # catch the edge case where you're delt 12+ aces
            if self.total > 21:
                self.total -= 10
                self.num_hard_aces -= 1
                self.soft = False
            if self.num_hard_aces > 0:
                self.soft = True
        if self.total > 21:
            self.bust = True

    def summary_data(self):
        """
        This method returns a dictionary with data on the hand.
        """
        data = {
            "total": self.total,
            "card_one_value": self.cards[0].value,
            "card_two_value": self.cards[1].value,
            "card_one_rank": self.cards[0].rank,
            "card_two_rank": self.cards[1].rank,
            "cards": " ".join([str(card) for card in self.cards]),
            "soft": int(self.soft),
            "from_split": int(self.from_split),
            "blackjack": int(self.blackjack),
            "num_cards": len(self.cards),
            "start_total": self.cards[0] + self.cards[1],
            "wager": int(self.wager),
            "insurance": int(self.insurance),
            "surrender": int(self.surrender),
            "double_down": int(self.double_down),
            "num_aces": self.num_aces,
            "num_hard_aces": self.num_hard_aces
        }
        return data

    # Private methods of Card class

    def _check_blackjack(self):
        if self.total == 21:
            setattr(self, "blackjack", True)
            setattr(self, "stand", True)

    def __gt__(self, other):
        if not isinstance(other, Hand):
            raise TypeError("Hand objects can only be compared to other "
                            "Hand objects.")
        return self.total > other.total

    def __lt__(self, other):
        if not isinstance(other, Hand):
            raise TypeError("Hand objects can only be compared to other "
                            "Hand objects.")
        return other.total > self.total

    def __eq__(self, other):
        if not isinstance(other, Hand):
            raise TypeError("Hand objects can only be compared to other "
                            "Hand objects.")
        return self.total == other.total

    def __str__(self) -> str:
        return (
            " ".join([str(card) for card in self.cards]) +
            f"\nTotal: {self.total}"
        )
