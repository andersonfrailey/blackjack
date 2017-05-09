"""
Supporting functions for user mode
"""

import pandas as pd
import numpy as np


def probability(data, count, total, d_up):
    """
    Function to display probability of winning a certain hand. Uses results
    data from simulated games

    Parameters
    ----------
    data: DF of hand results from simulations
    count: count at start of hand
    total: player's total
    d_up: dealer's up card

    Returns
    -------
    Proabability of the player winning the hand
    """
    beat = data['result'] == 1
    dbust = data['result'] == 4
    push = data['result'] == 3
    win = beat | dbust | push
    p = (float(len(data[(data['start'] == total) & (data['count'] == count) &
                        (data['d_up'] == d_up) & (win)])) /
         float(len(data[(data['start'] == total) & (data['count'] == count) &
                        (data['d_up'] == d_up)])))
    return round((p * 100), 2)


def bust(data, count, total, soft):
    """
    Function to determine how often a player busts hitting a certain hand
    """
    b = (float(len(data[(data['start'] == total) & (data['end'] > 21) &
                        (data['count'] == count) & (data['soft'] == soft)])) /
         float(len(data[(data['start'] == total) & (data['count'] == count) &
                        (data['soft'] == soft)])))
    return round((b * 100), 2)
