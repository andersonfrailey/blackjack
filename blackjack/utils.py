"""
Class to handle data from the blackjack game
"""

import pandas as pd
import numpy as np


class Data(object):

    def __init__(self):
        """

        """
        self.card_freq_dict = {'card': [], 'count': [], 'players': [],
                               'hands': []}

    def card_freq(self, card, count, players, hands):
        """
        Track how many times a card value appears, what the count is when it
        appears, how many players are playing, and how many hands have been
        played
        Parameters
        ----------
        card: card object
        count: game count
        players: number of players
        hands: number of hands played in the deck

        Returns
        -------

        """
        self.card_freq_dict['card'].append(card.rank)
        self.card_freq_dict['count'].append(count)
        self.card_freq_dict['players'].append(players)
        self.card_freq_dict['hands'].append(hands)
        # TODO add np.where to change value for face cards and aces when
        # converting to DataFrame

    def results(self, player, dealer, count):
        """
        Hold results for each hand
        Parameters
        ----------
        player
        dealer
        count

        Returns
        -------

        """
        # TODO if possible, just add rows to an existing DataFrame. Possible:
        # concat rows

    def hit_result(self, start_total, end_total, count):
        """
        Contains the result of a hit
        Parameters
        ----------
        start_total: total before hit
        end_total: total after hitting
        count: deck count when taking a hit

        Returns
        -------

        """
        # TODO: add stating total, ending total to a DataFrame

    def collect_side(self, poker, inbtwn, count):
        """
        Collect the results of the side bets
        Parameters
        ----------
        poker: result of poker hand
        inbtwn: result of in between bet
        count: Count going into the hand

        Returns
        -------

        """
