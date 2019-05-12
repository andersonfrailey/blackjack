"""
This file contains a number of built in strategies that can be passed to the
Player class as arguments for strategy_func, wager_func, or insurance_func
"""

import os
import random
import pandas as pd


CUR_PATH = os.path.abspath(os.path.dirname(__file__))
# read in strategy files
BASIC_HARD = pd.read_csv(os.path.join(CUR_PATH, "strategy_files",
                                      "basic_hard.csv"),
                         index_col=0).to_dict()
BASIC_SOFT = pd.read_csv(os.path.join(CUR_PATH, "strategy_files",
                                      "basic_soft.csv"),
                         index_col=0).to_dict()
BASIC_SPLIT = pd.read_csv(os.path.join(CUR_PATH, "strategy_files",
                                       "basic_split.csv"),
                          index_col=0).to_dict()


def basic_strategy(player, hand, dealer_up, game_params, **kwargs):
    """
    Function that plays with the basic strategy. Source:
    https://www.blackjackapprenticeship.com/blackjack-strategy-charts/

    This function can be used at the strategy_func argument in an instance of
    of the Player class.
    Parameters
    ----------
    player: instance of the Player class
    hand: instance of the Hand class
    dealer_up: dealer's up card
    game_params: rules of the specific game
    **kwargs: misc. arguements that get passed into the function
    Returns
    -------
    One of the following: HIT, STAND, DOUBLE, SPLIT
    """
    # strategy for splits
    if (hand.cards[0].value == hand.cards[1].value) and len(hand.cards) == 2:
        action = BASIC_SPLIT[str(dealer_up)][hand.cards[0].value]
        if action == "Y":
            return "SPLIT"
        elif action == "Y/N":
            if game_params.double_after_split:
                return "SPLIT"
    # strategy for hard hands
    if not hand.soft:
        action = BASIC_HARD[str(dealer_up)][hand.total]
    else:
        action = BASIC_SOFT[str(dealer_up)][hand.total]

    # return input accepted by the blackjack game
    if action == "H":
        return "HIT"
    elif action == "S":
        return "STAND"
    elif action == "D" or action == "Ds":
        return "DOUBLE"


def user_input(player, hand, dealer_up, count, ten_count, other_count,
               **kwargs):
    """
    Function that asks the user for input to select an action

    This function can be used at the strategy_func argument in an instance of
    of the Player class.
    """
    print(f"Total: {hand.total}")
    print(f"Ten Ratio: {other_count / ten_count}")
    action = input("\nEnter Action (h, s, d, sp): ")
    if action == "h":
        return "HIT"
    elif action == "s":
        return "STAND"
    elif action == "d":
        return "DOUBLE"
    elif action == "sp":
        return "SPLIT"


def hit_to_seventeen(player, hand, **kwargs):
    """
    Hit until the hand total reaches 17

    This function can be used at the strategy_func argument in an instance of
    of the Player class.
    """
    if hand.total >= 17:
        return "STAND"
    else:
        return "HIT"


def minimum_bet(player, min_bet, max_bet, **kwargs):
    """
    Function to serve as the default wager function if user doesn't input
    their own
    """
    return min_bet


def maximum_bet(player, min_bet, max_bet, **kwargs):
    """
    Always bet the max
    """
    return max_bet


def decline_insurance(**kwargs):
    """
    Function for always declining insurance.

    This can be used as the insurance_func argument in an insuance of the
    Player class.
    """
    return False


def accept_insurance(**kwargs):
    """
    Function for always accepting insurance.

    This can be used as the insurance_func argument in an insuance of the
    Player class.
    """
    return True


def random_choice(**kwargs):
    """
    Randomly pick a move
    """
    return random.choice(["HIT", "STAND"])
