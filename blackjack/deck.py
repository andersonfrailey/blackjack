# Class for creating the deck

import random
from card import Card


class Deck (object):

    def __init__(self, decks):
        """
        Initialize Deck class and create the first deck
        """
        self.deck = []
        self.decks = decks
        self.num_creates = 0
        self.create_deck()
        self.num_pop = 0

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
            print self.num_creates
            msg = 'Deck is empty'
            raise ValueError(msg)
        else:
            self.num_pop += 1
            return self.deck.pop(0)

    def __len__(self):
        return len(self.deck)
