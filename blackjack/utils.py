"""
Class to handle data from the blackjack game
"""

import pandas as pd
import numpy as np


class Data(object):

    def __init__(self):
        """

        """
        # Dictionary for holding card frequencies
        self.card_freq_dict = {'card': [], 'count': [], 'players': [],
                               'hands': [], 'decks': []}

        # Dictionary for side bet results
        self.side_dict = {'poker': [], 'inbtwn': [], 'count': [], 'decks': []}

        # Dictionary for hit results
        self.hit_dict = {'start': [], 'end': [], 'count': [], 'decks': []}

        # Dictionary for tracking number of times dealer has blackjack
        self.insurance_dict = {'blackjack': [], 'decks': []}

        # Dictionary for holding hand results
        self.results_dict = {'start': [], 'end': [], 'dealer': [], 'd_up': [],
                             'taken': [], 'decks': [], 'seat': [],
                             'players': [], 'result': []}

    def card_freq(self, card, count, players, hands, decks):
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
        decks: Number of decks in play

        Returns
        -------

        """
        # Change aces and face cards
        if card.rank == 14:
            rank = 'A'
        elif 11 <= card.rank <= 13:
            rank = 10
        else:
            rank = card.rank

        # Append data to the dictionary
        self.card_freq_dict['card'].append(rank)
        self.card_freq_dict['count'].append(count)
        self.card_freq_dict['players'].append(players)
        self.card_freq_dict['hands'].append(hands)
        self.card_freq_dict['decks'].append(decks)

    def collect_side(self, poker, inbtwn, count, decks):
        """
        Collect the results of the side bets
        Parameters
        ----------
        poker: result of poker hand
        inbtwn: result of in between bet
        count: Count going into the hand
        decks: Number of decks in play

        Returns
        -------

        """
        # Add data to dictionary
        self.side_dict['poker'].append(poker)
        self.side_dict['inbtwn'].append(inbtwn)
        self.side_dict['count'].append(count)
        self.side_dict['decks'].append(decks)

    def hit_result(self, start_total, end_total, count, decks):
        """
        Contains the result of a hit
        Parameters
        ----------
        start_total: total before hit
        end_total: total after hitting
        count: deck count when taking a hit
        decks: Number of decks in play

        Returns
        -------

        """
        # Add data to hit result dictionaries
        self.hit_dict['start'].append(start_total)
        self.hit_dict['end'].append(end_total)
        self.hit_dict['count'].append(count)
        self.hit_dict['decks'].append(decks)

    def insurance(self, blackjack, decks):
        """
        Keep track of how many times a dealer shows ace and has blackjack
        Parameters
        ----------
        blackjack
        decks

        Returns
        -------

        """
        # Add data to insurance dictionary
        self.insurance_dict['blackjack'].append(blackjack)
        self.insurance_dict['decks'].append(decks)

    def results(self, start_total, end_total, dealer_total, dealer_up, taken,
                decks, seat, players, result):
        """

        Parameters
        ----------
        start_total: Player's total from the deal
        end_total: Player's end total
        dealer_total
        dealer_up
        taken
        decks
        seat
        players
        result

        Returns
        -------

        """
        # Add data to dictionary
        self.results_dict['start'].append(start_total)
        self.results_dict['end'].append(end_total)
        self.results_dict['dealer'].append(dealer_total)
        if dealer_up == 14:
            self.results_dict['d_up'].append('A')
        elif 11 <= dealer_up <= 13:
            self.results_dict['d_up'].append(10)
        else:
            self.results_dict['d_up'].append(dealer_up)
        self.results_dict['taken'].append(taken)
        self.results_dict['decks'].append(decks)
        self.results_dict['seat'].append(seat)
        self.results_dict['players'].append(players)
        self.results_dict['result'].append(result)
