# Class for creating the deck

import random
from .card import Card


class Deck:

    def __init__(self, decks):
        """
        Initialize Deck class and create the first deck
        """
        self.deck = []
        self.decks = decks
        self.num_creates = 0
        self.create_deck()
        self.num_pop = 0
        self.hands_played = 0

    def create_deck(self):
        """
        Empties the deck then create the deck of cards by looping through all
        the suits and ranks
        Returns
        -------

        """
        del self.deck[:]
        self.num_pop = 0
        self.num_creates += 1
        for decks in range(self.decks):
            for suit in Card.SUITS:
                for rank in Card.RANKS:
                    card = Card(rank, suit)
                    self.deck.append(card)
        if len(self.deck) != 52 * self.decks:
            msg = 'Full deck not created'
            raise ValueError(msg)
        self.shuffle()
        # reset count variables
        setattr(self, "hands_played", 0)

    def shuffle(self):
        """
        Shuffle the deck
        """
        random.shuffle(self.deck)

    def deal(self):
        """
        Return:
         If the deck is empty, raise error. Otherwise return card of the top
        """
        if len(self.deck) == 0:
            msg = 'Deck is empty'
            raise IndexError(msg)
        else:
            self.num_pop += 1
            card = self.deck.pop(0)
            return card

    def check_status(self, shuffle_freq):
        """
        Check and see if the deck needs to be shuffled
        """
        # if shuffle_freq is less than one, the deck needs to be shuffled when
        # the fraction of cards remaining is less than shuffle_freq
        if shuffle_freq < 1:
            remaining_frac = len(self) / (self.decks * 52)
            _shuffle = remaining_frac <= shuffle_freq
        # else the shuffle frequency is based on the number of hands played
        else:
            _shuffle = self.hands_played >= shuffle_freq
        if _shuffle:
            self.create_deck()
        return _shuffle

    def __len__(self):
        return len(self.deck)
