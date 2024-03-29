# Class for creating the deck

import random
from py21.card import Card


class Deck:

    def __new__(cls, *args, **kwargs):
        """
        Allow a random seed to be set
        """
        cls._seed = kwargs.get("seed", None)
        cls.random = random.Random(cls._seed)
        return object.__new__(cls)

    def __init__(self, decks, test=False, burn=True, **kwargs):
        """
        Initialize Deck class and create the first deck
        Parameters
        ----------
        decks: number of decks to create
        test: boolean indicator for whether we should create the deck used for
              testing
        burn: boolean indicator for whether we burn the first card of a new
              deck
        """
        self.deck = []
        self.decks = decks
        self.burn = burn
        self.num_creates = 0
        if test:
            self._create_test_deck()
        else:
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
        assert len(self.deck) == 0
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
        assert len(self.deck) == 52 * self.decks
        # reset count variables
        setattr(self, "hands_played", 0)
        if self.burn:
            self.deal()

    def shuffle(self):
        """
        Shuffle the deck
        """
        self.random.shuffle(self.deck)

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

    def _create_test_deck(self):
        """
        Create a deck used for testing
        """
        # this deck is created to ensure that the player will need to split
        # their hand
        test_ranks = [6, 4, 6, 9, 8, 2, 12, 3, 13, 5, 4, 10, 11]
        for rank in test_ranks:
            self.deck.append(Card(rank, "C"))

    def __len__(self):
        return len(self.deck)
